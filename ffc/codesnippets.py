"Code snippets for code generation."

# Copyright (C) 2007 Anders Logg
#
# This file is part of FFC.
#
# FFC is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FFC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with FFC. If not, see <http://www.gnu.org/licenses/>.
#
# Modified by Kristian B. Oelgaard 2010-2011
# Modified by Marie Rognes 2007-2012
# Modified by Peter Brune 2009
#
# First added:  2007-02-28
# Last changed: 2011-11-22

# Code snippets

__all__ = ["comment_ufc", "comment_dolfin", "header_h", "header_c", "footer",
           "cell_coordinates", "jacobian", "inverse_jacobian",
           "evaluate_f",
           "facet_determinant", "map_onto_physical",
           "fiat_coordinate_map", "transform_snippet",
           "scale_factor", "combinations_snippet",
           "normal_direction",
           "facet_normal", "ip_coordinates", "cell_volume", "circumradius",
           "facet_area",
           "orientation_snippet"]

comment_ufc = """\
// This code conforms with the UFC specification version %(ufc_version)s
// and was automatically generated by FFC version %(ffc_version)s.
"""

comment_dolfin = """\
// This code conforms with the UFC specification version %(ufc_version)s
// and was automatically generated by FFC version %(ffc_version)s.
//
// This code was generated with the option '-l dolfin' and
// contains DOLFIN-specific wrappers that depend on DOLFIN.
"""

header_h = """\
#ifndef __%(prefix_upper)s_H
#define __%(prefix_upper)s_H

#include <cmath>
#include <stdexcept>
#include <fstream>
#include <ufc.h>
"""

header_c = """\
#include "%(prefix)s.h"
"""

footer = """\
#endif
"""

cell_coordinates = "const double * const * x = c.coordinates;\n"

# Code snippets for computing Jacobian
_jacobian_1D = """\
// Extract vertex coordinates
const double * const * x%(restriction)s = c%(restriction)s.coordinates;

// Compute Jacobian of affine map from reference cell
const double J%(restriction)s_00 = x%(restriction)s[1][0] - x%(restriction)s[0][0];"""

_jacobian_2D = """\
// Extract vertex coordinates
const double * const * x%(restriction)s = c%(restriction)s.coordinates;

// Compute Jacobian of affine map from reference cell
const double J%(restriction)s_00 = x%(restriction)s[1][0] - x%(restriction)s[0][0];
const double J%(restriction)s_01 = x%(restriction)s[2][0] - x%(restriction)s[0][0];
const double J%(restriction)s_10 = x%(restriction)s[1][1] - x%(restriction)s[0][1];
const double J%(restriction)s_11 = x%(restriction)s[2][1] - x%(restriction)s[0][1];"""

_jacobian_2D_1D = """\
// Geometric dimension 2, topological dimension 1

// Extract vertex coordinates
const double * const * x%(restriction)s = c%(restriction)s.coordinates;

// Compute Jacobian of affine map from reference cell
const double J%(restriction)s_00 = x%(restriction)s[1][0] - x%(restriction)s[0][0];
const double J%(restriction)s_10 = x%(restriction)s[1][1] - x%(restriction)s[0][1];
"""

_jacobian_3D = """\
// Extract vertex coordinates
const double * const * x%(restriction)s = c%(restriction)s.coordinates;

// Compute Jacobian of affine map from reference cell
const double J%(restriction)s_00 = x%(restriction)s[1][0] - x%(restriction)s[0][0];
const double J%(restriction)s_01 = x%(restriction)s[2][0] - x%(restriction)s[0][0];
const double J%(restriction)s_02 = x%(restriction)s[3][0] - x%(restriction)s[0][0];
const double J%(restriction)s_10 = x%(restriction)s[1][1] - x%(restriction)s[0][1];
const double J%(restriction)s_11 = x%(restriction)s[2][1] - x%(restriction)s[0][1];
const double J%(restriction)s_12 = x%(restriction)s[3][1] - x%(restriction)s[0][1];
const double J%(restriction)s_20 = x%(restriction)s[1][2] - x%(restriction)s[0][2];
const double J%(restriction)s_21 = x%(restriction)s[2][2] - x%(restriction)s[0][2];
const double J%(restriction)s_22 = x%(restriction)s[3][2] - x%(restriction)s[0][2];"""

_jacobian_3D_2D = """\
// Geometric dimension 3, topological dimension 2

// Extract vertex coordinates
const double * const * x%(restriction)s = c%(restriction)s.coordinates;

// Compute Jacobian of affine map from reference cell
const double J%(restriction)s_00 = x%(restriction)s[1][0] - x%(restriction)s[0][0];
const double J%(restriction)s_01 = x%(restriction)s[2][0] - x%(restriction)s[0][0];
const double J%(restriction)s_10 = x%(restriction)s[1][1] - x%(restriction)s[0][1];
const double J%(restriction)s_11 = x%(restriction)s[2][1] - x%(restriction)s[0][1];
const double J%(restriction)s_20 = x%(restriction)s[1][2] - x%(restriction)s[0][2];
const double J%(restriction)s_21 = x%(restriction)s[2][2] - x%(restriction)s[0][2];"""

