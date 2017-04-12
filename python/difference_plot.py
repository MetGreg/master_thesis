###program that plots differences between two radar imgaes on a new grid

'''
program plots differences between two radar images after interpolating
to the same cartesian grid.
'''





########################################################################
### modules ###
########################################################################

#modules
import matplotlib.pyplot as plt
import numpy as np
import re
import seaborn as sb
import parameters as par
from pathlib import Path
from MasterModule.main_radar import Radar
from MasterModule.dwd_radar import Dwd
from MasterModule.pattern_radar import Pattern
from MasterModule.radar_data import RadarData
from MasterModule.cartesian_grid import CartesianGrid





########################################################################
### lists, parameters ###
########################################################################

'''
Some parameters, that can be set in parameters.py.
Also, lists of program are defined here.
'''

#parameters
file1     = par.radar1[0] #name of first radar data file
file2     = par.radar2[0] #name of second radar data file
minute1   = par.radar1[1] #minute of 1st data file to be plotted
minute2   = par.radar2[1] #minute of 2nd data file to be plotted
proc_key1 = par.radar1[2] #key for proc. step of 1st radar
proc_key2 = par.radar2[2] #key for proc. step of 2nd radar
res_fac1  = par.radar1[3] #factor to incr. azi. res. of 1st radar
res_fac2  = par.radar2[3] #factor to incr. azi. res. of 2nd radar

#grid_par = [[[lon_start,lon_end],[lat_start,lat_end],
#          [lon_site,lat_site],max_range,resolution]]
grid_par  = par.grid_par  #numpy array containing grid parameters 
tick_nr   = par.tick_nr   #nr. of grid lines to be plotted as a grid
offset    = par.offset    #offset for wrongly calibrated azimuth angle
log_iso   = par.log_iso   #if True, rain area contours are plotted
rain_th   = par.rain_th   #threshold, at which rain is assumed

#lists
l_refl    = []            #reflectivity matrices of radars





########################################################################
### Create Radar objectives ###
########################################################################

'''
For both radars, a radar objective is created. The file name contains
information about the type of radar (dwd or pattern) and in case of
the pattern radar, also about the processing step (level1, level2).
--> scan file_name to get radar and processing step, then create the
correct radar objective (dwd or pattern object)
'''

### 1st radar ###
#pattern radar, proc. step: 'level1'
if re.search('level1',file1):         
    radar1 = Pattern(file1,minute1,offset,'dbz',res_fac1)
#pattern radar, proc. step: 'level2'      
elif re.search('level2', file1):     
    radar1 = Pattern(file1,minute1,offset,proc_key1,res_fac1) 
#dwd radar
elif re.search('dwd_rad_boo', file1): 
    radar1 = Dwd(file1,res_fac1)



### 2nd radar ###
#same procedure as for level1
if re.search('level1',file2):
    radar2 = Pattern(file2,minute2,offset,'dbz',res_fac2)  
elif re.search('level2', file2):
    radar2 = Pattern(file2,minute2,offset,proc_key2,res_fac2)
elif re.search('dwd_rad_boo', file2):
    radar2 = Dwd(file2,res_fac2)



#create list of both radar objectives, for easy looping
radars = [radar1,radar2]






########################################################################
### Create new cartesian grid ###
########################################################################
    
'''
Creates the cartesian grid, on which data shall be plotted.
'''

#CartesianGrid-object
car_grid = CartesianGrid(grid_par) 
    
   
   
   
    
########################################################################
### Main Loop ###
########################################################################

'''
A lot of calculations are the same for both radars. These common
calculations are done in this main loop.
'''

