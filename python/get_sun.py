###program to find azimuth angle of sun

'''
We think that the radars calibration is off for a few degrees.
The theoretically angle of the sun as seen from the radar site at a 
given time and date are well known.
This program calculates the angle, as seen by the radar, to compare it
to the real angle.

Program only works, if sun can be seen in radar image, and no rain is 
present at that time.
'''





########################################################################
### modules ###
########################################################################

'''
import modules
'''

from netCDF4 import Dataset
from datetime import datetime





########################################################################
### parameters, lists ###
########################################################################

'''
Define parameters and lists
'''

#parameters
minute = 45

#lists
l_refl = []





########################################################################
### read in data ###
########################################################################

'''
read in data
'''

#name of file
file_name    = '/scratch/uni/m4t/u300639/master_thesis'  \
               '/data/pattern/lawr/HHG/level2/2016/06/07'\
               '/m4t_HHG_wrx00_l2_dbz_v00_20160607030000.nc'

#open file
nc = Dataset(file_name,'r')

#reflectivity array
dbz          = nc.variables       \
                ['dbz_ac1'][:]\
                [minute*2] 

#get time
time         = nc.variables['time'][:][minute*2]
time = datetime.utcfromtimestamp(time).strftime('%d.%m.%Y %H:%M')





########################################################################
### get sun angle ###
########################################################################

'''
get the angle of the sun, by looping through all ranges and azimuths
and find the azimuth angle, at wich the reflectivity reaches its maximum
(integrated over all ranges). This is the angle to the sun.
'''

#loop through azimuth angles
for line in dbz:
    
    #set sum to zero for each azimuth angle
    refl_sum = 0
    
    #loop through ranges
    for col in line:
        
            #add reflectivity to sum variable
            refl_sum += col
    
    #append list of integrated reflectivites 
    l_refl.append(refl_sum)
        

angle = l_refl.index(max(l_refl))
print(angle)