_jacobian_3D_1D = """\
// Geometric dimension 3, topological dimension 1

// Extract vertex coordinates
const double * const * x%(restriction)s = c%(restriction)s.coordinates;

// Compute Jacobian of affine map from reference cell
const double J%(restriction)s_00 = x%(restriction)s[1][0] - x%(restriction)s[0][0];
const double J%(restriction)s_10 = x%(restriction)s[1][1] - x%(restriction)s[0][1];
const double J%(restriction)s_20 = x%(restriction)s[1][2] - x%(restriction)s[0][2];"""

# Code snippets for computing the inverse Jacobian. Assumes that
# Jacobian is already initialized
_inverse_jacobian_1D = """\

// Compute determinant of Jacobian
const double detJ%(restriction)s = J%(restriction)s_00;

// Compute inverse of Jacobian
const double K%(restriction)s_00 =  1.0 / detJ%(restriction)s;"""

_inverse_jacobian_2D = """\

// Compute determinant of Jacobian
const double detJ%(restriction)s = J%(restriction)s_00*J%(restriction)s_11 - J%(restriction)s_01*J%(restriction)s_10;

// Compute inverse of Jacobian
const double K%(restriction)s_00 =  J%(restriction)s_11 / detJ%(restriction)s;
const double K%(restriction)s_01 = -J%(restriction)s_01 / detJ%(restriction)s;
const double K%(restriction)s_10 = -J%(restriction)s_10 / detJ%(restriction)s;
const double K%(restriction)s_11 =  J%(restriction)s_00 / detJ%(restriction)s;"""

_inverse_jacobian_2D_1D = """\

// Compute pseudodeterminant of Jacobian
const double detJ2%(restriction)s = J%(restriction)s_00*J%(restriction)s_00 + J%(restriction)s_10*J%(restriction)s_10;
const double detJ%(restriction)s = std::sqrt(detJ2%(restriction)s);

// Compute pseudoinverse of Jacobian
const double K%(restriction)s_00 = J%(restriction)s_00 / detJ2%(restriction)s;
const double K%(restriction)s_01 = J%(restriction)s_10 / detJ2%(restriction)s;"""

_inverse_jacobian_3D = """\

// Compute sub determinants
const double d%(restriction)s_00 = J%(restriction)s_11*J%(restriction)s_22 - J%(restriction)s_12*J%(restriction)s_21;
const double d%(restriction)s_01 = J%(restriction)s_12*J%(restriction)s_20 - J%(restriction)s_10*J%(restriction)s_22;
const double d%(restriction)s_02 = J%(restriction)s_10*J%(restriction)s_21 - J%(restriction)s_11*J%(restriction)s_20;
const double d%(restriction)s_10 = J%(restriction)s_02*J%(restriction)s_21 - J%(restriction)s_01*J%(restriction)s_22;
const double d%(restriction)s_11 = J%(restriction)s_00*J%(restriction)s_22 - J%(restriction)s_02*J%(restriction)s_20;
const double d%(restriction)s_12 = J%(restriction)s_01*J%(restriction)s_20 - J%(restriction)s_00*J%(restriction)s_21;
const double d%(restriction)s_20 = J%(restriction)s_01*J%(restriction)s_12 - J%(restriction)s_02*J%(restriction)s_11;
const double d%(restriction)s_21 = J%(restriction)s_02*J%(restriction)s_10 - J%(restriction)s_00*J%(restriction)s_12;
const double d%(restriction)s_22 = J%(restriction)s_00*J%(restriction)s_11 - J%(restriction)s_01*J%(restriction)s_10;

// Compute determinant of Jacobian
const double detJ%(restriction)s = J%(restriction)s_00*d%(restriction)s_00 + J%(restriction)s_10*d%(restriction)s_10 + J%(restriction)s_20*d%(restriction)s_20;

// Compute inverse of Jacobian
const double K%(restriction)s_00 = d%(restriction)s_00 / detJ%(restriction)s;
const double K%(restriction)s_01 = d%(restriction)s_10 / detJ%(restriction)s;
const double K%(restriction)s_02 = d%(restriction)s_20 / detJ%(restriction)s;
const double K%(restriction)s_10 = d%(restriction)s_01 / detJ%(restriction)s;
const double K%(restriction)s_11 = d%(restriction)s_11 / detJ%(restriction)s;
const double K%(restriction)s_12 = d%(restriction)s_21 / detJ%(restriction)s;
const double K%(restriction)s_20 = d%(restriction)s_02 / detJ%(restriction)s;
const double K%(restriction)s_21 = d%(restriction)s_12 / detJ%(restriction)s;
const double K%(restriction)s_22 = d%(restriction)s_22 / detJ%(restriction)s;"""

