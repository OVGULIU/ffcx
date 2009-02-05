"Code generator for quadrature representation"

__author__ = "Kristian B. Oelgaard (k.b.oelgaard@tudelft.nl)"
__date__ = "2007-03-16 -- 2008-09-08"
__copyright__ = "Copyright (C) 2007-2008 Kristian B. Oelgaard"
__license__  = "GNU GPL version 3 or any later version"

# Modified by Anders Logg 2007

# Python modules
from numpy import shape

from sets import Set

# FFC common modules
#from ffc.common.constants import *
#from ffc.common.utils import *
from ffc.common.debug import *

# FFC fem modules
from ffc.fem.finiteelement import FiniteElement as FIATFiniteElement
from ffc.fem.vectorelement import VectorElement as FIATVectorElement
from ffc.fem.mixedelement import MixedElement as FIATMixedElement

# FFC language modules
from ffc.compiler.language.integral import Integral as FFCIntegral
#from ffc.compiler.language.index import *
#from ffc.compiler.language.restriction import *

# FFC code generation modules
#from ffc.compiler.codegeneration.common.codegenerator import *
from ffc.compiler.codegeneration.common.utils import *
from ffc.compiler.codegeneration.common.evaluatebasis import IndentControl

# FFC tensor representation modules
#from ffc.compiler.representation.tensor.multiindex import *

# Utility and optimisation functions for quadraturegenerator
from quadraturegenerator_utils import *
#from quadraturegenerator_optimisation import *
#import reduce_operations

# FFC format modules
#from ffc.compiler.format.removeunused import *

# UFL modules
from ufl.classes import FiniteElement, MixedElement, VectorElement, FiniteElementBase
from ufl.algorithms.analysis import *

#class QuadratureGenerator(CodeGenerator):
class QuadratureGenerator:
    "Code generator for quadrature representation"

    def __init__(self):
        "Constructor"

        # Initialize common code generator
#        CodeGenerator.__init__(self)
        self.optimise_level = 2

    def generate_cell_integrals(self, form_representation, format):
        code = {}
        if not form_representation.cell_integrals:
            return code
        # Generate code for cell integral
        debug("Generating code for cell integrals using quadrature representation...")
        for integral in form_representation.cell_integrals:
            code[("cell_integral", integral.domain_id())] =\
                 self.generate_cell_integral(form_representation, integral, format)
        debug("done")
        return code

    def generate_exterior_facet_integrals(self, form_representation, format):
        code = {}
        if not form_representation.exterior_facet_integrals:
            return code
        # Generate code for cell integral
        debug("Generating code for exterior facet integrals using quadrature representation...")
        for integral in form_representation.exterior_facet_integrals:
            code[("cell_integral", integral.domain_id())] =\
                 self.generate_exterior_facet_integral(form_representation, integral, format)
        debug("done")
        return code

    def generate_interior_facet_integrals(self, form_representation, format):
        code = {}
        if not form_representation.interior_facet_integrals:
            return code
        # Generate code for cell integral
        debug("Generating code for interior facet integrals using quadrature representation...")
        for integral in form_representation.interior_facet_integrals:
            code[("cell_integral", integral.domain_id())] =\
                 self.generate_interior_facet_integral(form_representation, integral, format)
        debug("done")
        return code

    def generate_cell_integral(self, form_representation, integral, format):
        """Generate dictionary of code for cell integral from the given
        form representation according to the given format"""

        code = []


        # Object to control the code indentation
        Indent = IndentControl()

        debug("")
        code += self.__reset_element_tensor(integral, Indent, format)
        print "integral: ", integral
        print "integral: ", integral.__repr__()
        print extract_basisfunctions(integral)

#        # Generate element code + set of used geometry terms
#        element_code, members_code, trans_set, num_ops = self.__generate_element_tensor\
#                                                     (tensors, None, None, Indent, format)

        # Get Jacobian snippet
        # FIXME: This will most likely have to change if we support e.g., 2D elements in 3D space
        jacobi_code = [format["generate jacobian"](form_representation.geometric_dimension, FFCIntegral.CELL)]
        code += jacobi_code

