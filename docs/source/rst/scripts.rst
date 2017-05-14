Scripts
========

Listed below are all scripts of my master thesis. For each script, there
is an example on how to use it. All scripts grab their input information
from the file 'parameters.py'. By modifying this file, you can adjust 
the parameters to match your intentions.

.. note:: 
   Most of the scripts use cartesian grids. These grids must be near
   the equator, to keep geometry easy (longitudes and latitudes are 
   perpendicular at the equator). Thus, input coordinates are 
   transformed to rotated pole coordinates with Hamburg at the 
   equator.
   
.. note::
   All scripts are designed for PATTERN 
   (`netCDF <https://www.unidata.ucar.edu/software/netcdf/>`_) or DWD 
   (`hdf5 <https://support.hdfgroup.org/HDF5/>`_) data
   files. Only input files structured in a very similar way will work.

.. note::
   My version of PATTERN data is rotated by a few degrees. Double 
   check, if your radar data, too, is rotated by accident. If so - 
   change the offset in parameters.py to correct the rotation.
   
.. toctree::
   :maxdepth: 1
   
   scripts/beam_height
   scripts/beam_height_diff
   scripts/cartesian_plot
   scripts/difference_plot
   scripts/get_sun
   scripts/radar_plot