#loop through both radars
for radar in radars:
    
        
    ####################################################################
    ### read in data ###
    ####################################################################
    
    '''
    Data is saved to a Radar-Object. The method used to read in the data
    differs, depending on the radar. (Different radar --> different 
    object --> different read-method)
    '''

    #read in data
    radar.read_file()
    
    
    
    
    
    ####################################################################
    ### artificially increase azimuth resolution ###
    ####################################################################
    
    '''
    The azimuth resolution of the radar usually is 1°. To avoid 
    empty grid boxes in the new cartesian grid, the azimuth 
    resolution is increased artificially. 
    '''
    
    #artificially increase azimuth resolution
    radar.increase_azi_res()
    
    
    
    
    
    ####################################################################
    ### calculate coordinates of middle pixel for each box ###
    ####################################################################
    
    '''
    Coordinates of data are given at specific points, but are
    valid for a box. 
    This method calculates for each grid box the polar coordinates 
    of the middle pixel out of the given coordinates at the edge of
    the box.
    '''
        
    #pixel_center is a np.meshgrid 
    #pixel_center[0] = range, pixel_center[1] = azi.
    pixel_center = radar.get_pixel_center() 
    
    
    
    
    
    ####################################################################
    ### transform polar coordinates to lon/lat ###
    ####################################################################
    
    '''
    Transformation of polar coordinates of grid boxes (middle pixel) to 
    cartesian coordinates, using a wradlib function
    '''
    
    #get cartesian coordinates of radar data
    lon, lat = radar.polar_to_cartesian(pixel_center[0],pixel_center[1])
    
    
    
    
    
    ####################################################################
    ### rotated pole transformation ###
    ####################################################################
    
    '''
    Transform the cartesian coords to rotated pole coordinates using
    a function from Claire Merker.
    '''
    
    #coords_rot.shape=(360,600,3), (azi,range,[lon,lat,height])
    coords_rot = radar.rotate_pole(lon,lat) 

    #save rotated coords to radar object
    radar.data.lon_rota = coords_rot[:,:,0]
    radar.data.lat_rota = coords_rot[:,:,1]
     
    
    
    
    
    ####################################################################
    ### Check/Create index-matrix ###
    ####################################################################

    '''
    Radar data in rotated pole coordinates will be interpolated to the
    cartesian grid, by averaging the reflectivity values of all data
    points falling into the same grid box. For a given cartesian grid
    and a given radar, always the same data points fall into the same
    grid boxes. --> This information doesn't need to be calculated each 
    time, but can be saved to a dat.file. 
    --> Check, if such a file is present already for the current radar
    and cartesian grid. If not, call method to create it.
    '''
    
    #the name of the file
    index_matrix_file =  './index_matrix/index_matrix_'     \
                            +str(radar.name)+'_'            \
                            +str(car_grid.lon_start)+'_'\
                            +str(car_grid.lon_end)+'_'  \
                            +str(car_grid.lat_start)+'_'\
                            +str(car_grid.lat_end)+'_'  \
                            +str(car_grid.res_m)+'_'    \
                            +str(radar.res_fac)+'_'         \
                            +str(offset)+'.dat'
	
    #Path is used to check, if the file exists
    index_matrix = Path(index_matrix_file)
	
    #if file doesn't exist, create it
    if not index_matrix.is_file():
        car_grid.create_index_matrix(radar,index_matrix_file)




      
    ####################################################################
    ### Interpolate radar data to cartesian grid ###
    ####################################################################
    
    '''
    Interpolates radar data to the new cartesian grid, by averaging all
    data points falling into the same grid box of the new 
    cartesian grid. 
    Due to noise and dbz beeing a logarithmic unit, 'no rain' can have a 
    large spread in dbz units. --> Reflectiviy smaller than 5 dbz, 
    will be set to 5,to avoid having large differences at low 
    reflectivity.
    '''
    
    #interpolate reflectivity to the new grid
    refl                 = car_grid.data2grid(index_matrix_file,radar)
    
    #set reflectivities smaller than 5 to 5
    refl[refl < rain_th] = rain_th
    
    #append inverted reflectivity matrix to list
    #mirror columns --> matplotlib plots the data exactly mirrored
    l_refl.append(refl)
    




########################################################################
### plot differences ###
########################################################################

'''
Plot the differences between the two radars on the cartesian grid by
calling the plot_diff method of the cartesian grid objectiv.
'''

#plot differences
car_grid.plot_diff(tick_nr,l_refl,log_iso,rain_th,radar1,radar2)
