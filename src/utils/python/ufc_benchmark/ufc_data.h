// This is utility code for UFC (Unified Form-assembly Code) v. 1.1.
// This code is released into the public domain.
//
// The FEniCS Project (http://www.fenics.org/) 2006-2007.

#ifndef __UFC_DATA_H__
#define __UFC_DATA_H__

#include <ufc.h>
#include <vector>
#include <stdexcept>

namespace ufc
{

  class ufc_data
  {
  public:

    ufc_data(const ufc::form & form):
      form(form)
    {
      // short forms of dimensions
      rank             = form.rank();
      num_coefficients = form.num_coefficients();
      num_arguments    = rank + num_coefficients;

      // construct all dofmaps and elements
      dofmaps.resize(num_arguments);
      elements.resize(num_arguments);
      dimensions = new uint[num_arguments];

      for(uint i=0; i<num_arguments; i++)
      {
        dofmaps[i]    = form.create_dof_map(i);
        elements[i]   = form.create_finite_element(i);
        dimensions[i] = dofmaps[i]->local_dimension();

        if(dimensions[i] != elements[i]->space_dimension())
          throw std::runtime_error("Mismatching dimensions between finite_elements and dof_maps!");

        if(elements[0]->cell_shape() != elements[i]->cell_shape())
          throw std::runtime_error("Mismatching cell shapes in elements!");
      }

      // construct all integral objects
      cell_integrals.resize(form.num_cell_integrals());
      for(uint i=0; i<form.num_cell_integrals(); i++)
      {
        cell_integrals[i] = form.create_cell_integral(i);
      }
      exterior_facet_integrals.resize(form.num_exterior_facet_integrals());
      for(uint i=0; i<form.num_exterior_facet_integrals(); i++)
      {
        exterior_facet_integrals[i] = form.create_exterior_facet_integral(i);
      }
      interior_facet_integrals.resize(form.num_interior_facet_integrals());
      for(uint i=0; i<form.num_interior_facet_integrals(); i++)
      {
        interior_facet_integrals[i] = form.create_interior_facet_integral(i);
      }

      // compute size of element tensor A
      A_size = 1;
      for(uint i=0; i<rank; i++)
      {
        A_size *= dimensions[i];
      }

      // allocate space for element tensor A
      A = new double[A_size];

      // Initialize local tensor for macro element
      A_size = 1;
      for (uint i = 0; i < form.rank(); i++)
        A_size *= 2*dimensions[i];
      macro_A = new double[A_size];

      // allocate space for local coefficient data
      w = new double*[num_coefficients];
      for(uint i=0; i<num_coefficients; i++)
      {
        uint dim = dimensions[i+rank];
        w[i] = new double[dim];
        memset(w[i], 0, sizeof(double)*dim);
      }

      // allocate space for local macro coefficient data
      macro_w = new double*[num_coefficients];
      for(uint i=0; i<num_coefficients; i++)
      {
        uint dim = 2*dimensions[i+rank];
        macro_w[i] = new double[dim];
        memset(macro_w[i], 0, sizeof(double)*dim);
      }
    }

    ~ufc_data()
    {
      for(uint i=0; i<num_arguments; i++)
        delete dofmaps[i];

      for(uint i=0; i<num_arguments; i++)
        delete elements[i];
      
      delete [] dimensions;

      for(uint i=0; i<form.num_cell_integrals(); i++)
        delete cell_integrals[i];
      
      for(uint i=0; i<form.num_exterior_facet_integrals(); i++)
        delete exterior_facet_integrals[i];
      
      for(uint i=0; i<form.num_interior_facet_integrals(); i++)
        delete interior_facet_integrals[i];

      for(uint i=0; i<num_coefficients; i++)
        delete [] w[i];
      delete [] w;

      for(uint i=0; i<num_coefficients; i++)
        delete [] macro_w[i];
      delete [] macro_w;
      
      delete [] A;
      delete [] macro_A;
    }

    const ufc::form & form;

    vector< ufc::dof_map * >        dofmaps;
    vector< ufc::finite_element * > elements;

    vector< ufc::cell_integral *>             cell_integrals;
    vector< ufc::exterior_facet_integral *>   exterior_facet_integrals;
    vector< ufc::interior_facet_integral *>   interior_facet_integrals;

    uint rank;
    uint num_coefficients;
    uint num_arguments;
    uint A_size;

    uint   *  dimensions;
    double *  A;
    double *  macro_A;
    double ** w;
    double ** macro_w;


    void print_tensor()
    {
      int dim0 = 1;
      int dim1 = 1;

      if(rank == 1)
      {
          dim1 = dimensions[0];
      }
      if(rank == 2)
      {
          dim0 = dimensions[0];
          dim1 = dimensions[1];
      }
      
      cout << "[" << endl;
      int k=0;
      for(int ii=0; ii<dim0; ii++)
      {
        for(int jj=0; jj<dim1; jj++)
        {
          cout << A[k++] << ", ";
        }
        cout << endl;
      }
      cout << "]" << endl;
      cout << endl;
    }
  };

}

#endif