_inverse_jacobian_3D_2D = """\

// Compute pseudodeterminant of Jacobian
const double d%(restriction)s_0 = J_10*J_21 - J_20*J_11;
const double d%(restriction)s_1 = - (J_00*J_21 - J_20*J_01);
const double d%(restriction)s_2 = J_00*J_11 - J_10*J_01;

const double detJ2%(restriction)s = d%(restriction)s_0*d%(restriction)s_0 + d%(restriction)s_1*d%(restriction)s_1 + d%(restriction)s_2*d%(restriction)s_2;
double detJ%(restriction)s = std::sqrt(detJ2%(restriction)s);

// Compute some common factors for the pseudoinverse
const double n%(restriction)s_1 = J%(restriction)s_00*J%(restriction)s_00 + J%(restriction)s_10*J%(restriction)s_10 + J%(restriction)s_20*J%(restriction)s_20;
const double n%(restriction)s_2 = J%(restriction)s_01*J%(restriction)s_01 + J%(restriction)s_11*J%(restriction)s_11 + J%(restriction)s_21*J%(restriction)s_21;
const double m%(restriction)s  = J%(restriction)s_00*J%(restriction)s_01 + J%(restriction)s_10*J%(restriction)s_11 + J%(restriction)s_20*J%(restriction)s_21;
const double den%(restriction)s = n%(restriction)s_1*n%(restriction)s_2 - m%(restriction)s*m%(restriction)s;

// Compute pseudoinverse of Jacobian
const double K%(restriction)s_00 =  (J%(restriction)s_00*n%(restriction)s_2 - J%(restriction)s_01*m%(restriction)s)/den%(restriction)s;
const double K%(restriction)s_01 =  (J%(restriction)s_10*n%(restriction)s_2 - J%(restriction)s_11*m%(restriction)s)/den%(restriction)s;
const double K%(restriction)s_02 =  (J%(restriction)s_20*n%(restriction)s_2 - J%(restriction)s_21*m%(restriction)s)/den%(restriction)s;
const double K%(restriction)s_10 = (-J%(restriction)s_00*m%(restriction)s + J%(restriction)s_01*n%(restriction)s_1)/den%(restriction)s;
const double K%(restriction)s_11 = (-J%(restriction)s_10*m%(restriction)s + J%(restriction)s_11*n%(restriction)s_1)/den%(restriction)s;
const double K%(restriction)s_12 = (-J%(restriction)s_20*m%(restriction)s + J%(restriction)s_21*n%(restriction)s_1)/den%(restriction)s;
"""

orientation_snippet = """
// Extract orientation
const int orientation_marker = c.orientation;
if (orientation_marker == 0)
  throw std::runtime_error("cell orientation must be defined (not 0)");
// (If orientation_marker == 1 = down, multiply detJ by -1)
else if (orientation_marker == 1)
  detJ%(restriction)s *= -1;
"""

_inverse_jacobian_3D_1D = """\

// Compute pseudodeterminant of Jacobian
const double detJ2%(restriction)s = J%(restriction)s_00*J%(restriction)s_00 + J%(restriction)s_10*J%(restriction)s_10 + J%(restriction)s_20*J%(restriction)s_20;
const double detJ%(restriction)s = std::sqrt(detJ2%(restriction)s);

// Compute pseudoinverse of Jacobian
const double K%(restriction)s_00 = J%(restriction)s_00 / detJ2%(restriction)s;
const double K%(restriction)s_01 = J%(restriction)s_10 / detJ2%(restriction)s;
const double K%(restriction)s_02 = J%(restriction)s_20 / detJ2%(restriction)s;"""

evaluate_f = "f.evaluate(vals, y, c);"

scale_factor = """\
// Set scale factor
const double det = std::abs(detJ);"""

_facet_determinant_1D = """\
// Facet determinant 1D (vertex)
const double det = 1.0;"""

_facet_determinant_2D = """\
// Get vertices on edge
static unsigned int edge_vertices[3][2] = {{1, 2}, {0, 2}, {0, 1}};
const unsigned int v0 = edge_vertices[facet%(restriction)s][0];
const unsigned int v1 = edge_vertices[facet%(restriction)s][1];

// Compute scale factor (length of edge scaled by length of reference interval)
const double dx0 = x%(restriction)s[v1][0] - x%(restriction)s[v0][0];
const double dx1 = x%(restriction)s[v1][1] - x%(restriction)s[v0][1];
const double det = std::sqrt(dx0*dx0 + dx1*dx1);"""

_facet_determinant_2D_1D = """\
// Facet determinant 1D in 2D (vertex)
const double det = 1.0;"""

