cartesian_plot.py
=================

This script creates a reflectivity plot on a cartesian grid. 

In parameters.py the following parameters incluence the output:

- **grid_par['lon']**: Longitude coordinate of grid center.
- **grid_par['lat']**: Latitude coordinate of grid center.
- **grid_par['res']**: Resolution of the cartesian grid in meters.
- **grid_par['lon_shape']**: Number of longitude grid boxes.
- **grid_par['lat_shape']**: Number of latitude grid boxes.
- **plot_par['tick_nr']**: Number of grid lines plotted.
- **plot_par['rain_th']**: Reflectivity threshold, at which rain is 
  assumed.
- **plot_par['max_range']**: Range to center, starting from which the 
  data will be masked.
- **radar1_par['file']**: Name of the data file.
- **radar1_par['res_fac']**: Factor, by which the azimuth resolution of 
  the data will be increased artificially.
  
In case of PATTERN data, also these parameters can be set:

- **radar1_par['minute']**: Minute of hourly data.
- **radar1_par['offset']**: Azimuth offset of data, which will be 
  corrected by rotating the data.

.. note::
   It is also possible to change the parameter 
   **radar1_par['proc_key']**. This parameter changes the processing 
   step of the PATTERN data. You shouldn't change this parameter though,
   since the other processing step seems to have flaws.
   
Example
-------

.. figure:: ../../../../plots/example_plots/cartesian_plot.png

The example image was created using the PATTERN data file for the 
7th June 2016 at 16:00 UTC with the following parameters:

- **grid_par['lon']**: 0.23101493
- **grid_par['lat']**: -0.36853593
- **grid_par['res']**: 250
- **grid_par['lon_shape']**: 160
- **grid_par['lat_shape']**: 160
- **plot_par['tick_nr']**: 10
- **plot_par['rain_th']**: 5
- **plot_par['max_range']**: 19966.140625
- **radar1_par['res_fac']**: 1
- **radar1_par['offset']**: -4




 
