#program to plot radar data

'''
This program plots pattern radar data. 
'''





########################################################################
### modules ###
########################################################################

'''
import modules 
'''

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from datetime import datetime




########################################################################
### parameters ###
########################################################################

'''
Define parameters
'''

minute = 45





########################################################################
### read in data ###
########################################################################

'''
read in all attributes needed to plot the data
'''

#name of file
file_name    = '/scratch/uni/m4t/u300639/master_thesis'  \
               '/data/pattern/lawr/HHG/level2/2016/06/07'\
               '/m4t_HHG_wrx00_l2_dbz_v00_20160607030000.nc'

#open file
nc           = Dataset(file_name, mode='r')

#reflectivity array
dbz          = nc.variables       \
                ['dbz_ac1'][:]\
                [minute*2] 

#get time
time         = nc.variables['time'][:][minute*2]
time = datetime.utcfromtimestamp(time).strftime('%d.%m.%Y %H:%M')

#array of to data points corresponding range coordinates
range_coords = nc.variables['range'][:]

#array of to data points corresponding azimuth coordinates
azi_coords   = nc.variables['azi'][:]

#create mehsgrid to get all combinations of range and azimuth
r,theta      = np.meshgrid(range_coords,azi_coords)

#make angle, range and reflectivity arrays 1-D
r            = np.reshape(r,len(range_coords)*len(azi_coords))
theta        = np.reshape(
                np.pi/180*theta,len(range_coords)*len(azi_coords)
                )
refl = np.reshape(dbz,len(range_coords)*len(azi_coords))





########################################################################
### plot ###
########################################################################

'''
plots data 
'''



ax = plt.subplot(111, polar = True)
sct = ax.scatter(theta,r,c=refl,s= 10,cmap=cm.jet,linewidths = 0)
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
plt.colorbar(sct)
plt.title(time)
plt.show()
