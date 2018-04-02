# -*- coding: utf-8 -*-
# Copyright (C) 2009-2017 Anders Logg and Martin Sandve Alnæs
#
# This file is part of UFLACS.
#
# UFLACS is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# UFLACS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with UFLACS. If not, see <http://www.gnu.org/licenses/>.


# Note: Much of the code in this file is a direct translation
# from the old implementation in FFC, although some improvements
# have been made to the generated code.


from collections import defaultdict
import numpy

from ufl import product
from ffc.uflacs.backends.ufc.generator import ufc_generator
from ffc.uflacs.backends.ufc.utils import generate_return_new_switch, generate_return_int_switch, generate_error

from ffc.uflacs.elementtables import clamp_table_small_numbers
from ffc.uflacs.backends.ufc.evaluatebasis import generate_evaluate_reference_basis
from ffc.uflacs.backends.ufc.evaluatebasis import tabulate_coefficients
from ffc.uflacs.backends.ufc.evalderivs import generate_evaluate_reference_basis_derivatives
from ffc.uflacs.backends.ufc.evalderivs import _generate_combinations
from ffc.uflacs.backends.ufc.evaluatedof import generate_map_dofs, reference_to_physical_map

from ffc.uflacs.backends.ufc.jacobian import jacobian, inverse_jacobian, orientation, fiat_coordinate_mapping, _mapping_transform

index_type = "int64_t"

def generate_element_mapping(mapping, i, num_reference_components, tdim, gdim, J, detJ, K):
    # Select transformation to apply
    if mapping == "affine":
        assert num_reference_components == 1
        num_physical_components = 1
        M_scale = 1
        M_row = [1]  # M_row[0] == 1
    elif mapping == "contravariant piola":
        assert num_reference_components == tdim
        num_physical_components = gdim
        M_scale = 1.0 / detJ
        M_row = [J[i, jj] for jj in range(tdim)]
    elif mapping == "covariant piola":
        assert num_reference_components == tdim
        num_physical_components = gdim
        M_scale = 1.0
        M_row = [K[jj, i] for jj in range(tdim)]
    elif mapping == "double covariant piola":
        assert num_reference_components == tdim**2
        num_physical_components = gdim**2
        # g_il = K_ji G_jk K_kl = K_ji K_kl G_jk
        i0 = i // tdim  # i in the line above
        i1 = i % tdim   # l ...
        M_scale = 1.0
        M_row = [K[jj,i0]*K[kk,i1] for jj in range(tdim) for kk in range(tdim)]
    elif mapping == "double contravariant piola":
        assert num_reference_components == tdim**2
        num_physical_components = gdim**2
        # g_il = (det J)^(-2) Jij G_jk Jlk = (det J)^(-2) Jij Jlk G_jk
        i0 = i // tdim  # i in the line above
        i1 = i % tdim   # l ...
        M_scale = 1.0 / (detJ*detJ)
        M_row = [J[i0,jj]*J[i1,kk] for jj in range(tdim) for kk in range(tdim)]
    else:
        error("Unknown mapping: %s" % mapping)
    return M_scale, M_row, num_physical_components


