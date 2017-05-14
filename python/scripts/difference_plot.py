'''
This program plots differences between two radar images after 
interpolating the radar data to the same cartesian grid.

'''





########################################################################
### modules and functions ###
########################################################################

'''
Import all modules and functions needed for this program.

'''
# Python modules
import re
import numpy as np
from pathlib import Path

# MasterModule
from MasterModule.cartesian_grid import CartesianGrid
from MasterModule.dwd_radar import DwdRadar
from MasterModule.pattern_radar import PatternRadar
from MasterModule.pattern_radar_v2 import PatternRadarV2
from MasterModule.refl_diff_plot import ReflDiffPlot

# Parameter
import parameters as par

# Functions
from functions import rotate_pole





########################################################################
### parameters, lists ###
########################################################################

'''
Get parameters. Parameters can be set in parameters.py.

'''
# Parameters
grid_par = par.grid_par 
radar1_par = par.radar1_par 
radar2_par = par.radar2_par 
plot_par = par.plot_par 

# Lists
l_refl = [] #reflectivity matrices of radars





########################################################################
### Create objects ###
########################################################################

'''
Creates all objects needed:
- Dwd or Pattern (depending on input file) to read in data
- CartesianGrid for interpolating data to Cartesian Grid
- ReflDiffPlot for plotting differences in reflectivity

Creates the correct radar object after scanning (using regular 
expressions) the file_name, which contains information about the radar
and processing step.

'''
# 1st radar
# dwd radars
if re.search('dwd_rad_boo', radar1_par['file']):
    radar1 = DwdRadar(radar1_par)
# pattern with version1 processing
elif re.search('version1', radar1_par['file']):
    radar1 = PatternRadar(radar1_par)
# pattern with version2 processing
elif re.search('version2', radar1_par['file']):
    radar1 = PatternRadarV2(radar1_par)

# 2nd radar
# dwd radars
if re.search('dwd_rad_boo', radar2_par['file']):
    radar2 = DwdRadar(radar2_par)
# pattern with version1 processing
elif re.search('version1', radar2_par['file']):
    radar2 = PatternRadar(radar2_par)
# pattern with version2 processing
elif re.search('version2', radar2_par['file']):
    radar2 = PatternRadarV2(radar2_par)

# Create list of both radar objectives, for easy looping
radars = [radar1, radar2]

# CartesianGrid object
car_grid = CartesianGrid(grid_par) 

# ReflDiffPlot object
refl_diff_plot = ReflDiffPlot(grid_par, plot_par)

      



####################################################################
### read in data ###
####################################################################

'''
Read in the data.

'''
radar1.read_file(radar1_par)
radar2.read_file(radar2_par)
    
    
    
    
    
########################################################################
### Main Loop ###
########################################################################

'''
A lot of calculations are the same for both radars. These common
calculations are done in this main loop:
 - increase azimuth resolution
 - calculate middle pixel polar coordinates
 - calculate cartesian coordinates out of polar coords
 - calculate rotated pole coordinates out of cartesian coords
 - create index matrix
 - interpolate data to cartesian grid

'''
# Loop through both radars
for radar in radars:
    



    
    ####################################################################
    ### artificially increase azimuth resolution ###
    ####################################################################
    
    '''
    The azimuth resolution of the radar usually is 1°. To avoid 
    empty grid boxes in the new cartesian grid, the azimuth 
    resolution is increased artificially. 
    
    '''
    data_inc_res = radar.increase_azi_res()
    
    
    
    
    
    ####################################################################
    ### calculate coordinates of middle pixel for each box ###
    ####################################################################
    
    '''
    Coordinates of data are given at specific points, but are
    valid for a box. 
    This method calculates for each grid box the polar coordinates 
    of the middle pixel out of the given coordinates at the edge of
    the box.
   
    '''
    mid_coords = radar.get_middle_pixel() 
    
    
    
    
    
    ####################################################################
    ### transform polar coordinates to lon/lat ###
    ####################################################################
    
    '''
    Transformation of polar coordinates of grid boxes (middle pixel) to 
    cartesian coordinates, using a wradlib function.
    
    '''
    # Create numpy meshgrid, to obtain all combinations
    r, az = np.meshgrid(mid_coords.range_, mid_coords.azi)
    
    # Get cartesian coordinates of radar data
    cart_coords = radar.polar_to_cartesian(r, az)
    
    
    
    
    
    ####################################################################
    ### rotated pole transformation ###
    ####################################################################
    
    '''
    Transform the cartesian coords to rotated pole coordinates using
    a function from Claire Merker.
    
    '''
    # coords_rot.shape=(360,600,3), (azi,range,[lon,lat,height])
    coords_rot = rotate_pole(cart_coords.lon, cart_coords.lat) 
    lon = coords_rot[:,:,0]
    lat = coords_rot[:,:,1]
    
    
    
    
    
    ####################################################################
    ### Check/Create index-matrix ###
    ####################################################################

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




      
    ####################################################################
    ### Interpolate radar data to cartesian grid ###
    ####################################################################
    
    '''
    Interpolates radar data to the new cartesian grid, by averaging all
    data points falling into the same grid box of the new 
    cartesian grid. 
    Due to noise and dbz beeing a logarithmic unit, 'no rain' can have a 
    large spread in dbz units. --> Reflectiviy smaller than 5 dbz, 
    will be set to 5,to avoid having large differences at low 
    reflectivity.
    
    '''
    # Interpolate reflectivity to the new grid
    refl = car_grid.data2grid(index_file, data_inc_res)
    
    # Set reflectivities smaller than 5 to 5
    refl[refl < plot_par['rain_th']] = plot_par['rain_th']
    
    # Append inverted reflectivity matrix to list
    l_refl.append(refl)
    




########################################################################
### plot differences ###
########################################################################

'''
Plot the differences between the two radars on the cartesian grid by
calling the plot_diff method of the cartesian grid objectiv.

'''
# Title                           
title = (
    radar2.name
    + '('
    + str(radar2.data.time_start.time())
    + ') minus '
    + radar1.name
    + '('
    + str(radar1.data.time_start.time())
    + ')\n'
    + str(radar1.data.time_start.date())
    )
        
# plot differences
refl_diff_plot.make_plot(
    l_refl[0], l_refl[1], radar1.name, radar2.name, title
    )
