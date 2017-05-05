'''
Calculates and plots heights of middle of pattern or dwd radar beam.

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

# MasterModule
from MasterModule.cartesian_grid import CartesianGrid                           
from MasterModule.dwd_radar import DwdRadar 
from MasterModule.heights_plot import HeightsPlot  
from MasterModule.pattern_radar import PatternRadar

# Parameters
import parameters as par 

# Functions
from functions import rotate_pole





########################################################################
### parameters ###
########################################################################

'''
Get parameters. Parameters can be set in parameters.py

'''
grid_par = par.grid_par
radar_par = par.radar_par
plot_par = par.plot_par





########################################################################
### Create objects ###
########################################################################

'''
Creates following objects:
- DwdRadar or PatternRadar (depending on input file) to read in data
- CartesianGrid for interpolating data to Cartesian Grid
- HeightsPlot for plotting heights

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

# Cartesian Grid object
car_grid = CartesianGrid(grid_par)

# HeightsPlot object
heights_plot = HeightsPlot(grid_par, plot_par)





########################################################################
### Read in data ###
########################################################################

'''
Reads in data, by calling the read_file method.

'''
radar.read_file(radar_par)





########################################################################
### Get rotated site coords ###
########################################################################

'''
The method to calculate beam heights needs rotated pole coords of radar 
site. 
--> Calculate rotated coords by using function from Claire Merker.

'''    
# Transform site coords to rotated pole coords
rot_site = rotate_pole(
    np.array(radar.data.lon_site), np.array(radar.data.lat_site)
    )
        
# Get lon and lat site
lon_site_rot = rot_site[0][0]
lat_site_rot = rot_site[0][1]





########################################################################
### Get beam height ###
########################################################################

'''
Calculates the height of the beam for each grid box of cartesian grid,
by calling the get_beam_height method. 

'''
heights = car_grid.get_beam_height(
    lon_site_rot, lat_site_rot, radar.data.ele
    )





########################################################################
### plot beam heights ###
########################################################################

'''
Plots heights of radar beam as isolines.

'''
# Title of plot
title = radar.name + ' - heights'

# Make plot
heights_plot.make_plot(heights, title)