_facet_determinant_3D = """\
// Get vertices on face
static unsigned int face_vertices[4][3] = {{1, 2, 3}, {0, 2, 3}, {0, 1, 3}, {0, 1, 2}};
const unsigned int v0 = face_vertices[facet%(restriction)s][0];
const unsigned int v1 = face_vertices[facet%(restriction)s][1];
const unsigned int v2 = face_vertices[facet%(restriction)s][2];

// Compute scale factor (area of face scaled by area of reference triangle)
const double a0 = (x%(restriction)s[v0][1]*x%(restriction)s[v1][2] + x%(restriction)s[v0][2]*x%(restriction)s[v2][1] + x%(restriction)s[v1][1]*x%(restriction)s[v2][2]) - (x%(restriction)s[v2][1]*x%(restriction)s[v1][2] + x%(restriction)s[v2][2]*x%(restriction)s[v0][1] + x%(restriction)s[v1][1]*x%(restriction)s[v0][2]);

const double a1 = (x%(restriction)s[v0][2]*x%(restriction)s[v1][0] + x%(restriction)s[v0][0]*x%(restriction)s[v2][2] + x%(restriction)s[v1][2]*x%(restriction)s[v2][0]) - (x%(restriction)s[v2][2]*x%(restriction)s[v1][0] + x%(restriction)s[v2][0]*x%(restriction)s[v0][2] + x%(restriction)s[v1][2]*x%(restriction)s[v0][0]);

const double a2 = (x%(restriction)s[v0][0]*x%(restriction)s[v1][1] + x%(restriction)s[v0][1]*x%(restriction)s[v2][0] + x%(restriction)s[v1][0]*x%(restriction)s[v2][1]) - (x%(restriction)s[v2][0]*x%(restriction)s[v1][1] + x%(restriction)s[v2][1]*x%(restriction)s[v0][0] + x%(restriction)s[v1][0]*x%(restriction)s[v0][1]);

const double det = std::sqrt(a0*a0 + a1*a1 + a2*a2);"""

_facet_determinant_3D_2D = """\
// Facet determinant 2D in 3D (edge)
// Get vertices on edge
static unsigned int edge_vertices[3][2] = {{1, 2}, {0, 2}, {0, 1}};
const unsigned int v0 = edge_vertices[facet%(restriction)s][0];
const unsigned int v1 = edge_vertices[facet%(restriction)s][1];

// Compute scale factor (length of edge scaled by length of reference interval)
const double dx0 = x%(restriction)s[v1][0] - x%(restriction)s[v0][0];
const double dx1 = x%(restriction)s[v1][1] - x%(restriction)s[v0][1];
const double dx2 = x%(restriction)s[v1][2] - x%(restriction)s[v0][2];
const double det = std::sqrt(dx0*dx0 + dx1*dx1 + dx2*dx2);"""

_facet_determinant_3D_1D = """\
// Facet determinant 1D in 3D (vertex)
const double det = 1.0;"""

_normal_direction_1D = """\
const bool direction = facet%(restriction)s == 0 ? x%(restriction)s[0][0] > x%(restriction)s[1][0] : x%(restriction)s[1][0] > x%(restriction)s[0][0];"""

_normal_direction_2D = """\
const bool direction = dx1*(x%(restriction)s[%(facet)s][0] - x%(restriction)s[v0][0]) - dx0*(x%(restriction)s[%(facet)s][1] - x%(restriction)s[v0][1]) < 0;"""

_normal_direction_3D = """\
const bool direction = a0*(x%(restriction)s[%(facet)s][0] - x%(restriction)s[v0][0]) + a1*(x%(restriction)s[%(facet)s][1] - x%(restriction)s[v0][1])  + a2*(x%(restriction)s[%(facet)s][2] - x%(restriction)s[v0][2]) < 0;"""

# MER: Coding all up in _facet_normal_ND_M_D for now; these are
# therefore empty.
_normal_direction_2D_1D = ""
_normal_direction_3D_2D = ""
_normal_direction_3D_1D = ""

_facet_normal_1D = """
// Facet normals are 1.0 or -1.0:   (-1.0) <-- X------X --> (1.0)
const double n%(restriction)s = %(direction)sdirection ? 1.0 : -1.0;"""

_facet_normal_2D = """\
// Compute facet normals from the facet scale factor constants
const double n%(restriction)s0 = %(direction)sdirection ? dx1 / det : -dx1 / det;
const double n%(restriction)s1 = %(direction)sdirection ? -dx0 / det : dx0 / det;"""

_facet_normal_2D_1D = """
// Compute facet normal
double n%(restriction)s0 = 0.0;
double n%(restriction)s1 = 0.0;
if (facet%(restriction)s == 0)
{
  n%(restriction)s0 = x[0][0] - x[1][0];
  n%(restriction)s1 = x[0][1] - x[1][1];
} else {
  n%(restriction)s0 = x[1][0] - x[0][0];
  n%(restriction)s1 = x[1][1] - x[0][1];
}
const double length = std::sqrt(n%(restriction)s0*n%(restriction)s0 + n%(restriction)s1*n%(restriction)s1);
n%(restriction)s0 /= length;
n%(restriction)s1 /= length;
"""

_facet_normal_3D = """\
// Compute facet normals from the facet scale factor constants
const double n%(restriction)s0 = %(direction)sdirection ? a0 / det : -a0 / det;
const double n%(restriction)s1 = %(direction)sdirection ? a1 / det : -a1 / det;
const double n%(restriction)s2 = %(direction)sdirection ? a2 / det : -a2 / det;"""

