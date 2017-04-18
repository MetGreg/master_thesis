###program to find azimuth angle of sun

'''
This program calculates the angle of the sun, as seen by the pattern 
radar.

Program only works, if sun can be seen in radar image, and no rain is 
present at that time.
'''





########################################################################
### modules ###
########################################################################

'''
Import modules needed for this program.
'''

#python modules
import re
from netCDF4 import Dataset
from datetime import datetime

#MasterModule
from MasterModule.pattern_radar import PatternRadar

#parameters
import parameters as par





########################################################################
### parameters, lists ###
########################################################################

'''
Get parameters. Parameters can be set in parameters.py
'''

#parameter
radar_par = par.radar_par  #radar parameter

#file_name
file_name = radar_par[0]

#offset, by which pattern radar is wrong
offset    = par.offset

#lists
l_refl    = [] #list with entry for each azimuth with integr. refl. 




########################################################################
### Intercept wrong input files ###
########################################################################

'''
This program only works for pattern radars. Check, if input file is
pattern data.
'''

assert(re.search('level2',file_name)),\
    'wrong input file, only pattern level2 data works'

########################################################################
### Create objects ###
########################################################################

'''
Creates objects needed for this program:
 - Pattern object, to read in data.
'''


#create pattern object
radar = PatternRadar(radar_par,offset)





########################################################################
### read in data ###
########################################################################

'''
Reads in data.
'''

radar.read_file()





########################################################################
### get sun angle ###
########################################################################

'''
Get the angle of the sun, by looping through all ranges and azimuths
and find the azimuth angle, at wich the reflectivity reaches its maximum
(integrated over all ranges). This is the angle to the sun. (Assuming
the sun gives the only echo in this image)
'''

#loop through azimuth angles
for line in radar.data.refl:
    
    #set sum to zero for each azimuth angle
    refl_sum = 0
    
    #loop through ranges
    for col in line:
        
            #add reflectivity to sum variable
            refl_sum += col
    
    #append list of integrated reflectivites 
    l_refl.append(refl_sum)
        
#find angle with maximum integrated reflectivity
angle = l_refl.index(max(l_refl))

#print angle
print(angle)
