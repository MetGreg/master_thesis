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
from MasterModule.pattern_radar_v2 import PatternRadarV2

# Parameter
import parameters as par





########################################################################
### parameters ###
########################################################################

'''
Some parameters, that can be set in parameters.py.
Also, lists of program are defined here.

'''
radar_par = par.radar1_par   
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
if re.search('dwd', radar_par['file']):
    radar = DwdRadar(radar_par)
# pattern with version1 processing
elif re.search('version1', radar_par['file']):
    radar = PatternRadar(radar_par)
# pattern with version2 processing
elif re.search('version2', radar_par['file']):
    radar = PatternRadarV2(radar_par)




    
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
