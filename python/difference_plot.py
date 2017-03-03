###program that plots differences between pattern and dwd radar on a new grid

'''
'''





########################################################################
### modules ###
########################################################################

###modules
import matplotlib.pyplot as plt
import numpy as np
import re
import seaborn as sb
import parameters
from pathlib import Path
from MasterModule.MainRadar import Radar
from MasterModule.DWDRadar import Dwd
from MasterModule.PatternRadar import Pattern
from MasterModule.RadarData import RadarData
from MasterModule.CartesianGrid import CartesianGrid
from MasterModule.GridParameter import GridParameter





########################################################################
### lists,parameters ###
########################################################################

'''
Some parameters, that can be set in parameters.py.
Also, lists of program are defined here.
'''

###parameters
file_name_dwd		= parameters.file_name_dwd		#name of dwd data file
file_name_pattern 	= parameters.file_name_pattern	#name of pattern data file
grid_par 			= parameters.grid_par			#numpy array containing grid parameters (np.array([start_lon,end_lon],[start_lat,end_lat],resolution]))
minute			= parameters.minute				#defines which minute of the hourly pattern radar data files shall be plotted
refl_key			= parameters.refl_key			#defines at which processing step reflectivity shall be plotted
res_dwd			= parameters.res_dwd			#factor, by which azimuth resolution of dwd radar is going to be increased
res_pattern		= parameters.res_pattern			#factor, by which azimuth resolution of pattern radar is going to be increased
tick_frac			= parameters.tick_frac			#fraction of grid lines, that will be labeled in plot

###lists
reflectivities 	= []							#Will contain reflectivity matrices of both radars
x_label			= []							#for labeling x-axis
y_label			= []							#for labling y-axis




########################################################################
### Create Radar objectives ###
########################################################################

'''
For both radars, a radar objective is created
'''

###class of dwd radar
radar_dwd 			= Dwd(file_name_dwd,res_dwd)

###pattern data can be of different processing steps --> can be found in file name
if re.search('level1',file_name_pattern):
	radar_pattern 	= Pattern('dbz',minute,file_name_pattern,res_pattern)
elif re.search('level2', file_name_pattern):
	radar_pattern	= Pattern(refl_key,minute,file_name_pattern,res_pattern)

###create list of both radar objectives, for easy loop
radars = [radar_dwd,radar_pattern]






########################################################################
### Main Loop ###
########################################################################

'''
A lot of calculations are the same for both radars. These common
calculations are done in this main loop.
'''

###loop through both radars
for radar in radars:
	
		
	########################################################################
	### read in data ###
	########################################################################
	
	'''
	Data is saved to a Radar-Object. The method used to read in the data
	differs, depending on the radar that shall be plotted. 
	'''

	### read in data
	radar.read_file()
	
	
	
	
	
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
	
	radar.increase_azi_res()
	
	
	
	
	
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
	index_matrix_file 	= './index_matrix/index_matrix_'+str(radar.name)+'_'+str(new_grid.par.lon_start)+'_'+str(new_grid.par.lon_end)+'_'+str(new_grid.par.lat_start)+'_'+str(new_grid.par.lat_end)+'_'+str(new_grid.par.res_m)+'_'+ str(radar.res_factor)+'.dat'
			
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
	Reflectiviy smaller than 5 dbz, will be set to zero, to avoid having 
	large differences at low reflectivity.
	'''
	
	reflectivity = new_grid.data_to_grid(index_matrix_file,radar)
	
	###set reflectivities smaller than 5 to 5
	reflectivity[reflectivity < 5] = 5
	
	###append reflectivities to list after inverting (since matplotlib plots the data exactly inverted)
	reflectivities.append(reflectivity[::-1])
	




########################################################################
### Calculate Difference ###
########################################################################

'''
Calculates differences of the two reflectivity matrices.
'''

refl_diff = reflectivities[1] - reflectivities[0]





########################################################################
### Plot ###
########################################################################

'''
Plots difference matrix on the new cartesian grid using seaborn.
'''

###calculates lon/lat of each grid cell of the cartesian grid
lon_plot 	= np.arange(new_grid.par.lon_start,new_grid.par.lon_end,new_grid.par.res_deg)
lat_plot 	= np.arange(new_grid.par.lat_start,new_grid.par.lat_end,new_grid.par.res_deg)

###number of grid boxes to be plotted
ticks 		= int(np.ceil((new_grid.par.lon_end - new_grid.par.lon_start)/new_grid.par.res_deg))

###fill label list with lon/lat 
for x in range(0,ticks,int(ticks/tick_frac)):
	x_label.append(round(lon_plot[x],2))
	y_label.append(round(lat_plot[x],2))

###create plot
fig,ax 				= plt.subplots() 													#create subplot																	
sb.heatmap			(refl_diff,vmin = -70, vmax = 70,cmap = 'bwr')						#create heatmap
ax.set_xticks		(np.arange(0,ticks,ticks/tick_frac), minor = False)					#x-tick positions
ax.set_yticks		(np.arange(0,ticks,ticks/tick_frac), minor = False)					#y-tick positions
ax.set_xticklabels	(x_label,fontsize = 16)												#x-tick labels
ax.set_yticklabels	(y_label,fontsize = 16)												#y-tick labels
ax.xaxis.grid		(True, which='major',color = 'k')									#x axis grid
ax.yaxis.grid		(True, which='major',color = 'k')									#y axis grid
ax.set_axisbelow	(False)																#put grid in front of data
plt.xlabel			('longitude',fontsize = 18)											#label x axis
plt.ylabel			('latitude'	,fontsize = 18)											#label y axis
plt.title			('Difference plot at ' + str(radar.data.time_start),fontsize = 24)	#title
plt.show()																				#show