class ufc_finite_element(ufc_generator):
    "Each function maps to a keyword in the template. See documentation of ufc_generator."
    def __init__(self):
        ufc_generator.__init__(self, "finite_element")

    def cell_shape(self, L, cell_shape):
        return L.Return(L.Symbol("ufc::shape::" + cell_shape))

    def topological_dimension(self, L, topological_dimension):
        return L.Return(topological_dimension)

    def geometric_dimension(self, L, geometric_dimension):
        return L.Return(geometric_dimension)

    def space_dimension(self, L, space_dimension):
        return L.Return(space_dimension)

    def value_rank(self, L, value_shape):
        return L.Return(len(value_shape))

    def value_dimension(self, L, value_shape):
        return generate_return_int_switch(L, "i", value_shape, 1)

    def value_size(self, L, value_shape):
        return L.Return(product(value_shape))

    def reference_value_rank(self, L, reference_value_shape):
        return L.Return(len(reference_value_shape))

    def reference_value_dimension(self, L, reference_value_shape):
        return generate_return_int_switch(L, "i", reference_value_shape, 1)

    def reference_value_size(self, L, reference_value_shape):
        return L.Return(product(reference_value_shape))

    def degree(self, L, degree):
        return L.Return(degree)

    def family(self, L, family):
        return L.Return(L.LiteralString(family))

    def num_sub_elements(self, L, num_sub_elements):
        return L.Return(num_sub_elements)

    def create_sub_element(self, L, ir):
        classnames = ir["create_sub_element"]
        return generate_return_new_switch(L, "i", classnames, factory=ir["jit"])

    def map_dofs(self, L, ir, parameters):
        """Generate code for map_dofs()"""
        return generate_map_dofs(L, ir["evaluate_dof"])

    def tabulate_reference_dof_coordinates(self, L, ir, parameters):
        # TODO: Change signature to avoid copy? E.g.
        # virtual const std::vector<double> & tabulate_reference_dof_coordinates() const = 0;
        # See integral::enabled_coefficients for example

        # TODO: ensure points is a numpy array,
        #   get tdim from points.shape[1],
        #   place points in ir directly instead of the subdict
        ir = ir["tabulate_dof_coordinates"]

        # Raise error if tabulate_reference_dof_coordinates is ill-defined
        if not ir:
            msg = "tabulate_reference_dof_coordinates is not defined for this element"
            return generate_error(L, msg, parameters["convert_exceptions_to_warnings"])

        # Extract coordinates and cell dimension
        tdim = ir["tdim"]
        points = ir["points"]

        # Output argument
        reference_dof_coordinates = L.Symbol("reference_dof_coordinates")

        # Reference coordinates
        dof_X = L.Symbol("dof_X")
        dof_X_values = [X[jj] for X in points for jj in range(tdim)]
        decl = L.ArrayDecl("static const double", dof_X,
                           (len(points) * tdim,), values=dof_X_values)
        copy = L.MemCopy(dof_X, reference_dof_coordinates, tdim*len(points))

        code = [decl, copy]
        return code

    def evaluate_reference_basis(self, L, ir, parameters):
        data = ir["evaluate_basis"]
        if isinstance(data, str):
            msg = "evaluate_reference_basis: %s" % data
            return generate_error(L, msg, parameters["convert_exceptions_to_warnings"])

        return generate_evaluate_reference_basis(L, data, parameters)

    def evaluate_reference_basis_derivatives(self, L, ir, parameters):
        data = ir["evaluate_basis"]
        if isinstance(data, str):
            msg = "evaluate_reference_basis_derivatives: %s" % data
            return generate_error(L, msg, parameters["convert_exceptions_to_warnings"])

        return generate_evaluate_reference_basis_derivatives(L, data, parameters)

    def transform_reference_basis_derivatives(self, L, ir, parameters):
        data = ir["evaluate_basis"]
        if isinstance(data, str):
            msg = "transform_reference_basis_derivatives: %s" % data
            return generate_error(L, msg, parameters["convert_exceptions_to_warnings"])

        # Get some known dimensions
        #element_cellname = data["cellname"]
        gdim = data["geometric_dimension"]
        tdim = data["topological_dimension"]
        max_degree = data["max_degree"]
        reference_value_size = data["reference_value_size"]
        physical_value_size = data["physical_value_size"]
        num_dofs = len(data["dofs_data"])

        max_g_d = gdim**max_degree
        max_t_d = tdim**max_degree

        # Output arguments
        values_symbol = L.Symbol("values")

        # Input arguments
        order = L.Symbol("order")
        num_points = L.Symbol("num_points")  # FIXME: Currently assuming 1 point?
        reference_values = L.Symbol("reference_values")
        J = L.Symbol("J")
        detJ = L.Symbol("detJ")
        K = L.Symbol("K")

        # Internal variables
        transform = L.Symbol("transform")

        # Indices, I've tried to use these for a consistent purpose
        ip = L.Symbol("ip") # point
        i = L.Symbol("i")   # physical component
        j = L.Symbol("j")   # reference component
        k = L.Symbol("k")   # order
        r = L.Symbol("r")   # physical derivative number
        s = L.Symbol("s")   # reference derivative number
        d = L.Symbol("d")   # dof

        combinations_code = []
        if max_degree == 0:
            # Don't need combinations
            num_derivatives_t = 1  # TODO: I think this is the right thing to do to make this still work for order=0?
            num_derivatives_g = 1
        elif tdim == gdim:
            num_derivatives_t = L.Symbol("num_derivatives")
            num_derivatives_g = num_derivatives_t
            combinations_code += [
                L.VariableDecl("const " + index_type, num_derivatives_t,
                               L.Call("pow", (tdim, order))),
            ]

            # Add array declarations of combinations
            combinations_code_t, combinations_t = _generate_combinations(L, tdim, max_degree, order, num_derivatives_t)
            combinations_code += combinations_code_t
            combinations_g = combinations_t
        else:
            num_derivatives_t = L.Symbol("num_derivatives_t")
            num_derivatives_g = L.Symbol("num_derivatives_g")
            combinations_code += [
                L.VariableDecl("const " + index_type, num_derivatives_t,
                               L.Call("pow", (tdim, order))),
                L.VariableDecl("const " + index_type, num_derivatives_g,
                               L.Call("pow", (gdim, order))),
            ]
            # Add array declarations of combinations
            combinations_code_t, combinations_t = _generate_combinations(L, tdim, max_degree, order, num_derivatives_t, suffix="_t")
            combinations_code_g, combinations_g = _generate_combinations(L, gdim, max_degree, order, num_derivatives_g, suffix="_g")
            combinations_code += combinations_code_t
            combinations_code += combinations_code_g

        # Define expected dimensions of argument arrays
        J = L.FlattenedArray(J, dims=(num_points, gdim, tdim))
        detJ = L.FlattenedArray(detJ, dims=(num_points,))
        K = L.FlattenedArray(K, dims=(num_points, tdim, gdim))

        values = L.FlattenedArray(values_symbol,
            dims=(num_points, num_dofs, num_derivatives_g, physical_value_size))
        reference_values = L.FlattenedArray(reference_values,
            dims=(num_points, num_dofs, num_derivatives_t, reference_value_size))

        # Generate code to compute the derivative transform matrix
        transform_matrix_code = [
            # Initialize transform matrix to all 1.0
            L.ArrayDecl("double", transform, (max_g_d, max_t_d)),
            L.ForRanges(
                (r, 0, num_derivatives_g),
                (s, 0, num_derivatives_t),
                index_type=index_type,
                body=L.Assign(transform[r, s], 1.0)
            ),
            ]
        if max_degree > 0:
            transform_matrix_code += [
                # Compute transform matrix entries, each a product of K entries
                L.ForRanges(
                    (r, 0, num_derivatives_g),
                    (s, 0, num_derivatives_t),
                    (k, 0, order),
                    index_type=index_type,
                    body=L.AssignMul(transform[r, s],
                                     K[ip, combinations_t[s, k], combinations_g[r, k]])
                ),
            ]

        # Initialize values to 0, will be added to inside loops
        values_init_code = [
            L.MemZero(values_symbol, num_points * num_dofs * num_derivatives_g * physical_value_size),
            ]

        # Make offsets available in generated code
        reference_offsets = L.Symbol("reference_offsets")
        physical_offsets = L.Symbol("physical_offsets")
        dof_attributes_code = [
            L.ArrayDecl("const " + index_type, reference_offsets, (num_dofs,),
                        values=[dof_data["reference_offset"] for dof_data in data["dofs_data"]]),
            L.ArrayDecl("const " + index_type, physical_offsets, (num_dofs,),
                        values=[dof_data["physical_offset"] for dof_data in data["dofs_data"]]),
            ]

        # Build dof lists for each mapping type
        mapping_dofs = defaultdict(list)
        for idof, dof_data in enumerate(data["dofs_data"]):
            mapping_dofs[dof_data["mapping"]].append(idof)

        # Generate code for each mapping type
        d = L.Symbol("d")
        transform_apply_code = []
        for mapping in sorted(mapping_dofs):
            # Get list of dofs using this mapping
            idofs = mapping_dofs[mapping]

            # Select iteration approach over dofs
            if idofs == list(range(idofs[0], idofs[-1]+1)):
                # Contiguous
                dofrange = (d, idofs[0], idofs[-1]+1)
                idof = d
            else:
                # Stored const array of dof indices
                idofs_symbol = L.Symbol("%s_dofs" % mapping.replace(" ", "_"))
                dof_attributes_code += [
                    L.ArrayDecl("const " + index_type, idofs_symbol,
                                (len(idofs),), values=idofs),
                ]
                dofrange = (d, 0, len(idofs))
                idof = idofs_symbol[d]

            # NB! Array access to offsets, these are not Python integers
            reference_offset = reference_offsets[idof]
            physical_offset = physical_offsets[idof]

            # How many components does each basis function with this mapping have?
            # This should be uniform, i.e. there should be only one element in this set:
            num_reference_components, = set(data["dofs_data"][i]["num_components"] for i in idofs)

            M_scale, M_row, num_physical_components = generate_element_mapping(
                mapping, i,
                num_reference_components, tdim, gdim,
                J[ip], detJ[ip], K[ip]
            )

