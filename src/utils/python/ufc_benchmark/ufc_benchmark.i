%module ufc_benchmark

%{
#include "ufc.h"
#include "ufc_benchmark.h"
#include "ufc_reference_cell.h"
#include <vector>
%}

%include stl.i
%include std_vector.i
%include std_carray.i

%template(vector_double)     std::vector<double>;
%typedef std::vector<double> vector_double;

%template(vector_vector_double)             std::vector< std::vector<double> >;
%typedef std::vector< std::vector<double> > vector_vector_double;

%template(vector_uint) std::vector< unsigned int >;
%typedef std::vector< unsigned int > vector_uint;

%template(vector_vector_uint) std::vector< std::vector< unsigned int > >;
%typedef std::vector< std::vector< unsigned int > > vector_vector_uint;

%include "ufc.h"
%include "ufc_benchmark.h"
%include "ufc_reference_cell.h"

%pythoncode{

def benchmark_forms(forms, print_tensors):
    import gc
    gc.collect()
    
    times = []
    for f in forms:
        res = benchmark(f, print_tensors)
        times.append(tuple(res))
    return times

}
