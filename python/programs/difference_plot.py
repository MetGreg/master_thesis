###Plot radar differences

'''
program plots differences between two radar images after interpolating
to the same cartesian grid.

For both radars:
1. step: Read in radar data. 
2. step: Transform polar coordinates of radar data points to lon/lat
3. step: Transform lon/lat coordinates to coordinates in a rotated pole    
         coordinate system with Hamburg beeing the equator.
4. step: Interpolate radar data in rotated pole coordinates to the new 
         cartesian grid.

Finally:
5. step: Calculate reflectivity differences between radar data arrays.
6. step: Plot reflectivity differences.
'''





########################################################################
### modules and functions ###
########################################################################

'''
Import all modules and functions needed for this program.
'''

#python modules
import re
from pathlib import Path

#Mastermodule
from MasterModule.cartesian_grid import CartesianGrid
from MasterModule.dwd_radar      import DwdRadar
from MasterModule.pattern_radar  import PatternRadar
from MasterModule.refl_diff_plot import ReflDiffPlot

#parameter
import parameters as par

#functions
from functions import rotate_pole




########################################################################
### parameters, lists ###
########################################################################

'''
Get parameters. Parameters can be set in parameters.py
'''

#parameters
radar1_par = par.radar1_par #radar parameter of first radar
radar2_par = par.radar2_par #radar parameter of second radar
grid_par   = par.grid_par   #grid parameter
plot_par   = par.plot_par   #plot parameter

#file_name
file1      = radar1_par[0]
file2      = radar2_par[0]

#offset of radar
offset     = par.offset

#threshold, at which rain is plotted
rain_th    = par.rain_th

#lists
l_refl     = [] #reflectivity matrices of radars





########################################################################
### Create objects ###
########################################################################

'''
Creates all objects needed:
- Dwd or Pattern (depending on input file) to read in data
- CartesianGrid for interpolating data to Cartesian Grid
- ReflDiffPlot for plotting differences in reflectivity

Creates the correct radar object after scanning (using regular 
expressions) the file_name, which contains information about the radar
and processing step.
'''



####################### 1st radar ######################################

#for dwd radars
if re.search('dwd_rad_boo',file1):
    radar1 = DwdRadar(radar1_par)

#for pattern radars
elif re.search('level2',file1):
    radar1 = PatternRadar(radar1_par,offset)



####################### 2nd radar ######################################

#for dwd radars
if re.search('dwd_rad_boo',file2):
    radar2 = DwdRadar(radar2_par)

#for pattern radars
elif re.search('level2',file2):
    radar2 = PatternRadar(radar2_par,offset)

#create list of both radar objectives, for easy looping
radars = [radar1,radar2]



#################### CartesianGrid object ##############################
car_grid = CartesianGrid(grid_par) 



#################### ReflDiffPlot ######################################
refl_diff_plot = ReflDiffPlot(grid_par,plot_par)

      


    
########################################################################
### Main Loop ###
########################################################################

'''
A lot of calculations are the same for both radars. These common
calculations are done in this main loop:
 - read data
 - increase azimuth resolution
 - calculate middle pixel polar coordinates
 - calculate cartesian coordinates out of polar coords
 - calculate rotated pole coordinates out of cartesian coords
 - create index matrix
 - interpolate data to cartesian grid
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
    cartesian coordinates, using a wradlib function.
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
    coords_rot = rotate_pole(lon,lat) 

    
    
    
    
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
    index_matrix_file =  '../index_matrix/index_matrix_'     \
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
        car_grid.create_index_matrix(index_matrix_file,coords_rot)




      
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
    refl = car_grid.data2grid(
        index_matrix_file,coords_rot,radar.data.refl_inc
        )
    
    #set reflectivities smaller than 5 to 5
    refl[refl < rain_th] = rain_th
    
    #append inverted reflectivity matrix to list
    l_refl.append(refl)
    




########################################################################
### plot differences ###
########################################################################

'''
Plot the differences between the two radars on the cartesian grid by
calling the plot_diff method of the cartesian grid objectiv.
'''

#title                           
title = radar2.name + '('                             \
    + str(radar2.data.time_start.time()) + ' - '      \
    + str(radar2.data.time_end.time()) + ')'          \
    + ' minus ' + radar1.name                         \
    + '(' + str(radar1.data.time_start.time()) + ' - '\
    + str(radar1.data.time_end.time()) + ')\n'        \
    + str(radar1.data.time_end.date())
        
#plot differences
refl_diff_plot.make_plot(l_refl,[radar1.name,radar2.name],title)