#            transform_apply_body = [
#                L.AssignAdd(values[ip, idof, r, physical_offset + k],
#                            transform[r, s] * reference_values[ip, idof, s, reference_offset + k])
#                for k in range(num_physical_components)
#            ]

            msg = "Using %s transform to map values back to the physical element." % mapping.replace("piola", "Piola")

            mapped_value = L.Symbol("mapped_value")
            transform_apply_code += [
                L.ForRanges(
                    dofrange,
                    (s, 0, num_derivatives_t),
                    (i, 0, num_physical_components),
                    index_type=index_type, body=[
                        # Unrolled application of mapping to one physical component,
                        # for affine this automatically reduces to
                        #   mapped_value = reference_values[..., reference_offset]
                        L.Comment(msg),
                        L.VariableDecl("const double", mapped_value,
                                       M_scale * sum(M_row[jj] * reference_values[ip, idof, s, reference_offset + jj]
                                                     for jj in range(num_reference_components))),
                        # Apply derivative transformation, for order=0 this reduces to
                        # values[ip,idof,0,physical_offset+i] = transform[0,0]*mapped_value
                        L.Comment("Mapping derivatives back to the physical element"),
                        L.ForRanges(
                            (r, 0, num_derivatives_g),
                            index_type=index_type, body=[
                                L.AssignAdd(values[ip, idof, r, physical_offset + i],
                                            transform[r, s] * mapped_value)
                        ])
                ])
            ]

        # Transform for each point
        point_loop_code = [
            L.ForRange(ip, 0, num_points, index_type=index_type, body=(
                transform_matrix_code
                + transform_apply_code
            ))
        ]

        # Join code
        code = (
            combinations_code
            + values_init_code
            + dof_attributes_code
            + point_loop_code
        )
        return code


def _num_vertices(cell_shape):
    """Returns number of vertices for a given cell shape."""

    num_vertices_dict = {"interval": 2, "triangle": 3, "tetrahedron": 4, "quadrilateral": 4, "hexahedron": 8}
    return num_vertices_dict[cell_shape]