_facet_normal_3D_2D = """
// Compute facet normal n via Rodrigues' rotation formula:
//   n = k x e  + k (k . e)
// where e is the vector to be rotated (given by dx0, dx1, dx2) and k
// is the surface normal of the cell
double _k%(restriction)s0 = (x%(restriction)s[1][1] - x%(restriction)s[0][1])*(x%(restriction)s[2][2] - x%(restriction)s[0][2]) - (x%(restriction)s[1][2] - x%(restriction)s[0][2])*(x%(restriction)s[2][1] - x%(restriction)s[0][1]);
double _k%(restriction)s1 = - ((x%(restriction)s[1][0] - x%(restriction)s[0][0])*(x%(restriction)s[2][2] - x%(restriction)s[0][2]) - (x%(restriction)s[1][2] - x%(restriction)s[0][2])*(x%(restriction)s[2][0] - x%(restriction)s[0][0]));
double _k%(restriction)s2 = (x%(restriction)s[1][0] - x%(restriction)s[0][0])*(x%(restriction)s[2][1] - x%(restriction)s[0][1]) - (x%(restriction)s[1][1] - x%(restriction)s[0][1])*(x%(restriction)s[2][0] - x%(restriction)s[0][0]);
const double _k%(restriction)s_length = std:sqrt(_k%(restriction)s0*_k%(restriction)s0 + _k%(restriction)s1*_k%(restriction)s1 + _k%(restriction)s2*_k%(restriction)s2);
_k%(restriction)s0 /= _k%(restriction)s_length;
_k%(restriction)s1 /= _k%(restriction)s_length;
_k%(restriction)s2 /= _k%(restriction)s_length;
const double k%(restriction)sdote = k%(restriction)s0*dx0 + k%(restriction)s1*dx1 + k%(restriction)s2*dx2;

double n%(restriction)s0 = (k%(restriction)s1*dx2 - k%(restriction)s2*dx1) + k%(restriction)s0*k%(restriction)sdote;
double n%(restriction)s1 = -(k%(restriction)s0*dx2 - k%(restriction)s2*dx0) + k%(restriction)s1*k%(restriction)sdote;
double n%(restriction)s2 = (k%(restriction)s0*dx1 - k%(restriction)s1*dx0) + k%(restriction)s2*k%(restriction)sdote;

"""

_facet_normal_3D_1D = """
// Compute facet normal
double n%(restriction)s0 = 0.0;
double n%(restriction)s1 = 0.0;
double n%(restriction)s2 = 0.0;
if (facet%(restriction)s == 0)
{
  n%(restriction)s0 = x[0][0] - x[1][0];
  n%(restriction)s1 = x[0][1] - x[1][1];
  n%(restriction)s1 = x[0][2] - x[1][2];
} else {
  n%(restriction)s0 = x[1][0] - x[0][0];
  n%(restriction)s1 = x[1][1] - x[0][1];
  n%(restriction)s1 = x[1][2] - x[0][2];
}
const double length = std::sqrt(n%(restriction)s0*n%(restriction)s0 + n%(restriction)s1*n%(restriction)s1 + n%(restriction)s2*n%(restriction)s2);
n%(restriction)s0 /= length;
n%(restriction)s1 /= length;
n%(restriction)s2 /= length;
"""

_cell_volume_1D = """\
// Cell Volume.
const double volume%(restriction)s = std::abs(detJ%(restriction)s);"""

_cell_volume_2D = """\
// Cell Volume.
const double volume%(restriction)s = std::abs(detJ%(restriction)s)/2.0;"""

_cell_volume_3D = """\
// Cell Volume.
const double volume%(restriction)s = std::abs(detJ%(restriction)s)/6.0;"""

_circumradius_1D = """\
// Compute circumradius, in 1D it is equal to the cell volume.
const double circumradius%(restriction)s = std::abs(detJ%(restriction)s);"""

_circumradius_2D = """\
// Compute circumradius, assuming triangle is embedded in 2D.
const double v1v2%(restriction)s  = std::sqrt( (x%(restriction)s[2][0] - x%(restriction)s[1][0])*(x%(restriction)s[2][0] - x%(restriction)s[1][0]) + (x%(restriction)s[2][1] - x%(restriction)s[1][1])*(x%(restriction)s[2][1] - x%(restriction)s[1][1]) );
const double v0v2%(restriction)s  = std::sqrt( J%(restriction)s_11*J%(restriction)s_11 + J%(restriction)s_01*J%(restriction)s_01 );
const double v0v1%(restriction)s  = std::sqrt( J%(restriction)s_00*J%(restriction)s_00 + J%(restriction)s_10*J%(restriction)s_10 );

const double circumradius%(restriction)s = 0.25*(v1v2%(restriction)s*v0v2%(restriction)s*v0v1%(restriction)s)/(volume%(restriction)s);"""

