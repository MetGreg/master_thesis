###parameter file for plotting radar data on a new defined cartesian grid

'''
In this file, all parameters used to plot radar data on a new defined grid
can be set.
'''





########################################################################
### new cartesian grid ###
########################################################################

'''
parameters specific for the new defined cartesian grid
'''

#lon_start			= 'min'
#lat_start			= 'min'
#lon_end			= 'max'
#lat_end			= 'max'
lon_start			= 0.0516949287345										#starting longitude
lon_end				= 0.410334898692										#ending longitude
lat_start			= -0.547853479291										#starting latitude
lat_end				= -0.18922092829										#ending latitude
resolution			= 250													#resolution of the new cartesian grid in m
grid_par			= [[lon_start,lon_end],[lat_start,lat_end],resolution] 	#grid parameters in one list			









########################################################################
### pattern radar ###
########################################################################

'''
parameters specific for pattern radar data
'''

minute				= 1								#pattern data has one file per hour. This parameter defines which minute of the hour shall be plotted. (Minute 1 == first measurement, minute 60 == last measurement of hour)
refl_key			= 'dbz_ac2'						#level 2 pattern data has two processing steps. Define here which one shall be plotted. dbz_ac1 = step1, dbz_ac2 = step2





########################################################################
### general ###
########################################################################

'''
general paramaters
'''

res_factor			= 10		#factor by which the azimuth-resolution will be increased

###file_names
#file_name 			= './data/dwd_rad_boo/sweeph5allm/2016/06/07/ras07-pcpng01_sweeph5allm_any_00-2016060716003300-boo-10132-hd5'
#file_name			= './data/level1_hdcp2/2016/06/m4t_HHG_wrx00_l1_dbz_v00_20160607160000.nc'
file_name			= './data/level2_hdcp2/2016/06/m4t_HHG_wrx00_l2_dbz_v00_20160607160000.nc'
