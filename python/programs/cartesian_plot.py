#plot radar data (in polar coord) on a new defined cartesian grid

'''
Radar data of pattern or dwd radar will be plotted on a cartesian grid, 
its parameters can be defined in parameters.py. The plot will exactly 
cover the pattern area.

1. step: Read in radar data.
2. step: Transform polar coordinates of radar data points to lon/lat
3. step: Transform lon/lat coordinates to coordinates in a rotated pole    
         coordinate system with Hamburg beeing the equator.
4. step: Interpolate radar data in rotated pole coordinates to the new 
         cartesian grid.
5. step: Plot data
'''





########################################################################
### modules and functions ###
########################################################################

'''
Imports modules and functions needed for this program.
'''

#python modules
import re                                                            
from pathlib import Path

#MasterModule modules
from MasterModule.cartesian_grid import CartesianGrid
from MasterModule.dwd_radar      import DwdRadar
from MasterModule.pattern_radar  import PatternRadar
from MasterModule.refl_plot      import ReflPlot

#parameter
import parameters as par
    
#functions
from functions import rotate_pole
    
    

                

########################################################################
### parameters ###
########################################################################

'''
Some parameters, that can be set in parameters.py.
'''

#parameters
radar_par = par.radar_par #radar parameter
grid_par  = par.grid_par  #grid parameter
plot_par  = par.plot_par  #plot parameter

#file_name
file_name = radar_par[0]

#offset of radar
offset    = par.offset

#threshold, at which rain is plotted
rain_th   = par.rain_th





########################################################################
### Create objects ###
########################################################################

'''
Creates following objects:
- DwdRadar or PatternRadar (depending on input file) to read in data
- CartesianGrid for interpolating data to cartesian grid
- ReflPlot for plotting reflectivity data on cartesian grid

Creates the correct radar object after scanning (using regular 
expressions) the file_name, which contains information about the radar
and processing step.
'''



################### radar object #######################################

#for dwd radars
if re.search('dwd_rad_boo',file_name):
    radar = DwdRadar(radar_par)

#for pattern radars
elif re.search('level2',file_name):
    radar = PatternRadar(radar_par,offset)



############### Cartesian Grid object ##################################
car_grid = CartesianGrid(grid_par)



############## ReflPlot object #########################################
refl_plot = ReflPlot(grid_par,plot_par)           





########################################################################
### Read in data ###
########################################################################

'''
Reads in data, by calling the read_file method.
'''

#read in data
radar.read_file()





########################################################################
### artificially increase azimuth resolution ###
########################################################################

'''
The azimuth resolution of the radar usually is 1°. To avoid 
empty grid boxes in the new cartesian grid, the azimuth 
resolution is increased artificially. 
'''

#artificially increase azimuth resolution
radar.increase_azi_res()





########################################################################
### calculate coordinates of middle pixel for each box ###
########################################################################

'''
Coordinates of data are given at specific points, but are
valid for a box. 
This method calculates for each grid box the polar coordinates 
of the middle pixel out of the given coordinates at the edge of
the box.
'''
  
#pixel_center is a np.meshgrid 
#pixel_center[0] = range, pixel_center[1] = azimuth  
pixel_center = radar.get_pixel_center() 





########################################################################
### transform polar coordinates to lon/lat ###
########################################################################

'''
Transformation of polar coordinates of grid boxes (middle pixel) to 
cartesian coordinates, using a wradlib function.
'''

#get cartesian coordinates of radar data
lon, lat = radar.polar_to_cartesian(pixel_center[0],pixel_center[1])





########################################################################
### rotated pole transformation ###
########################################################################

'''
Transform the cartesian coordinates to rotated pole coordinates using
a function from Claire Merker.
'''

#rotated_coords.shape=(360,600,3), (azi,range,[lon,lat,height])
coords_rot = rotate_pole(lon,lat) 





########################################################################
### Check/Create index-matrix ###
########################################################################

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





########################################################################
### Interpolate radar data to cartesian grid ###
########################################################################

'''
Interpolates radar data to the new cartesian grid, by averaging all
data points falling into the same grid box of the new cartesian grid. 
Due to noise and dbz beeing a logarithmic unit, 'no rain' can have a 
large spread in dbz units. --> Dbz values smaller than 5 dbz will
be set to 5, to avoid large differences at low reflectivity.
'''

#interpolate radar data to cartesian grid
refl = car_grid.data2grid(
    index_matrix_file,coords_rot,radar.data.refl_inc
    )

#set reflectivities smaller than 5 to 5 (since no rain not def)
refl[refl < rain_th] = rain_th





########################################################################
### plot data ###
########################################################################

'''
Plots data on the new cartesian grid.
'''

#create title
title = str(radar.name)                    \
        +'-data: '                         \
        + str(radar.data.time_start.time())\
        + ' - '                            \
        + str(radar.data.time_end.time())  \
        +'\n'                              \
        + str(radar.data.time_end.date())

#make plot
refl_plot.make_plot(refl,title)
