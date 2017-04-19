#Plot radar data

'''
This program plots radar data (dwd or pattern).
'''





########################################################################
### modules ###
########################################################################

'''
Import all modules needed for this program.
'''

#python modules
import re

#MasterModule
from MasterModule.dwd_radar     import DwdRadar
from MasterModule.pattern_radar import PatternRadar

#parameter
import parameters as par





########################################################################
### parameters ###
########################################################################

'''
Some parameters, that can be set in parameters.py.
Also, lists of program are defined here.
'''
#parameters
radar_par  = par.radar_par  #radar parameter 
grid_par   = par.grid_par   #grid parameter
plot_par   = par.plot_par   #plot parameter

#file_name
file_name  = radar_par[0]


#offset of radar
offset    = par.offset





########################################################################
### Create objects ###
########################################################################

'''
Creates following objects:
- Dwd or Pattern (depending on input file) to read in data

Creates the correct radar object after scanning (using regular 
expressions) the file_name, which contains information about the radar
and processing step.
'''

#for dwd radars
if re.search('dwd_rad_boo',file_name):
    radar = DwdRadar(radar_par)

#for pattern radars
elif re.search('level2',file_name):
    radar = PatternRadar(radar_par,offset)




    
########################################################################
### read in data ###
########################################################################

'''
Reads in data.
'''

#read in data
radar.read_file()





########################################################################
### plot ###
########################################################################

'''
Plots data 
'''

radar.plot()
