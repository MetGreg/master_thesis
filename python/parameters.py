#parameter file for plotting radar data on a new defined cartesian grid

'''
In this file, all parameters that are used to plot radar data on a new 
defined cartesian grid can be set.
'''





########################################################################
### new cartesian grid ###
########################################################################

'''
parameters specific for the new defined cartesian grid
'''

#maximal range of pattern radar in m
max_range = 19966.140625        

#rot. lon coord of radar site of pattern radar                                    
lon_site  = 0.23101493

#rot. lat coord of radar site of pattern radar                                            
lat_site  = -0.36853593    

#coordinates of grid                                    
lon_start = 0.0516949287345                                        
lon_end   = 0.410334898692                                        
lat_start = -0.547853479291                                        
lat_end   = -0.18922092829                                        

#resolution of the new cartesian grid in m
res       = 250    

#grid parameters in one list                                                
grid_par  = [[lon_start,lon_end],[lat_start,lat_end],
            [lon_site,lat_site],max_range,res]                         





########################################################################
### 1st radar ###
########################################################################

'''
parameters specific for the first radar
'''

#datafile of first radar
file1     = '../data/dwd_rad_boo/sweeph5allm/2016/06/07/ras07-pcpng01_sweeph5allm_any_00-2016060716003300-boo-10132-hd5'
#file1     = '../data/dwd_rad_boo/sweeph5allm/2015/07/29/ras07-pcpng01_sweeph5allm_any_00-2015072910203400-boo-10132-hd5'
#file1     = '/scratch/uni/m4t/u300639/master_thesis/data/pattern/lawr/HHG/level2/2016/06/07/m4t_HHG_wrx00_l2_dbz_v00_20160607160000.nc'

#minute of hourly files, that shall be plotted (only concerns pattern)
minute1   = 0                                

#key of proc. step to be plotted. Only concerns pattern.
#dbz_ac1 = step1, dbz_ac2 = step2
proc_key1 = 'dbz_ac1' 

#factor by which the azi. res. of 1st radar data will be increased	 
res_fac1  = 10  

#merge all 1st radar parameters to one list
radar1    = [file1,minute1,proc_key1,res_fac1]





########################################################################
### 2nd radar ###
########################################################################

'''
parameters specific for the second radar
'''

#data file of 2nd radar
file2     = '/scratch/uni/m4t/u300639/master_thesis/data/pattern/lawr/HHG/level2/2016/06/07/m4t_HHG_wrx00_l2_dbz_v00_20160607160000.nc'
#file2     = '/scratch/uni/m4t/u300639/master_thesis/data/pattern/lawr/HHG/level2/2015/07/29/m4t_HHG_wrx00_l2_dbz_v00_20150729100000.nc'

#minute of hourly files, that shall be plotted (only concerns pattern).
minute2   = 0.5    

#key of proc. step to be plotted. Only concerns pattern.
#dbz_ac1 = step1, dbz_ac2 = step2
proc_key2 = 'dbz_ac1' 

#factor by which the azi. res. of 2nd radar data will be increased
res_fac2  = 10        

#merge all 2nd radar parameters to one list
radar2    = [file2,minute2,proc_key2,res_fac2]





########################################################################
### plot ###
########################################################################

'''
parameters for plotting
'''

tick_nr = 10     #number of grid lines, that will be plotted as a grid
log_iso = True   #True --> plot rain area contours




########################################################################
### specific for cartesian_plot.py ###
########################################################################

'''
Cartesian_plot.py only plots one radar image. Define here which one.
'''

#define which of 2 radars shall be plotted
radar = radar2





########################################################################
### general pattern ###
########################################################################

'''
Parameters concerning all pattern radars
'''

#offset for a wrongly calibrated azimuth angle
offset = -4
