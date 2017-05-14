radar_plot.py
=============

This script creates simple plots of reflectivity using a 
`wradlib function <http://wradlib.org/wradlib-docs/0.9.0/generated/wradlib.vis.plot_cg_ppi.html#wradlib.vis.plot_cg_ppi>`_.

In parameters.py the following parameters incluence the output:

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

.. figure:: ../../../../plots/example_plots/radar_plot.png

The example image was created using the PATTERN data file for the 
7th June 2016 at 16:00 UTC with the following parameters:

- **radar1_par['res_fac']**: 1
- **radar1_par['offset']**: -4


