'''
This program plots differences in height between two radars (PATTERN or
DWD) on a cartesian grid.

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
from MasterModule.pattern_radar_v2 import PatternRadarV2

# Functions
from functions import rotate_pole

# Parameter
import parameters as par 





########################################################################
### parameters, lists ###
########################################################################

'''
Get parameters. Parameters can be set in parameters.py

'''
# Parameters
radar1_par = par.radar1_par 
radar2_par = par.radar2_par 
grid_par = par.grid_par   
plot_par = par.plot_par  

# Lists
l_heights = [] #list of beam height arrays (one entry for each radar)





########################################################################
### Create objects ###
########################################################################

'''
Creates all objects needed:
- DwdRadar or PatternRadar (depending on input file) to read in data.
- CartesianGrid for interpolating data to Cartesian Grid.
- HeightsPlot for plotting height differences.

Creates the correct radar object after scanning (using regular 
expressions) the file_name, which contains information about the radar
and processing step.

'''
# First radar
# For dwd radars
if re.search('dwd', radar1_par['file']):
    radar1 = DwdRadar(radar1_par)
# pattern with version1 processing
elif re.search('version1', radar1_par['file']):
    radar1 = PatternRadar(radar1_par)
# pattern with version2 processing
elif re.search('version2', radar1_par['file']):
    radar1 = PatternRadarV2(radar1_par)

# Second radar
# For dwd radars
if re.search('dwd', radar2_par['file']):
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

# HeightsPlot object 
heights_plot = HeightsPlot(grid_par, plot_par)





########################################################################
### Read files ###
########################################################################

'''
Read in data of the two radar data files.

'''
radar1.read_file(radar1_par)
radar2.read_file(radar2_par)





########################################################################
### Main Loop ###
########################################################################

'''
Some calculations are the same for both radars. These common
calculations are done in this main loop:
 - calculate rotated coordinates of site
 - calculate beam heights

'''
# Loop through both radars
for radar in radars:
    




    ####################################################################
    ### rotated site coords ###
    ####################################################################

    '''
    Method to calculate beam heights needs the rotated pole coordinates
    of radar site.
    --> calculate these rotated pole coordinates using a function of
    Claire Merker.
    
    '''
    # Transform site coords to rotated pole coords
    rot_site = rotate_pole(
        np.array(radar.data.lon_site), np.array(radar.data.lat_site)
        )
    
    # Get rotated lon and lat of site
    lon_site_rot = rot_site[0][0]
    lat_site_rot = rot_site[0][1]
    
    



    ####################################################################
    ### get beam heights ###
    ####################################################################

    '''
    Calculates the height of the beam for each grid box, by calling the
    get_beam_height - method of the CartesianGrid object.
    Height array is then appended to l_heights list, for later
    calculation of the height differences.
    
    '''
    # Get heights
    heights = car_grid.get_beam_height(
        lon_site_rot, lat_site_rot, radar.data.ele
        )

    # Append heights to l_heights to subtract them later
    l_heights.append(heights)





########################################################################
### Get height differences ###
########################################################################

'''
Calculate height differences by subtracting the height arrays.

'''
height_diff = l_heights[1] - l_heights[0]





########################################################################
### plot beam heights ###
########################################################################

'''
Plots heights of radar beam as isolines.

'''
# Title of plot
title = radar2.name + ' minus ' + radar1.name + ' - heights' 

# Plot height differences
heights_plot.make_plot(height_diff, title)
