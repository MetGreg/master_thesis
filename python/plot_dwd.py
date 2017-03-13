###program to plot dwd data






########################################################################
### modules ###
########################################################################

'''
import modules
'''

import numpy as np
import h5py
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.cm as cm





########################################################################
### read in data ###
########################################################################

'''
reads in dwd data
'''

#file name
file_name = '../data/dwd_rad_boo/sweeph5allm/2016/06/07/'\
            'ras07-pcpng01_sweeph5allm_any_00-'\
            '2016060716003300-boo-10132-hd5'

#open file
with h5py.File(file_name,'r') as h5py_file:
    
    #factor to correct the dwd refl to ordinary dbz values 
    gain       = h5py_file.get('dataset1/data1/what').attrs['gain']
    
    #Offset, to correct the dwd refl to ordinary dbz values 
    offset     = h5py_file.get('dataset1/data1/what').attrs['offset']
       
    #uncorrected data 
    refl       = h5py_file.get('dataset1/data1/data')
    
    #corrected data
    refl_cor   = refl * gain + offset 

    #time at which scan started in epochs (linux time)                            
    time_start = h5py_file.get('how').attrs['startepochs']
    
    #number of radius bins (600 --> 250m steps up to 150000m)                           
    r_bins     = h5py_file.get('dataset1/where').attrs['nbins']

    #range of first measurement                    
    r_start    = h5py_file.get('dataset1/where').attrs['rstart']

    #distance between 2 measurements on radius-axis (250m)                    
    r_steps    = h5py_file.get('dataset1/where').attrs['rscale'] 

    #number of azimuth rays(360 --> 1° steps)
    azi_rays   = h5py_file.get('dataset1/where').attrs['nrays'] 
    
    #azimuth angle of first measurement
    azi_start  = h5py_file.get('dataset1/where').attrs['startaz']
            
    #angle step between 2 measurements
    azi_steps  = h5py_file.get('dataset1/how').attrs['angle_step']





########################################################################
### create 1-D arrays ###
########################################################################

'''
to plot data, arrays must be 1D
'''

#create array of azi coords
azi_coords = np.arange(azi_start,azi_steps*azi_rays, azi_steps)

#create array of range coords
r_coords   = np.arange(r_start,r_steps*r_bins, r_steps)

#create np.meshgrid for all possible combinations of range and azimuth
r, theta   = np.meshgrid(r_coords,azi_coords)

#create 1-D arrays
r          = np.reshape(r,len(azi_coords)*len(r_coords))
theta      = np.reshape(np.pi/180*theta,len(azi_coords)*len(r_coords))
refl       = np.reshape(refl_cor,len(azi_coords)*len(r_coords))





########################################################################
### plot ###
########################################################################

'''
plots data 
'''

time = datetime.utcfromtimestamp(time_start).strftime('%d.%m.%Y %H:%M')
ax  = plt.subplot(111, polar = True)
sct = ax.scatter(theta,r,c=refl,s= 10,cmap=cm.jet,linewidths = 0)
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
plt.colorbar(sct)
plt.title(time)
plt.show()

