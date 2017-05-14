beam_height_diff.py
===================

This script creates a plot of height differences between PATTERN and 
DWD radar on a cartesian grid. 

.. note:
   The first and second data file should be from different radars, since 
   the height difference between the same radar results in zero 
   everywhere.

In parameters.py the following parameters incluence the output:

- **grid_par['lon']**: Longitude coordinate of grid center.
- **grid_par['lat']**: Latitude coordinate of grid center.
- **grid_par['res']**: Resolution of the cartesian grid in meters.
- **grid_par['lon_shape']**: Number of longitude grid boxes.
- **grid_par['lat_shape']**: Number of latitude grid boxes.
- **plot_par['tick_nr']**: Number of grid lines plotted.
- **plot_par['height_iso']**: Isolines to be plotted.
- **plot_par['max_range']**: Range to center, starting from which the 
  data will be masked.
- **radar1_par['file']**: Name of the first data file.
- **radar2_par['file']**: Name of the second data file.

    
Example
-------

.. figure:: ../../../../plots/example_plots/beam_height_diff.png

The example image was created using a PATTERN data file with the 
following parameters:

- **grid_par['lon']**: 0.23101493
- **grid_par['lat']**: -0.36853593
- **grid_par['res']**: 250
- **grid_par['lon_shape']**: 160
- **grid_par['lat_shape']**: 160
- **plot_par['tick_nr']**: 10
- **plot_par['height_iso']**: np.array(-1000,1001,250)
- **plot_par['max_range']**: 19966.140625
