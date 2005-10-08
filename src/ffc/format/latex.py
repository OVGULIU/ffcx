"LaTeX output format."

__author__ = "Anders Logg (logg@tti-c.org)"
__date__ = "2004-10-14 -- 2005-10-07"
__copyright__ = "Copyright (c) 2004, 2005 Anders Logg"
__license__  = "GNU GPL Version 2"

# FFC common modules
from ffc.common.constants import *

# Specify formatting for code generation
format = { "sum": lambda l: " + ".join(l),
           "subtract": lambda l: " - ".join(l),
           "multiplication": lambda l: "".join(l),
           "grouping": lambda s: "(%s)" % s,
           "determinant": "\\det F_K'",
           "floating point": lambda a: __floating_point(a),
           "constant": lambda j: "c%d" % j,
           "coefficient": lambda j, k: "w_{%d%d}" % (j + 1, k + 1),
           "transform": lambda j, k: "\\frac{\\partial X_{%d}}{\\partial x_{%d}}" % (j + 1, k + 1),
           "reference tensor" : lambda j, i, a: None,
           "geometry tensor": lambda j, a: "G_{K,%d}^{%s}" % (j + 1, ",".join(["%d" % (index + 1) for index in a])),
           "element tensor": lambda i, k: "A^K_{%s}" % "".join(["%d" % (index + 1) for index in i]) }

def init(options):
    "Initialize code generation for LaTeX format."
    return

def write(forms, options):
    "Generate code for LaTeX format."
    print "Generating output for LaTeX"

    # Get name of form
    name = forms[0].name

    # Write file header
    output = ""
    output += __file_header(name)

    # Write all forms
    for j in range(len(forms)):
        output += "\\section{Form %s}\n" % str(j + 1)
        output += __form(forms[j])

    # Write file footer
    output += __file_footer()

    # Write file
    filename = name + ".tex"
    file = open(filename, "w")
    file.write(output)
    file.close()
    print "Output written to " + filename

    return

def __file_header(name):
    "Generate file header for LaTeX."
    return """
\\documentclass[12pt]{article}

\\begin{document}

\\title{%s}
\\author{Automatically generated by FFC version %s}
\\date{\\today}
\\maketitle

""" % (name, FFC_VERSION)

def __file_footer():
    "Generate file footer for LaTeX."
    return """
\\end{document}
"""

def __form(form):
    "Generate form for LaTeX."
    output = ""    

    # Interior contribution
    if form.AKi.terms:
        output += """\
\\subsection{Interior contribution}
\\subsubsection{Evaluation of the geometry tensor}

\\begin{equation}
  \\begin{array}{rcl}
"""
        for gK in form.AKi.gK:
            output += "    %s &=& %s \\\\\n" % (gK.name, gK.value)
        output += """  \\end{array}
\\end{equation}

\\subsubsection{Evaluation of the element tensor}

\\begin{equation}
  \\begin{array}{rcl}
"""
        for aK in form.AKi.aK:
            output += "    %s &=& %s \\\\\n" % (aK.name, aK.value)
        output += """ \\end{array}
\\end{equation}

"""

        # Display as a matrix of matrices if possible
        A0 = form.AKi.terms[0].A0
        if len(form.AKi.terms) == 1 and A0.i.rank == A0.a.rank == 2:
            output += __reference_tensor(A0)

    # Boundary contribution
    if form.AKb.terms:
        output += """\
\\subsection{Boundary contribution}
\\subsubsection{Evaluation of the geometry tensor}

\\begin{equation}
  \\begin{array}{rcl}
"""
        for gK in form.AKb.gK:
            output += "    %s &=& %s \\\\\n" % (gK.name, gK.value)
        output += """  \\end{array}
\\end{equation}

\\subsubsection{Evaluation of the element tensor}

\\begin{equation}
  \\begin{array}{rcl}
"""
        for aK in form.AKb.aK:
            output += "    %s &=& %s \\\\\n" % (aK.name, aK.value)
        output += """ \\end{array}
\\end{equation}

"""
    return output

def __reference_tensor(A0):
    """Generate LaTeX representation of reference tensor as a matrix
    of matrices if possible (both primary and secondary ranks need to
    be 2)."""
    output = ""

    # First alternative: primary index i leading (alpha in sub matrices)
    output += """\
\\subsubsection{Reference tensor ($i$ leading index)}

\\begin{center}
\\begin{tabular}{|%s|}\n\\hline\n""" % "|".join(["c" for j in range(A0.i.dims[1])])
    for i0 in range(A0.i.dims[0]):
        for i1 in range(A0.i.dims[1]):
            output += "\\begin{tabular}{%s}\n" % "".join(["c" for j in range(A0.a.dims[1])])
            for a0 in range(A0.a.dims[0]):
                for a1 in range(A0.a.dims[1]):
                    output += __floating_point(A0.A0[[i0,i1,a0,a1]])
                    if not (a1 == A0.a.dims[1] - 1):
                        output += " & "
                output += "\\\\\n"
            output += "\\end{tabular}\n"
            if not (i1 == A0.i.dims[1] - 1):
                output += "&\n"
        output += "\\\\\\hline\n"
    output += """\
\\end{tabular}
\\end{center}

"""

    # Second alternative: secondary index i leading (i in sub matrices)
    output += """\
\\subsubsection{Reference tensor ($\\alpha$ leading index)}

\\begin{center}
\\begin{tabular}{|%s|}\n\\hline\n""" % "|".join(["c" for j in range(A0.a.dims[1])])
    for a0 in range(A0.a.dims[0]):
        for a1 in range(A0.a.dims[1]):
            output += "\\begin{tabular}{%s}\n" % "".join(["c" for j in range(A0.i.dims[1])])
            for i0 in range(A0.i.dims[0]):
                for i1 in range(A0.i.dims[1]):
                    output += __floating_point(A0.A0[[i0,i1,a0,a1]])
                    if not (i1 == A0.i.dims[1] - 1):
                        output += " & "
                output += "\\\\\n"
            output += "\\end{tabular}\n"
            if not (a1 == A0.a.dims[1] - 1):
                output += "&\n"
        output += "\\\\\\hline\n"
    output += """\
\\end{tabular}
\\end{center}

"""

    return output

def __floating_point(a):
    "Format (round) floating point number"
    if abs(round(a) - a) < FFC_EPSILON:
        return "%d" % round(a)
    else:
        return "%.3f" % a
