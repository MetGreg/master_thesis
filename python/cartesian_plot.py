###program to plot radar data (in polar coordinates) on a new defined cartesian grid

'''
Radar data of pattern or dwd radar will be plotted on a cartesian grid, 
its parameters can be defined in parameters.py. 

1. step: Read in radar data.
2. step: Transform polar coordinates of radar data points to lon/lat
3. step: Transform lon/lat coordinates to coordinates in a rotated pole	coordinate system with Hamburg beeing the equator.
4. step: Interpolate radar data in rotated pole coordinates to the new cartesian grid.
5. step: Plot data
'''

###QUESTIONS/to-dos
#-modules and objects, where do I have to import modules?
#-deal with warnings

########################################################################
### modules ###
########################################################################

###modules
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import re
import seaborn as sns
import parameters
from pathlib import Path
from MasterModule.MainRadar import Radar
from MasterModule.DWDRadar import Dwd
from MasterModule.PatternRadar import Pattern
from MasterModule.RadarData import RadarData
from MasterModule.CartesianGrid import CartesianGrid
from MasterModule.GridParameter import GridParameter


	
	
					
########################################################################
### parameters ###
########################################################################

'''
Some parameters can be set in parameters.py
'''

file_name 	= parameters.file_name	#name of data file
grid_par 	= parameters.grid_par	#numpy array containing grid parameters (np.array([start_lon,end_lon],[start_lat,end_lat],resolution]))
refl_key	= parameters.refl_key	#defines at which processing step reflectivity shall be plotted
minute		= parameters.minute		#defines which minute of the hourly pattern radar data files shall be plotted
res_factor	= parameters.res_factor	#factor, by which azimuth resolution is going to be increased





########################################################################
### read in data ###
########################################################################

'''
Data is saved to a Radar-Object. The method used to read in the data
differs, depending on the radar that shall be plotted. 
'''

###check, data from which radar is used and create a corresponding radar-object
if re.search('dwd_rad_boo',file_name):
	radar = Dwd()
elif re.search('level1_hdcp2',file_name):
	radar = Pattern('dbz',minute)
elif re.search('level2_hdcp2',file_name):
	radar = Pattern(refl_key,minute)

### read in data
radar.read_file(file_name,res_factor)





########################################################################
### artificially increase azimuth resolution ###
########################################################################

'''
The azimuth resolution of the radar usually is 1°. To avoid 
empty grid boxes in the new cartesian grid, the azimuth 
resolution can be increased artificially. Each gridbox will 
be divided into 'x' gridboxes with the same value (x beeing the 
res_factor). This is done by duplicating all lines (azimuths) 'x'-times. 
This is equivalent to dividing all grid boxes at this azimuth into 'x' 
sub-grid boxes, when the coordinates of the sub grid boxes are adjusted 
(growing with 1/x ° instead of 1°)
'''

radar.increase_azi_res(res_factor)





########################################################################
### calculate coordinates of middle pixel for each box ###
########################################################################

'''
Coordinates of data are given at specific points, but are
valid for a box. The coordinates of the data points are given
at the far edge in range and near edge in azimuth for each
grid box (looking from radar site).
This method calculates for each grid box the polar coordinates 
of the middle pixel out of the given coordinates at the edge of
the box.
The middle pixel is calculated through averaging of two 
consecutive ranges and through averaging of two consecutive 
azimuth angles.
'''
	
pixel_center 	= radar.get_pixel_center() #pixel_center is a np.meshgrid (pixel_center[0] = range, pixel_center[1] = azimuth)





########################################################################
### transform polar coordinates to lon/lat ###
########################################################################

'''
Transformation of polar coordinates of grid boxes (middle pixel) to 
cartesian coordinates, using a wradlib function
'''

lon, lat		= radar.polar_to_cartesian(pixel_center[0],pixel_center[1])





########################################################################
### rotated pole transformation ###
########################################################################

'''
Transform the cartesian coordinates to rotated pole coordinates using
a function from Claire Merker.
'''

rotated_coords = radar.rotate_pole(lon,lat) #rotated_coords.shape=(360,600,3), (azi,range,[lon,lat,height])





########################################################################
### Create new cartesian grid ###
########################################################################

'''
Creates the cartesian grid, on which data shall be plotted.
'''

new_grid = CartesianGrid(grid_par,radar) #CartesianGrid-object





########################################################################
### Check/Create index-matrix ###
########################################################################

'''
To interpolate radar data to the new cartesian grid, it is necessary 
to know for each grid box, which data points fall into this grid box.
For a given cartesian grid and a given radar, the data points always 
fall into the same grid boxes. Thus, this information can be saved to a 
file and doesn't have to be calculated again. The information is saved
in form of a matrix (index-matrix), which has exactly the shape of 
the new cartesian grid. For each grid box, there is an entry in the
index-matrix, which contains the indices (location in rotated pole 
coordinate array) of all data points falling into this grid box.
'''

###name of matrix file
index_matrix_file 	= './index_matrix/index_matrix_'+str(radar.name)+'_'+str(new_grid.par.lon_start)+'_'+str(new_grid.par.lon_end)+'_'+str(new_grid.par.lat_start)+'_'+str(new_grid.par.lat_end)+'_'+str(new_grid.par.res_m)+'_'+ str(res_factor)+'.dat'
		
###path is used to check if file exists or needs to be created.
index_matrix 		= Path(index_matrix_file)
		
###Check, if index-matrix file is present already. If not, calculate the index-matrix and create a file containing this matrix for future use
if not index_matrix.is_file():	
	new_grid.create_index_matrix(radar,index_matrix_file)
	
	
	
	
	
########################################################################
### Interpolate radar data to cartesian grid ###
########################################################################

'''
Interpolates radar data to the new cartesian grid, by averaging all
data points falling into the same grid box of the new cartesian grid. 
'''

reflectivity = new_grid.data_to_grid(index_matrix_file,radar)





########################################################################
### plot data ###
########################################################################

'''
Plots radar data on the new cartesian grid using seaborn.
'''


xlabel = []
ylabel = []

lon_plot = np.arange(new_grid.par.lon_start,new_grid.par.lon_end,new_grid.par.res_deg)
lat_plot = np.arange(new_grid.par.lat_start,new_grid.par.lat_end,new_grid.par.res_deg)

ticks = int(np.ceil((new_grid.par.lon_end - new_grid.par.lon_start)/new_grid.par.res_deg))


for x in range(0,ticks,int(ticks/10)):
	xlabel.append(round(lon_plot[x],2))
	ylabel.append(round(lat_plot[x],2))
	
###change order of lines
refl_rev = reflectivity[::-1] #matplotlib starts to plot from top, but data is saved from bottom --> need to reverse


###create plot
fig,ax = plt.subplots()
sns.heatmap(refl_rev, square=True)
ax.set_yticks(np.arange(0,ticks,ticks/10), minor = False)
ax.set_xticklabels(xlabel,fontsize = 16)
ax.set_yticklabels(ylabel,fontsize = 16)
ax.set_xticks(np.arange(0,ticks,ticks/10), minor = False)
ax.yaxis.grid(True, which='major')
ax.xaxis.grid(True, which='major')
plt.title(str(radar.name) + '-data on cartesian grid with res. of ' + str(int(new_grid.par.res_m)) + ' m, with ' + str(res_factor) + ' x incr. azi-res.',fontsize = 24)
plt.xlabel('longitude',fontsize = 18)
plt.ylabel('latitude',fontsize = 18)
plt.show()