_circumradius_3D = """\
// Compute circumradius.
const double v1v2%(restriction)s  = std::sqrt( (x%(restriction)s[2][0] - x%(restriction)s[1][0])*(x%(restriction)s[2][0] - x%(restriction)s[1][0]) + (x%(restriction)s[2][1] - x%(restriction)s[1][1])*(x%(restriction)s[2][1] - x%(restriction)s[1][1]) + (x%(restriction)s[2][2] - x%(restriction)s[1][2])*(x%(restriction)s[2][2] - x%(restriction)s[1][2]) );
const double v0v2%(restriction)s  = std::sqrt(J%(restriction)s_01*J%(restriction)s_01 + J%(restriction)s_11*J%(restriction)s_11 + J%(restriction)s_21*J%(restriction)s_21);
const double v0v1%(restriction)s  = std::sqrt(J%(restriction)s_00*J%(restriction)s_00 + J%(restriction)s_10*J%(restriction)s_10 + J%(restriction)s_20*J%(restriction)s_20);
const double v0v3%(restriction)s  = std::sqrt(J%(restriction)s_02*J%(restriction)s_02 + J%(restriction)s_12*J%(restriction)s_12 + J%(restriction)s_22*J%(restriction)s_22);
const double v1v3%(restriction)s  = std::sqrt( (x%(restriction)s[3][0] - x%(restriction)s[1][0])*(x%(restriction)s[3][0] - x%(restriction)s[1][0]) + (x%(restriction)s[3][1] - x%(restriction)s[1][1])*(x%(restriction)s[3][1] - x%(restriction)s[1][1]) + (x%(restriction)s[3][2] - x%(restriction)s[1][2])*(x%(restriction)s[3][2] - x%(restriction)s[1][2]) );
const double v2v3%(restriction)s  = std::sqrt( (x%(restriction)s[3][0] - x%(restriction)s[2][0])*(x%(restriction)s[3][0] - x%(restriction)s[2][0]) + (x%(restriction)s[3][1] - x%(restriction)s[2][1])*(x%(restriction)s[3][1] - x%(restriction)s[2][1]) + (x%(restriction)s[3][2] - x%(restriction)s[2][2])*(x%(restriction)s[3][2] - x%(restriction)s[2][2]) );
const  double la%(restriction)s   = v1v2%(restriction)s*v0v3%(restriction)s;
const  double lb%(restriction)s   = v0v2%(restriction)s*v1v3%(restriction)s;
const  double lc%(restriction)s   = v0v1%(restriction)s*v2v3%(restriction)s;
const  double s%(restriction)s    = 0.5*(la%(restriction)s+lb%(restriction)s+lc%(restriction)s);
const  double area%(restriction)s = std::sqrt(s%(restriction)s*(s%(restriction)s-la%(restriction)s)*(s%(restriction)s-lb%(restriction)s)*(s%(restriction)s-lc%(restriction)s));

const double circumradius%(restriction)s = area%(restriction)s / ( 6.0*volume%(restriction)s );"""

_facet_area_1D = """\
// Facet Area (FIXME: Should this be 0.0?).
const double facet_area = 1.0;"""

_facet_area_2D = """\
// Facet Area.
const double facet_area = det;"""

_facet_area_3D = """\
// Facet Area (divide by two because 'det' is scaled by area of reference triangle).
const double facet_area = det/2.0;"""

evaluate_basis_dofmap = """\
unsigned int element = 0;
unsigned int tmp = 0;
for (unsigned int j = 0; j < %d; j++)
{
  if (tmp +  dofs_per_element[j] > i)
  {
    i -= tmp;
    element = element_types[j];
    break;
  }
  else
    tmp += dofs_per_element[j];
}"""

# Used in evaluate_basis_derivatives. For second order derivatives in 2D it will
# generate the combinations: [(0, 0), (0, 1), (1, 0), (1, 1)] (i.e., xx, xy, yx, yy)
# which will also be the ordering of derivatives in the return value.
combinations_snippet = """\
// Declare pointer to two dimensional array that holds combinations of derivatives and initialise
unsigned int **%(combinations)s = new unsigned int *[%(num_derivatives)s];
for (unsigned int row = 0; row < %(num_derivatives)s; row++)
{
  %(combinations)s[row] = new unsigned int [%(n)s];
  for (unsigned int col = 0; col < %(n)s; col++)
    %(combinations)s[row][col] = 0;
}

// Generate combinations of derivatives
for (unsigned int row = 1; row < %(num_derivatives)s; row++)
{
  for (unsigned int num = 0; num < row; num++)
  {
    for (unsigned int col = %(n)s-1; col+1 > 0; col--)
    {
      if (%(combinations)s[row][col] + 1 > %(dimension-1)s)
        %(combinations)s[row][col] = 0;
      else
      {
        %(combinations)s[row][col] += 1;
        break;
      }
    }
  }
}"""

def _transform_snippet(tdim, gdim):

    if tdim == gdim:
        _t = ""
        _g = ""
    else:
        _t = "_t"
        _g = "_g"

    # Matricize K_ij -> {K_ij}
    matrix = "{{" + "}, {".join([", ".join(["K_%d%d"% (t, g)
                                            for g in range(gdim)])
                                 for t in range(tdim)]) + "}};\n\n"
    snippet = """\
// Compute inverse of Jacobian
const double %%(K)s[%d][%d] = %s""" % (tdim, gdim, matrix)

    snippet +="""// Declare transformation matrix
// Declare pointer to two dimensional array and initialise
double **%%(transform)s = new double *[%%(num_derivatives)s%(g)s];

for (unsigned int j = 0; j < %%(num_derivatives)s%(g)s; j++)
{
  %%(transform)s[j] = new double [%%(num_derivatives)s%(t)s];
  for (unsigned int k = 0; k < %%(num_derivatives)s%(t)s; k++)
    %%(transform)s[j][k] = 1;
}

// Construct transformation matrix
for (unsigned int row = 0; row < %%(num_derivatives)s%(g)s; row++)
{
  for (unsigned int col = 0; col < %%(num_derivatives)s%(t)s; col++)
  {
    for (unsigned int k = 0; k < %%(n)s; k++)
      %%(transform)s[row][col] *= %%(K)s[%%(combinations)s%(t)s[col][k]][%%(combinations)s%(g)s[row][k]];
  }
}""" % {"t":_t, "g":_g}

    return snippet

