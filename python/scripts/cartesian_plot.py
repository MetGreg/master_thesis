'''
Radar data of pattern or dwd radar will be plotted on a cartesian grid, 
its parameters can be defined in parameters.py. The plot will exactly 
cover the pattern area.

'''





########################################################################
### modules and functions ###
########################################################################

'''
Imports modules and functions needed for this program.

'''
# Python modules
import re      
import numpy as np                                                      
from pathlib import Path

# MasterModule
from MasterModule.cartesian_grid import CartesianGrid
from MasterModule.dwd_radar import DwdRadar
from MasterModule.pattern_radar import PatternRadar
from MasterModule.refl_plot import ReflPlot

# Parameter
import parameters as par
    
# Functions
from functions import rotate_pole
    
    

                

########################################################################
### parameters ###
########################################################################

'''
Some parameters, that can be set in parameters.py.

'''
grid_par = par.grid_par 
radar_par = par.radar_par 
plot_par = par.plot_par 





########################################################################
### Create objects ###
########################################################################

'''
Creates following objects:
- DwdRadar or PatternRadar (depending on input file) to read in data.
- CartesianGrid for interpolating data to cartesian grid.
- ReflPlot for plotting reflectivity data on cartesian grid.

Creates the correct radar object after scanning (using regular 
expressions) the file_name, which contains information about the radar
and processing step.

'''
# dwd radars
if re.search('dwd_rad_boo', radar_par['file']):
    radar = DwdRadar(radar_par)
    
# pattern radars
elif re.search('level2', radar_par['file']):
    radar = PatternRadar(radar_par)
    
# Create cartesian grid object
car_grid = CartesianGrid(grid_par)

# Create ReflPlot object
refl_plot = ReflPlot(grid_par, plot_par)           





########################################################################
### Read in data ###
########################################################################

'''
Reads in data, by calling the read_file method.

'''
radar.read_file(radar_par)





########################################################################
### artificially increase azimuth resolution ###
########################################################################

'''
The azimuth resolution of the radar usually is 1°. To avoid 
empty grid boxes in the new cartesian grid, the azimuth 
resolution is increased artificially. 

'''
data_inc_res = radar.increase_azi_res()





########################################################################
### calculate coordinates of middle pixel for each box ###
########################################################################

'''
Coordinates of data are given at specific points, but are
valid for a box. 
This method calculates for each grid box the polar coordinates 
of the middle pixel out of the given coordinates at the edge of
the box.

'''   
mid_coords = radar.get_middle_pixel() 





########################################################################
### transform polar coordinates to lon/lat ###
########################################################################

'''
Transformation of polar coordinates of grid boxes (middle pixel) to 
cartesian coordinates, using a wradlib function.

'''
# Create numpy meshgrid, to obtain all combinations
r, az = np.meshgrid(mid_coords.range_, mid_coords.azi)

# Transform polar to cartesian coordinates
cart_coords = radar.polar_to_cartesian(r, az)





########################################################################
### rotated pole transformation ###
########################################################################

'''
Transform the cartesian coordinates to rotated pole coordinates using
a function from Claire Merker.

'''
# Rotated_coords.shape=(360,600,3), (azi,range,[lon,lat,height])
coords_rot = rotate_pole(cart_coords.lon, cart_coords.lat) 
lon = coords_rot[:,:,0]
lat = coords_rot[:,:,1]




########################################################################
### Check/Create index-matrix ###
########################################################################

'''
Radar data in rotated pole coordinates will be interpolated to the
cartesian grid, by averaging the reflectivity values of all data
points falling into the same grid box. For a given cartesian grid
and a given radar, always the same data points fall into the same
grid boxes. --> This information doesn't need to be calculated each 
time, but can be saved to a dat.file. 
--> Check, if such a file is present already for the current radar
and cartesian grid. If not, call method to create it.

'''
# Name of the index file
index_file = (
    '../index_matrix/index_matrix_'
    + str(radar.name)
    + '_'
    + str(car_grid.corners.lon_start)
    + '_'
    + str(car_grid.corners.lon_end)
    + '_'
    + str(car_grid.corners.lat_start)
    + '_'
    + str(car_grid.corners.lat_end)
    + '_'
    + str(car_grid.res_m)
    + '_'
    + str(radar.res_fac)
    + '_'
    + str(radar.offset)
    + '.dat'
    )

# Path is used to check, if the file exists
index_matrix = Path(index_file)

# If file doesn't exist, create it
if not index_matrix.is_file():
    car_grid.create_index_matrix(index_file, lon, lat)





########################################################################
### Interpolate radar data to cartesian grid ###
########################################################################

'''
Interpolates radar data to the new cartesian grid, by averaging all
data points falling into the same grid box of the new cartesian grid. 
Due to noise and dbz beeing a logarithmic unit, 'no rain' can have a 
large spread in dbz units. --> Dbz values smaller than 5 dbz will
be set to 5, to avoid large differences at low reflectivity.

'''
# Interpolate radar data to cartesian grid
refl = car_grid.data2grid(index_file, data_inc_res)

# Set reflectivities smaller than 5 to 5 (since no rain not def)
refl[refl < plot_par['rain_th']] = plot_par['rain_th']




########################################################################
### plot data ###
########################################################################

'''
Plots data on the new cartesian grid.

'''
# Create title
title = (
    str(radar.name)
    +'-data: '
    + str(radar.data.time_start.time())
    + ' - '
    + str(radar.data.time_end.time())
    +'\n'
    + str(radar.data.time_end.date())
    )

# Make plot
refl_plot.make_plot(refl, title)
