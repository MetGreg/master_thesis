#program to plot radar data as it is

'''
This program plots radar data (dwd or pattern)
'''





########################################################################
### modules ###
########################################################################

import parameters as par
from MasterModule.MainRadar import Radar
from MasterModule.DWDRadar import Dwd
from MasterModule.PatternRadar import Pattern
import re
import wradlib





########################################################################
### parameters ###
########################################################################

'''
Some parameters, that can be set in parameters.py.
Also, lists of program are defined here.
'''

#parameters
file_name = par.radar[0]  #name of data file
minute    = par.radar[1]  #minute of file to be plotted (only for pat.)
proc_key  = par.radar[2]  #key for processing step (only for pat. radar)
res_fac   = par.radar[3]  #actor to incr. azimuth resolution 

#grid_par = [[[lon_start,lon_end],[lat_start,lat_end],
#            [lon_site,lat_site],max_range,resolution]]
offset    = par.offset    #offset for wrongly calibrated azimuth angle





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
### plot ###
########################################################################

'''
plots data 
'''

radar.plot()