# Codesnippets used in evaluate_dof
_map_onto_physical_1D = """\
// Evaluate basis functions for affine mapping
const double w0 = 1.0 - X_%(i)d[%(j)s][0];
const double w1 = X_%(i)d[%(j)s][0];

// Compute affine mapping y = F(X)
y[0] = w0*x[0][0] + w1*x[1][0];"""

_map_onto_physical_2D = """\
// Evaluate basis functions for affine mapping
const double w0 = 1.0 - X_%(i)d[%(j)s][0] - X_%(i)d[%(j)s][1];
const double w1 = X_%(i)d[%(j)s][0];
const double w2 = X_%(i)d[%(j)s][1];

// Compute affine mapping y = F(X)
y[0] = w0*x[0][0] + w1*x[1][0] + w2*x[2][0];
y[1] = w0*x[0][1] + w1*x[1][1] + w2*x[2][1];"""

_map_onto_physical_3D = """\
// Evaluate basis functions for affine mapping
const double w0 = 1.0 - X_%(i)d[%(j)s][0] - X_%(i)d[%(j)s][1] - X_%(i)d[%(j)s][2];
const double w1 = X_%(i)d[%(j)s][0];
const double w2 = X_%(i)d[%(j)s][1];
const double w3 = X_%(i)d[%(j)s][2];

// Compute affine mapping y = F(X)
y[0] = w0*x[0][0] + w1*x[1][0] + w2*x[2][0] + w3*x[3][0];
y[1] = w0*x[0][1] + w1*x[1][1] + w2*x[2][1] + w3*x[3][1];
y[2] = w0*x[0][2] + w1*x[1][2] + w2*x[2][2] + w3*x[3][2];"""

_ip_coordinates_1D = """\
X%(num_ip)d[0] = %(name)s[%(ip)s][0]*x%(restriction)s[0][0] + \
%(name)s[%(ip)s][1]*x%(restriction)s[1][0];"""

_ip_coordinates_2D = """\
X%(num_ip)d[0] = %(name)s[%(ip)s][0]*x%(restriction)s[0][0] + \
%(name)s[%(ip)s][1]*x%(restriction)s[1][0] + %(name)s[%(ip)s][2]*x%(restriction)s[2][0];
X%(num_ip)d[1] = %(name)s[%(ip)s][0]*x%(restriction)s[0][1] + \
%(name)s[%(ip)s][1]*x%(restriction)s[1][1] + %(name)s[%(ip)s][2]*x%(restriction)s[2][1];"""

_ip_coordinates_3D = """\
X%(num_ip)d[0] = %(name)s[%(ip)s][0]*x%(restriction)s[0][0] + \
%(name)s[%(ip)s][1]*x%(restriction)s[1][0] + %(name)s[%(ip)s][2]*x%(restriction)s[2][0] + \
%(name)s[%(ip)s][3]*x%(restriction)s[3][0];
X%(num_ip)d[1] = %(name)s[%(ip)s][0]*x%(restriction)s[0][1] + \
%(name)s[%(ip)s][1]*x%(restriction)s[1][1] + %(name)s[%(ip)s][2]*x%(restriction)s[2][1] + \
%(name)s[%(ip)s][3]*x%(restriction)s[3][1];
X%(num_ip)d[2] = %(name)s[%(ip)s][0]*x%(restriction)s[0][2] + \
%(name)s[%(ip)s][1]*x%(restriction)s[1][2] + %(name)s[%(ip)s][2]*x%(restriction)s[2][2] + \
%(name)s[%(ip)s][3]*x%(restriction)s[3][2];"""

# Codesnippets used in evaluatebasis[|derivatives]
_map_coordinates_FIAT_interval = """\
// Get coordinates and map to the reference (FIAT) element
double X = (2.0*coordinates[0] - x[0][0] - x[1][0]) / J_00;"""

_map_coordinates_FIAT_interval_in_2D = """\
// Get coordinates and map to the reference (FIAT) element
double X = 2*(std::sqrt(std::pow(coordinates[0]-x[0][0], 2) + std::pow(coordinates[1]-x[0][1], 2))/ detJ) - 1.0;"""

_map_coordinates_FIAT_interval_in_3D = """\
// Get coordinates and map to the reference (FIAT) element
double X = 2*(std::sqrt(std::pow(coordinates[0]-x[0][0], 2) + std::pow(coordinates[1]-x[0][1], 2) + std::pow(coordinates[2]-x[0][2], 2))/ detJ) - 1.0;"""

