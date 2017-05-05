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
# Python modules
import re

# MasterModule
from MasterModule.pattern_radar import PatternRadar

# Parameters
import parameters as par





########################################################################
### parameters, lists ###
########################################################################

'''
Get parameters. Parameters can be set in parameters.py

'''
# Parameter
radar_par = par.radar_par  

# Lists
l_refl = [] #list with entry for each azimuth with integr. refl. 





########################################################################
### Intercept wrong input files ###
########################################################################

'''
This program only works for pattern radars. Check, if input file is
pattern data.

'''
assert(
    re.search('level2', radar_par['file'])
    ), 'wrong input file, only pattern level2 data works'





########################################################################
### Create objects ###
########################################################################

'''
Creates objects needed for this program:
 - Pattern object to read in data.

'''
radar = PatternRadar(radar_par)





########################################################################
### read in data ###
########################################################################

'''
Reads in data.

'''
radar.read_file(radar_par)





########################################################################
### get sun angle ###
########################################################################

'''
Get the angle of the sun, by looping through all ranges and azimuths
and find the azimuth angle, at wich the reflectivity reaches its maximum
(integrated over all ranges). This is the angle to the sun. (Assuming
the sun gives the only echo in this image)

'''
# Loop through azimuth angles
for line in radar.data.refl:
    
    # Set sum to zero for each azimuth angle
    refl_sum = 0
    
    # Loop through ranges
    for col in line:
        
            # Add reflectivity to sum variable
            refl_sum += col
    
    # Append list of integrated reflectivites 
    l_refl.append(refl_sum)
        
# Find angle with maximum integrated reflectivity
angle = l_refl.index(max(l_refl))

# Print angle
print(angle)
