MasterModule
============

This Module contains all classes needed for all scripts of my master 
thesis. To mention only the most important features: You can read in
radar data from PATTERN 
(`netCDF <https://www.unidata.ucar.edu/software/netcdf/>`_) or DWD
(`hdf5 <https://support.hdfgroup.org/HDF5/>`_)
data files, interpolate the radar data to a cartesian grid, calculate 
beam heights of the radar beam and plot reflectivity data. For more 
details, take a look into the classes and their methods or see some 
:doc:`examples <scripts>`.

.. currentmodule:: MasterModule

Class overview
--------------

.. autosummary::
   :toctree: stubs

   cartesian_coordinates
   cartesian_grid
   dwd_radar
   grid_coordinates
   grid_corners
   grid_plot
   heights_plot
   main_radar
   middle_coordinates
   pattern_radar
   pattern_radar_v2
   radar_data
   refl_diff_plot
   refl_plot