#        # Remove unused declarations
#        code = self.__remove_unused(jacobi_code, trans_set, format)

#        # Add element code
#        code += ["", format["comment"]("Compute element tensor (using quadrature representation, optimisation level %d)" % self.optimise_level),\
#                 format["comment"]("Total number of operations to compute element tensor (from this point): %d" %num_ops)]
#        code += element_code
        debug("Number of operations to compute tensor: ")

#        return {"tabulate_tensor": code, "members":members_code}
        return {"tabulate_tensor": code, "members":[]}

    def generate_exterior_facet_integral(self, form_representation, sub_domain, format):
        """Generate dictionary of code for exterior facet integral from the given
        form representation according to the given format"""

#        # Object to control the code indentation
#        Indent = IndentControl()

#        # Prefetch formats to speed up code generation
#        format_comment      = format["comment"]
#        format_block_begin  = format["block begin"]
#        format_block_end    = format["block end"]

#        # Extract terms for sub domain
#        tensors = [[term for term in t if term.monomial.integral.sub_domain == sub_domain]\
#                    for t in form_representation.exterior_facet_tensors]
#        if all([len(t) == 0 for t in tensors]):
#            element_code = self.__reset_element_tensor(form_representation.exterior_facet_tensors[0][0], Indent, format)
#            return {"tabulate_tensor": (element_code, []), "members": ""}

#        num_facets = len(tensors)
#        cases = [None for i in range(num_facets)]
#        trans_set = Set()

#        debug("")
#        for i in range(num_facets):
#            case = [format_block_begin]

#            # Assuming all tables have same dimensions for all facets (members_code)
#            c, members_code, t_set, num_ops = self.__generate_element_tensor(tensors[i], i, None, Indent, format)
#            case += [format_comment("Total number of operations to compute element tensor (from this point): %d" %num_ops)] + c
#            case += [format_block_end]
#            cases[i] = case
#            trans_set = trans_set | t_set
#            debug("Number of operations to compute tensor for facet %d: %d" % (i, num_ops))


#        # Get Jacobian snippet
#        jacobi_code = [format["generate jacobian"](form_representation.cell_dimension, Integral.EXTERIOR_FACET)]

#        # Remove unused declarations
#        common = self.__remove_unused(jacobi_code, trans_set, format)

#        # Add element code
#        common += ["", format_comment("Compute element tensor for all facets (using quadrature representation, optimisation level %d)" %self.optimise_level)]

#        return {"tabulate_tensor": (common, cases), "constructor":"// Do nothing", "members":members_code}
        return {"tabulate_tensor": ([], []), "constructor":"// Do nothing", "members":[]}
    
    def generate_interior_facet_integral(self, form_representation, sub_domain, format):
        """Generate dictionary of code for interior facet integral from the given
        form representation according to the given format"""

#        # Object to control the code indentation
#        Indent = IndentControl()

#        # Prefetch formats to speed up code generation
#        format_comment      = format["comment"]
#        format_block_begin  = format["block begin"]
#        format_block_end    = format["block end"]

#        # Extract terms for sub domain
#        tensors = [[[term for term in t2 if term.monomial.integral.sub_domain == sub_domain] for t2 in t1] for t1 in form_representation.interior_facet_tensors]
#        if all([len(t) == 0 for tt in tensors for t in tt]):
#            element_code = self.__reset_element_tensor(form_representation.interior_facet_tensors[0][0][0], Indent, format)
#            return {"tabulate_tensor": (element_code, []), "members": ""}

#        num_facets = len(tensors)
#        cases = [[None for j in range(num_facets)] for i in range(num_facets)]
#        trans_set = Set()

#        debug("")
#        for i in range(num_facets):
#            for j in range(num_facets):
#                case = [format_block_begin]

