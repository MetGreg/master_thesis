###Plot beam heights

'''
Calculates and plots middle of beam heights of pattern or dwd radar.
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

#MasterModule modules  
from MasterModule.cartesian_grid import CartesianGrid                           
from MasterModule.dwd_radar      import DwdRadar 
from MasterModule.heights_plot   import HeightsPlot  
from MasterModule.pattern_radar  import PatternRadar

#parameters
import parameters as par 

#functions
from functions import rotate_pole





########################################################################
### parameters ###
########################################################################

'''
Get parameters. Parameters can be set in parameters.py
'''

#parameters
radar_par = par.radar_par #list of radar parameters
grid_par  = par.grid_par  #list of grid parameters
plot_par  = par.plot_par  #list of plot parameters

#name of file
file_name = radar_par[0]

#offset of pattern radar
offset    = par.offset




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



################# radar object #########################################

#for dwd radars
if re.search('dwd_rad_boo',file_name):
    radar = DwdRadar(radar_par)

#for pattern radars
elif re.search('level2',file_name):
    radar = PatternRadar(radar_par,offset)



############ Cartesian Grid object #####################################
car_grid = CartesianGrid(grid_par)



############ HeightsPlot object ########################################
heights_plot = HeightsPlot(grid_par,plot_par)





########################################################################
### Read in data ###
########################################################################

'''
Reads in data, by calling the read_file method.
'''

#read in data
radar.read_file()





########################################################################
### Get rotated site coords ###
########################################################################

'''
Method to calculate beam heights needs rotated pole coords of radar 
site. 
--> Calculate rotated coords by using function from Claire Merker.
'''

#coordinates of radar site
site = (radar.data.lon_site,radar.data.lat_site)
        
#transform site coords to rotated pole coords
rot_site = rotate_pole(np.array(site[0]), np.array(site[1]))
        
#bring rot_site to correct shape
rot_site = (rot_site[0][0], rot_site[0][1])





########################################################################
### Get beam height ###
########################################################################

'''
Calculates the height of the beam for each grid box of cartesian grid,
by calling the get_beam_height method. 
'''

#get heights
heights = car_grid.get_beam_height(rot_site,radar.data.ele)





########################################################################
### plot beam heights ###
########################################################################

'''
Plots heights of radar beam as isolines.
'''

#title of plot
title = radar.name + ' - heights'

#make plot
heights_plot.make_plot(heights,title)
