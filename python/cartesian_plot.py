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
### modules ###
########################################################################

'''
Modules that need to be imported
'''

#modules
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors                       
import numpy as np                                        
import re
import seaborn as sb
import parameters as par
from pathlib import Path
from MasterModule.MainRadar import Radar
from MasterModule.DWDRadar import Dwd
from MasterModule.PatternRadar import Pattern
from MasterModule.RadarData import RadarData
from MasterModule.CartesianGrid import CartesianGrid
from MasterModule.GridParameter import GridParameter


    
    
                    
########################################################################
### lists, parameters ###
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
grid_par  = par.grid_par  #numpy array containing grid parameters 
tick_nr   = par.tick_nr   #number of grid lines to be labeled
offset    = par.offset    #offset for wrongly calibrated azimuth angle
rain_th   = par.rain_th   #threshold, at which rain is assumed





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
cartesian coordinates, using a wradlib function
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
coords_rot = radar.rotate_pole(lon,lat) 

#save rotated coords to radar object
radar.data.lon_rota = coords_rot[:,:,0]
radar.data.lat_rota = coords_rot[:,:,1]
        




########################################################################
### Create new cartesian grid ###
########################################################################

'''
Creates the cartesian grid, on which data shall be plotted.
'''

#CartesianGrid-object
car_grid = CartesianGrid(grid_par) 





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
index_matrix_file =  './index_matrix/index_matrix_'     \
                        +str(radar.name)+'_'            \
                        +str(car_grid.par.lon_start)+'_'\
                        +str(car_grid.par.lon_end)+'_'  \
                        +str(car_grid.par.lat_start)+'_'\
                        +str(car_grid.par.lat_end)+'_'  \
                        +str(car_grid.par.res_m)+'_'    \
                        +str(radar.res_fac)+'_'         \
                        +str(offset)+'.dat'

#Path is used to check, if the file exists
index_matrix = Path(index_matrix_file)

#if file doesn't exist, create it
if not index_matrix.is_file():
    car_grid.create_index_matrix(radar,index_matrix_file)





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
refl                 = car_grid.data2grid(index_matrix_file,radar)

#set reflectivities smaller than 5 to 5)
refl[refl < rain_th] = rain_th

#mirror columns --> matplotlib plots the data exactly mirrored
refl                 = refl[::-1]





########################################################################
### prepare plot ###
########################################################################

'''
prepares plot by defining labling lists, ticks, cmaps etc 
'''

#getting rot. lon-coords of grid lines to be labeled
lon_plot = np.around(
            np.linspace(
                car_grid.par.lon_start,
                car_grid.par.lon_end,
                num = tick_nr
                       ),decimals = 2
                    )
                     
#getting rot. lat-coords of grid lines to be labeled                        
lat_plot = np.around(
            np.linspace(
                car_grid.par.lat_start,
                car_grid.par.lat_end,
                num = tick_nr
                       ),decimals = 2
                    )

#maximum number of grid lines (lon_dim = lat_dim)
ticks = car_grid.par.lon_dim

#create colormap for plot (continously changing colormap)                                                                    
cmap     = mcolors.LinearSegmentedColormap.from_list(
           'my colormap',['white','blue','red','magenta']
           )    





########################################################################
### plot data ###
########################################################################

'''
Plots interpolated radar data on the new cartesian grid using seaborn.
'''

#create subplot
fig,ax = plt.subplots() 

#create heatmap                                                                                                              
sb.heatmap(refl,vmin = 5, vmax = 70, cmap = cmap)                  

#x- and y-tick positions
ax.set_xticks(np.linspace(0,ticks,num=tick_nr), minor = False)                
ax.set_yticks(np.linspace(0,ticks,num=tick_nr), minor = False)                

#x- and y-tick labels
ax.set_xticklabels(lon_plot,fontsize = 16)                                        
ax.set_yticklabels(lat_plot,fontsize = 16,rotation = 'horizontal')                                        

#grid
ax.xaxis.grid(True, which='major', color = 'k')                                
ax.yaxis.grid(True, which='major', color = 'k')

#put grid in front of data                        
ax.set_axisbelow(False)  

#label x- and y-axis                                                  
plt.xlabel('r_lon', fontsize = 18)                                    
plt.ylabel('r_lat', fontsize = 18)    

#title 
plt.title(                                   \
          str(radar.name)                    \
          +'-data: '                         \
          + str(radar.data.time_start.time())\
          + ' - '                            \
          + str(radar.data.time_end.time())  \
          +'\n'\
          + str(radar.data.time_end.date()),
          fontsize = 20
         )   

#show  
plt.show()                                                                