#                # Assuming all tables have same dimensions for all facet-facet combinations (members_code)
#                c, members_code, t_set, num_ops = self.__generate_element_tensor(tensors[i][j], i, j, Indent, format)
#                case += [format_comment("Total number of operations to compute element tensor (from this point): %d" %num_ops)] + c
#                case += [format_block_end]
#                cases[i][j] = case
#                trans_set = trans_set | t_set
#                debug("Number of operations to compute tensor for facets (%d, %d): %d" % (i, j, num_ops))

#        # Get Jacobian snippet
#        jacobi_code = [format["generate jacobian"](form_representation.cell_dimension, Integral.INTERIOR_FACET)]

#        # Remove unused declarations
#        common = self.__remove_unused(jacobi_code, trans_set, format)

#        # Add element code
#        common += ["", format_comment("Compute element tensor for all facets (using quadrature representation, optimisation level %d)" %self.optimise_level)]

#        return {"tabulate_tensor": (common, cases), "constructor":"// Do nothing", "members":members_code}
        return {"tabulate_tensor": ([], []), "constructor":"// Do nothing", "members":[]}

    def __generate_element_tensor(self, tensors, facet0, facet1, Indent, format):
        "Construct quadrature code for element tensors"

        # Prefetch formats to speed up code generation
        format_comment      = format["comment"]
        format_ip           = format["integration points"]
        format_G            = format["geometry tensor"]
        format_const_float  = format["const float declaration"]
        exp_ops   = reduce_operations.expand_operations
        red_ops   = reduce_operations.reduce_operations
        count_ops = reduce_operations.operation_count

        # Generate load_table.h if tables should be saved. (Not reimplemented)
        members_code = ""

        # Reset values of the element tensor
        # FIXME: assuming same dimensions for all tensors
        tabulate_code = []
        tabulate_code += self.__reset_element_tensor(tensors[0], Indent, format)

        # Tabulate weights at quadrature points, get name-map if some tables
        # are redundant
        weight_name_map, weight_tables = unique_weight_tables(tensors, format)
        tabulate_code += self.__tabulate_weights(weight_tables, weight_name_map,\
                                                 Indent, format)

        # Tabulate values of basis functions and their derivatives at
        # quadrature points, get dictionary of unique tables, and the name_map
        psi_name_map, psi_tables = unique_psi_tables(tensors,\
                                                     self.optimise_level, format)
        tabulate_code += self.__tabulate_psis(psi_tables, psi_name_map,\
                                              Indent, format)

        # Group tensors according to number of quadrature points in order to
        # reduce the number of loops
        group_tensors = equal_loops(tensors)

        # Some variables
        element_code = []
        trans_set = Set()
        geo_terms = {}
        tensor_ops_count = 0

        # Generate code to evaluate tensor
        # Loop all quadrature points
        for points in group_tensors:
            # Continue if we don't have any quadrature points
            if not points:
                continue
            # Create list of tensors for comment
            ts = group_tensors[points]
            ip_code = [Indent.indent(format_comment\
            ("Loop quadrature points (tensor/monomial terms %s)" %(str(tuple(ts))))) ]

            # Generate all terms for the given number of quadrature points
            terms, t_set = generate_terms(points, group_tensors[points], tensors, format, psi_name_map,
                                          weight_name_map, self.optimise_level)
            # Update transformation set
            trans_set = trans_set | t_set

            # Generate code for all terms according to optimisation level
            terms_code, num_ops = generate_code(terms, geo_terms, self.optimise_level, Indent, format)

            # Get number of operations to compute entries for all terms when
            # looping over all IPs and update tensor count
            num_operations = num_ops*points
            tensor_ops_count += num_operations

            ip_code.append(format_comment\
                ("Number of operations to compute element tensor for following IP loop = %d" %(num_operations)) )

            # Loop code over all IPs
            if points > 1:
                ip_code += generate_loop(terms_code, [(format_ip, 0, points)], Indent, format)
            else:
                ip_code.append(format_comment("Only 1 integration point, omitting IP loop."))
                ip_code += terms_code

            # Add integration point code element code
            element_code += ip_code

        # Tabulate geometry code, sort according to number
        geo_code = []
        items = geo_terms.items()
        items = [(int(v.replace(format_G, "")), k) for (k, v) in items]
        items.sort()
        items = [(k, format_G + str(v)) for (v, k) in items]
        geo_ops = 0
        for key, val in items:
            declaration = red_ops(exp_ops(key, format), format)
            # Get number of operations needed to compute geometry declaration
            geo_ops += count_ops(declaration, format)
            geo_code += [(format_const_float + val, declaration)]
        geo_code.append("")
        if geo_ops:
            geo_code = ["", format_comment("Number of operations to compute geometry constants = %d" % geo_ops)] + geo_code
        else:
            geo_code = [""] + geo_code

        # Add operation count
        tensor_ops_count += geo_ops

        element_code = geo_code + element_code

        return (tabulate_code + element_code, members_code,\
                trans_set, tensor_ops_count)


    def __tabulate_weights(self, tables, name_map, Indent, format):
        "Generate table of quadrature weights"
        
        # Prefetch formats to speed up code generation
        format_comment  = format["comment"]
        format_float    = format["floating point"]
        format_table    = format["table declaration"]
        format_block    = format["block"]
        format_sep      = format["separator"]
        format_weight   = format["weight"]
        format_array    = format["array access"]

        code = []

        # Loop tables of weights and create code
        for tensor_number, weights in tables.items():

            # Continue if we don't have any weights
            if not weights.any():
                continue

            # Create name and value
            name = format_table + format_weight(tensor_number)
            value = format_float(weights[0])
            if len(weights) > 1:
                name += format_array(str(len(weights)))
                value = format_block(format_sep.join([format_float(w)\
                                                      for w in weights]))

            if tensor_number in name_map:
                # Get the list of tensors that this weight is valid for
                tw = [tensor_number] + name_map[tensor_number]
                tw.sort()
                code += [Indent.indent(format_comment\
                    ("Array of quadrature weights (tensor/monomial terms %s)"\
                      %(str(tuple(tw)))))]
            else:
                code += [Indent.indent(format_comment\
                    ("Array of quadrature weights (tensor/monomial term %d)"\
                      %(tensor_number,) ))]

            code += [(Indent.indent(name), value)]

        return code

    def __tabulate_psis(self, tables, inv_name_map, Indent, format):
        "Tabulate values of basis functions and their derivatives at quadrature points"

        # Prefetch formats to speed up code generation
        format_comment    = format["comment"]
        format_float      = format["floating point"]
        format_block      = format["block"]
        format_table      = format["table declaration"]
        format_matrix     = format["matrix access"]
        format_array      = format["array access"]
        format_const_uint = format["static const uint declaration"]
        format_nzcolumns  = format["nonzero columns"]
        format_sep        = format["separator"]

        code = []

        # Get list of non zero columns with more than 1 column
        nzcs = [val[1] for key, val in inv_name_map.items()\
                                       if val[1] and len(val[1][1]) > 1]
        new_nzcs = []
        for nz in nzcs:
            # Only get unique arrays
            if not nz in new_nzcs:
                new_nzcs.append(nz)

        # Construct name map
        name_map = {}
        if inv_name_map:
            for name in inv_name_map:
                if inv_name_map[name][0] in name_map:
                    name_map[inv_name_map[name][0]].append(name)
                else:
                    name_map[inv_name_map[name][0]] = [name]

        # Loop items in table and tabulate 
        for name, vals in tables.items():
            # Only proceed if values are still used (if they're not remapped)
            if not vals == None:
                # Add declaration to name
                ip, dofs = shape(vals)
                decl_name = format_table + name + format_matrix(ip, dofs)

                # Generate array of values
                value = tabulate_matrix(vals, format)
                code += ["", (Indent.indent(decl_name), Indent.indent(value))]

            # Tabulate non-zero indices
            if self.optimise_level >= 1:
                if name in name_map:
                    for n in name_map[name]:
                        if inv_name_map[n][1] and inv_name_map[n][1] in new_nzcs:
                            code += [Indent.indent(format_comment("Array of non-zero columns") )]
                            i, cols = inv_name_map[n][1]
                            value = format_block(format_sep.join(["%d" %c for c in list(cols)]))
                            name_col = format_const_uint + format_nzcolumns(i) + format_array(len(cols))
                            code += [(Indent.indent(name_col), value)]
                            # Remove from list of columns
                            new_nzcs.remove(inv_name_map[n][1])

        # Tabulate remaining non-zero columns for tables that might have been deleted
        new_nzcs = [nz for nz in new_nzcs if nz and len(nz[1]) > 1]
        if self.optimise_level >= 1 and new_nzcs:
            code += [Indent.indent(format_comment("Array of non-zero columns for arrays that might have been deleted (on purpose)") )]
            for i, cols in new_nzcs:
                value = format_block(format_sep.join(["%d" %c for c in list(cols)]))
                name_col = format_const_uint + format_nzcolumns(i) + format_array(len(cols))
                code += [(Indent.indent(name_col), value)]

        return code

    def __reset_element_tensor(self, integral, Indent, format):
        "Reset the entries of the local element tensor"

        code = [""]

        # Comment
        code.append(Indent.indent(format["comment"]\
                ("Reset values of the element tensor block")))

        # Get basisfunctions
        basis = extract_basisfunctions(integral)

        # Create FIAT elements for each basisfunction. There should be one and
        # only one element per basisfunction so it is OK to pick first.
        elements = [self.__create_fiat_elements(extract_elements(b)[0]) for b in basis]

        # Create the index range for resetting the element tensor by
        # multiplying the element space dimensions
        index_range = 1
        for element in elements:
            index_range *= element.space_dimension()

        # Create loop
        # FIXME: It is general to create a loop, however, for a functional it
        # is not strictly needed. On the other hand, it is not expected to have
        # any influence on the runtime performance.
        value = format["floating point"](0.0)
        name =  format["element tensor quad"] + format["array access"](format["first free index"])
        lines = [(name, value)]
        code += generate_loop(lines, [(format["first free index"], 0, index_range)], Indent, format)
        code.append("")

        return code

    def __create_fiat_elements(self, ufl_e):

        if isinstance(ufl_e, VectorElement):
            print "Vector"
            return FIATVectorElement(ufl_e.family(), ufl_e.cell().domain(), ufl_e.degree(), len(ufl_e.sub_elements()))
        elif isinstance(ufl_e, MixedElement):
            print "Mixed"
            sub_elems = [self.__create_fiat_elements(e) for e in ufl_e.sub_elements()]
            return FIATMixedElement(sub_elems)
        elif isinstance(ufl_e, FiniteElement):
            print "Finite"
            return FIATFiniteElement(ufl_e.family(), ufl_e.cell().domain(), ufl_e.degree())
        # Element type not supported (yet?) TensorElement will trigger this.
        else:
            raise RuntimeError(ufl_e, "Unable to create equivalent FIAT element.")
        return

    def __remove_unused(self, code, set, format):
        "Remove unused variables so that the compiler will not complain"

        # Normally, the removal of unused variables should happen at the
        # formatting stage, but since the code for the tabulate_tensor()
        # function may grow to considerable size, we make an exception and
        # remove unused variables here when we know the names of the used
        # variables. No searching necessary and much, much, much faster.

        if code:
            # Generate body of code, using the format
            lines = format["generate body"](code)

            # Generate auxiliary code line that uses all members of the set
            # (to trick remove_unused)
            line_set = format["add equal"]("A", format["multiply"](set))
            lines += "\n" + line_set

            # Remove unused Jacobi declarations
            code = remove_unused(lines)

            # Delete auxiliary line
            code = code.replace("\n" + line_set, "")

            return [code]
        else:
            return code

