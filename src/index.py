__author__ = "Anders Logg (logg@tti-c.org)"
__version__ = "0.0.1"
__date__ = "2004-09-29"
__copyright__ = "Copyright (c) 2004 Anders Logg"
__license__  = "GNU GPL Version 2"

next_index_1 = 0
next_index_2 = 0

def next_primary_index():
    "Return next available primary index."
    global next_index_1
    next_index_1 += 1
    return next_index_1 - 1

def next_secondary_index():
    "Return next available secondary index."
    global next_index_2
    next_index_2 += 1
    return next_index_2 - 1

def reset():
    "Reset all indices."
    global next_index_1, next_index_2
    next_index_1 = 0
    next_index_2 = 0

class Index:
    
    """An Index represents a tensor index. The type of index can be
    either fixed, primary, or secondary as listed below

      fixed:     tensor rank 0, index is a fixed integer
      primary:   tensor rank 1, index is part of first multiindex (i)
      secondary: tensor rank 1, index is part of second multiindex (alpha)
      
    The type of index is determined by the arguments to the
    constructor:

      i = Index(0)           creates a given fixed index (0 in this case)
      i = Index("primary")   creates a free primary index
      i = Index("secondary") creates a free primary index
      i = Index()            creates a free secondary index"""

    def __init__(self, index = "secondary"):
        if isinstance(index, Index):
            self.index = index.index
            self.type = index.type
        elif isinstance(index, int):
            self.index = index
            self.type = "fixed"
        elif index == "primary":
            self.index = next_primary_index()
            self.type = "primary"
        elif index == "secondary":
            self.index = next_secondary_index()
            self.type = "secondary"
        elif index == None:
            self.index = next_secondary_index()
            self.type = "secondary"
        else:
            raise RuntimeError, "Unknown index type " + str(index)
        return

    def __call__(self, index, r0):
        "Return current index."
        if self.type == "fixed":
            return self.index
        elif self.type == "primary":
            return index[self.index]
        elif self.type == "secondary":
            return index[self.index + r0]
        else:
            raise RuntimeError, "Unknown index type " + str(index)
        
    def __repr__(self):
        if self.type == "fixed":
            return str(self.index)
        elif self.type == "primary":
            return "i" + str(self.index)
        elif self.type == "secondary":
            return "a" + str(self.index)
        else:
            raise RuntimeError, "Unknown index type " + str(index)
        return
