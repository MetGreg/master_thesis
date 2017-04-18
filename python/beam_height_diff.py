###Plot height differences

'''
This program plots differences in height between two radars (pattern or
dwd) on a cartesian grid.
'''





########################################################################
### modules and functions ###
########################################################################

'''
Imports modules and functions needed for this program.
'''

#python modules
import re                    
import numpy as np  

#MasterModule 
from MasterModule.cartesian_grid import CartesianGrid                          
from MasterModule.dwd_radar      import DwdRadar  
from MasterModule.heights_plot   import HeightsPlot
from MasterModule.pattern_radar  import PatternRadar

#functions
from functions import rotate_pole

#parameter
import parameters as par 





########################################################################
### parameters, lists ###
########################################################################

'''
Get parameters. Parameters can be set in parameters.py
'''

#parameters
radar1_par = par.radar1_par #radar parameter of first radar
radar2_par = par.radar2_par #radar parameter of second radar
grid_par   = par.grid_par   #grid parameter
plot_par   = par.plot_par   #plot parameter

#file_name
file1      = radar1_par[0]
file2      = radar2_par[0]

#offset of radar
offset     = par.offset

#lists
l_heights  = [] #list of beam height arrays (one entry for each radar)





########################################################################
### Create objects ###
########################################################################

'''
Creates all objects needed:
- DwdRadar or PatternRadar (depending on input file) to read in data
- CartesianGrid for interpolating data to Cartesian Grid
- HeightsPlot for plotting height differences

Creates the correct radar object after scanning (using regular 
expressions) the file_name, which contains information about the radar
and processing step.
'''



##################### 1st radar ########################################

#for dwd radars
if re.search('dwd_rad_boo',file1):
    radar1 = DwdRadar(radar1_par)

#for pattern radars
elif re.search('level2',file1):
    radar1 = PatternRadar(radar1_par,offset)



##################### 2nd radar ########################################

#for dwd radars
if re.search('dwd_rad_boo',file2):
    radar2 = DwdRadar(radar2_par)

#for pattern radars
elif re.search('level2',file2):
    radar2 = PatternRadar(radar2_par,offset)

#create list of both radar objectives, for easy looping
radars = [radar1,radar2]



#################### CartesianGrid object ##############################
car_grid = CartesianGrid(grid_par) 



#################### HeightsPlot object ################################
heights_plot = HeightsPlot(grid_par,plot_par)





########################################################################
### Main Loop ###
########################################################################

'''
A lot of calculations are the same for both radars. These common
calculations are done in this main loop:
 - Read file
 - calculate rotated coordinates of site
 - calculate beam heights
'''

#loop through both radars
for radar in radars:
    
        



    ####################################################################
    ### read in data ###
    ####################################################################
    
    '''
    Data is saved to a Radar-Object. The method used to read in the data
    differs, depending on the radar. (Different radar --> different 
    object --> different read-method)
    '''

    #read in data
    radar.read_file()





    ####################################################################
    ### rotated site coords ###
    ####################################################################

    '''
    Method to calculate beam heights needs the rotated pole coordinates
    of radar site.
    --> calculate these rotated pole coordinates using a function of
    Claire Merker.
    '''

    #coordinates of radar site
    site = (radar.data.lon_site,radar.data.lat_site)
    
    #transform site coords to rotated pole coords
    rot_site = rotate_pole(np.array(site[0]), np.array(site[1]))
    
    #bring rot_site to correct shape
    rot_site = (rot_site[0][0], rot_site[0][1])
    
    



    ####################################################################
    ### get beam heights ###
    ####################################################################

    '''
    Calculates the height of the beam for each grid box, by calling the
    get_beam_height - method of the CartesianGrid object.
    Height array is then appended to l_heights list, for later
    calculation of the height differences.
    '''

    #get heights
    heights = car_grid.get_beam_height(rot_site,radar.data.ele)

    #append heights to l_heights to subtract them later
    l_heights.append(heights)





########################################################################
### Get height differences ###
########################################################################

'''
Calculate height differences by subtracting the height arrays.
'''

#subtract height arrays to get height differences
height_diff = l_heights[1] - l_heights[0]





########################################################################
### plot beam heights ###
########################################################################

'''
Plots heights of radar beam as isolines.
'''

#title of plot
title = radar2.name + ' minus ' + radar1.name + ' - heights' 

#plot height differences
heights_plot.make_plot(height_diff,title)