_map_coordinates_FIAT_triangle = """\
// Compute constants
const double C0 = x[1][0] + x[2][0];
const double C1 = x[1][1] + x[2][1];

// Get coordinates and map to the reference (FIAT) element
double X = (J_01*(C1 - 2.0*coordinates[1]) + J_11*(2.0*coordinates[0] - C0)) / detJ;
double Y = (J_00*(2.0*coordinates[1] - C1) + J_10*(C0 - 2.0*coordinates[0])) / detJ;"""

_map_coordinates_FIAT_triangle_in_3D = """\
const double b0 = x[0][0];
const double b1 = x[0][1];
const double b2 = x[0][2];

// P_FFC = J^dag (p - b), P_FIAT = 2*P_FFC - (1, 1)
double X = 2*(K_00*(coordinates[0] - b0) + K_01*(coordinates[1] - b1) + K_02*(coordinates[2] - b2)) - 1.0;
double Y = 2*(K_10*(coordinates[0] - b0) + K_11*(coordinates[1] - b1) + K_12*(coordinates[2] - b2)) - 1.0;
"""

_map_coordinates_FIAT_tetrahedron = """\
// Compute constants
const double C0 = x[3][0] + x[2][0] + x[1][0] - x[0][0];
const double C1 = x[3][1] + x[2][1] + x[1][1] - x[0][1];
const double C2 = x[3][2] + x[2][2] + x[1][2] - x[0][2];

// Get coordinates and map to the reference (FIAT) element
double X = (d_00*(2.0*coordinates[0] - C0) + d_10*(2.0*coordinates[1] - C1) + d_20*(2.0*coordinates[2] - C2)) / detJ;
double Y = (d_01*(2.0*coordinates[0] - C0) + d_11*(2.0*coordinates[1] - C1) + d_21*(2.0*coordinates[2] - C2)) / detJ;
double Z = (d_02*(2.0*coordinates[0] - C0) + d_12*(2.0*coordinates[1] - C1) + d_22*(2.0*coordinates[2] - C2)) / detJ;
"""

# Mappings to code snippets used by format

# The 'jacobian', 'inverse_jacobian', 'facet_determinant' dictionaries
# accept as keys first the geometric dimension, and then the
# topological dimension
jacobian = {1: {1:_jacobian_1D},
            2: {2:_jacobian_2D, 1:_jacobian_2D_1D},
            3: {3:_jacobian_3D, 2:_jacobian_3D_2D, 1:_jacobian_3D_1D}}

inverse_jacobian = {1: {1:_inverse_jacobian_1D},
                    2: {2:_inverse_jacobian_2D, 1:_inverse_jacobian_2D_1D},
                    3: {3:_inverse_jacobian_3D, 2:_inverse_jacobian_3D_2D,
                        1:_inverse_jacobian_3D_1D}}

facet_determinant = {1: {1: _facet_determinant_1D},
                     2: {2: _facet_determinant_2D, 1: _facet_determinant_2D_1D},
                     3: {3: _facet_determinant_3D, 2: _facet_determinant_3D_2D,
                         1: _facet_determinant_3D_1D}}

map_onto_physical = {1: _map_onto_physical_1D,
                     2: _map_onto_physical_2D,
                     3: _map_onto_physical_3D}

# FIXME: Must add more here
fiat_coordinate_map = {"interval": {1:_map_coordinates_FIAT_interval,
                                    2:_map_coordinates_FIAT_interval_in_2D,
                                    3:_map_coordinates_FIAT_interval_in_3D},
                       "triangle": {2:_map_coordinates_FIAT_triangle,
                                    3: _map_coordinates_FIAT_triangle_in_3D},
                       "tetrahedron": {3:_map_coordinates_FIAT_tetrahedron}}

transform_snippet = {"interval": {1: _transform_snippet(1, 1),
                                  2: _transform_snippet(1, 2),
                                  3: _transform_snippet(1, 3)},
                     "triangle": {2: _transform_snippet(2, 2),
                                  3: _transform_snippet(2, 3)},
                     "tetrahedron": {3: _transform_snippet(3, 3)}}

normal_direction = {1: {1: _normal_direction_1D},
                    2: {2: _normal_direction_2D, 1: _normal_direction_2D_1D},
                    3: {3: _normal_direction_3D, 2: _normal_direction_3D_2D,
                        1: _normal_direction_3D_1D}}

facet_normal = {1: {1: _facet_normal_1D},
                2: {2: _facet_normal_2D, 1: _facet_normal_2D_1D},
                3: {3: _facet_normal_3D, 2: _facet_normal_3D_2D, 1: _facet_normal_3D_1D}}

ip_coordinates = {1: (3, _ip_coordinates_1D),
                  2: (10, _ip_coordinates_2D),
                  3: (21, _ip_coordinates_3D)}

cell_volume = {1: _cell_volume_1D,
               2: _cell_volume_2D,
               3: _cell_volume_3D}

circumradius = {1: _circumradius_1D,
                2: _circumradius_2D,
                3: _circumradius_3D}

facet_area = {1: _facet_area_1D,
              2: _facet_area_2D,
              3: _facet_area_3D}

