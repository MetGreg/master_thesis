'''
This program plots radar data (dwd or pattern).

'''





########################################################################
### modules ###
########################################################################

'''
Import all modules needed for this program.

'''
# Python modules
import re

# MasterModule
from MasterModule.dwd_radar import DwdRadar
from MasterModule.pattern_radar import PatternRadar

# Parameter
import parameters as par





########################################################################
### parameters ###
########################################################################

'''
Some parameters, that can be set in parameters.py.
Also, lists of program are defined here.

'''
radar_par = par.radar_par   
grid_par = par.grid_par   
plot_par = par.plot_par   





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
# dwd radars
if re.search('dwd_rad_boo', radar_par['file']):
    radar = DwdRadar(radar_par)

# pattern radars
elif re.search('level2', radar_par['file']):
    radar = PatternRadar(radar_par)




    
########################################################################
### read in data ###
########################################################################

'''
Reads in data.

'''
radar.read_file(radar_par)





########################################################################
### plot ###
########################################################################

'''
Plots data 

'''
radar.plot()
