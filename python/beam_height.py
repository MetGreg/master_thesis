###Calculates heights of radar beams for pattern or dwd radar

'''
'''





########################################################################
### modules ###
########################################################################

'''
imports modules needed for this program
'''

import re                                    
import parameters as par                     
import wradlib  
import numpy as np                             
from MasterModule.MainRadar     import Radar 
from MasterModule.DWDRadar      import Dwd   
from MasterModule.PatternRadar  import Pattern
from MasterModule.CartesianGrid import CartesianGrid 





########################################################################
### parameters ###
########################################################################

'''
Get parameters. Parameters can be set in parameters.py
'''

file_name = par.radar[0] #radar data file to be used
minute    = par.radar[1] #minute of file to be plotted (only for pat.)
proc_key  = par.radar[2] #key for processing step (only for pat. radar)
res_fac   = par.radar[3] #actor to incr. azimuth resolution 
offset    = par.offset   #offset for wrongly calibrated azimuth angle
grid_par  = par.grid_par #list of grid parameters for the cart. grid
isolines  = par.isolines #array of height isolines to be plotted
tick_nr   = par.tick_nr  #nr of grid lines to be plotted





########################################################################
### read in data ###
########################################################################

'''
Data is saved to a Radar-Object. The method used to read in the data
differs, depending on the radar that shall be plotted. Information 
about the radar and processing step is in the name of the data file.
--> scan data file name to find out which radar is going to be plotted
and create corresponding radar object.
'''

#scan data file and create corresponding radar object
if re.search('dwd_rad_boo',file_name):
    radar = Dwd(file_name,res_fac)
elif re.search('level1',file_name):
    radar = Pattern(file_name,minute,offset,'dbz',res_fac)
elif re.search('level2',file_name):
    radar = Pattern(file_name,minute,offset,proc_key,res_fac)

#read in data
radar.read_file()





########################################################################
### Get beam height ###
########################################################################

'''
Calculates the height of the beam for each grid box of cartesian grid.
'''

#create Cartesian Grid object
car_grid = CartesianGrid(grid_par)

#get distance of grid box to radar site 
a_dist = car_grid.dist_grid2radar(radar)

#get height of radar beam at each grid box
heights = wradlib.georef.beam_height_n(a_dist,radar.data.ele)

print(heights.shape)




########################################################################
### plot beam heights ###
########################################################################

'''
Plots heights of radar beam as isolines.
'''

#plot heights
car_grid.plot_heights(heights,isolines,tick_nr,radar)
