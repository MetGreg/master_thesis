get_sun.py
==========

This script calculates the angle of the sun relativ to the radar site.
At sunrise and sunset, the sun is visible in the radar image. Using the
signal of the sun, this script calculates the angle, at which the sun
is seen by the radar.

.. note::
   The script only makes sense for data at sunrise or sunset, since 
   only then the sun is seen in the radar image.

.. note::
   The script only makes sense for cases of no rain, since the rain 
   signal otherwise outweighs the suns signal.
   
.. note::
   The script only works for pattern level 2 data, since only the 
   PATTERN radar catches the signal of the sun and only at the 
   processing step 2 clutter and noise are removed. 

In parameters.py the following parameters incluence the output:

- **radar1_par['file']**: Name of the data file.

In case of PATTERN data, also these parameters can be set:

- **radar1_par['minute']**: Minute of hourly data.

Example
-------

For PATTERN data at 07.06.2016 at 03:40 UTC, this script calculates
an angle to the sun of 61°.

