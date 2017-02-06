###program to plot data on a new defined cartesian grid



########################################################################
### modules and functions ###
########################################################################

###modules
import numpy as np
import wradlib
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib.cm as cm
import seaborn as sns

###functions
from functions import read_dwd_hdf5
from functions import get_pixel_center
from functions import rotate_pole
from functions import get_index
from functions import raise_azi_res



########################################################################
### read in data ###
########################################################################

file_name 		= '../../Daten/dwd_rad_boo/sweeph5allm/2016/06/07/ras07-pcpng01_sweeph5allm_any_00-2016060716003300-boo-10132-hd5'
index_matrix 	= Path('index_matrix.dat')
dwd 			= read_dwd_hdf5(file_name) 	#this is a dwd-object that contains actual data + all meta-data, that is needed (like height, lon/lat etc)
resolution		= 250						#resolution of the new cartesian grid
raise_factor	= 10


########################################################################
### raise azimuth resolution ###
########################################################################

'''
The azimuth resolution of the dwd-radar is 1°. To avoid empty grid boxes
in the new cartesian grid, the azimuth resolution must be raised 
artificially. This is done by a factor x. The artificially created grid
boxes get the same value as the nearest real grid box.  
'''

art_data = raise_azi_res(dwd.data,raise_factor)



########################################################################
### calculate coordinates of middle pixel for each box ###
########################################################################
 
'''
dwd-values start actually at r=0, but are valid for the box with range from 0 to 250m. 
function get_pixel_center expects range values at far edge from box --> start with r = 250m
'''

#nrays = dimension of azimuth (360), nbins = dimension of radius (600). rscale = distance between to measurements on radius-axis (250m) 
coord_range = np.arange(0+dwd.rscale,dwd.nbins*int(dwd.rscale)+1,int(dwd.rscale)) 	#range 		= 250,500,......,150000
coord_azi 	= np.arange(0,dwd.nrays,1/raise_factor) 								#azimuth 	= 0,1,....,359

###polar coordinates of middle pixel of each box, needs far edge range and near edge azimuth
pixel_center = get_pixel_center(coord_range,coord_azi)	#numpy.meshgrid, pixel_center[0] = range, pixel_center[1] = azimuth

###transform polar coordinates to lon/lat
#[[],[],...,[]] inner lists loop through ranges, outer lists through azimuth
lon, lat = wradlib.georef.polar2lonlat(pixel_center[0],pixel_center[1],(dwd.lon,dwd.lat),re=6370040) #lon.shape and lat.shape = (360,600) = (azimuth,range)



########################################################################
### rotated pole transformation ###
########################################################################

#360*600 points of coordinates in format = (lon,lat,height)
#[[],[],....,[]] inner lists loop through ranges, outer list through azimuth
rotated_coords = rotate_pole(lon,lat) #rotated_coords.shape=(360,600,3)

###lon and lat coordinates of rotated_coords-matrix
lon_rota = rotated_coords[:,:,0]
lat_rota = rotated_coords[:,:,1]



########################################################################
### define new grid ###
########################################################################

###since lon/lat is in degrees, the resolution of new grid must be in degrees too --> transform resolution in 'm' to resolution in '°'
res_new= 1/(60*1852/resolution) #1° equals 60 NM, equals 60*1852 m. --> 250m equals 1°/(60*1852/250) 

###calculate min and max lon/lat. This is needed as a starting-/ending point for the new grid 
lon_min = min(np.reshape(lon_rota,dwd.nrays*dwd.nbins*raise_factor))
lat_min = min(np.reshape(lat_rota,dwd.nrays*dwd.nbins*raise_factor))
lon_max = max(np.reshape(lon_rota,dwd.nrays*dwd.nbins*raise_factor))
lat_max = max(np.reshape(lat_rota,dwd.nrays*dwd.nbins*raise_factor))



########################################################################
### transformation to new grid ###
########################################################################

'''
reflectivity-data is present in a 2D (360,600)-Matrix. The corresponding
coordinates of each data point are present in rotated-pole coordinates.
To compare two different radars with different resolution, data of both
radars must be brought to a new (cartesian) grid. 
Data of radars are in polar coordinates, but are brought to a cartesian
grid. Thus it can happen, that more than one data point fall into the
same grid box of the new grid. Therefore it must be calculated, which
data points fall into each of the grid boxes of the new grid. The
reflectivity-value of a grid box is represented by the mean of all 
data points falling into this grid box.
'''

###For each data point, calculate the x- and y-index of the grid box (of new grid), in which the data point lies.  
lon_index = np.floor((lon_rota-lon_min)/res_new)
lat_index = np.floor((lat_rota - lat_min)/res_new)



'''
The information about which data points fall into which grid box of new grid can be saved into an 2D-array. For a given old and a given new grid, this matrix stays the same. 
That's why the matrix has to be calculated only once and if this was done already, the index-matrix can simply be read in, instead of calculating it again. 
'''

	
###Check, if index-matrix file is present already. If not, calculate the index-matrix and create a file containing this matrix for the future
if not index_matrix.is_file():
	
	print('No Index-Matrix present yet. Calculating the matrix...')
	get_index(lon_index,lat_index) ###function, to calculate the index-matrix and save it to a dat.file

###load the index-matrix	
index_matrix = np.load('index_matrix.dat')

###create an empty array with the same dimensions as the new cartesian grid. This array is going to be filled with the reflectivity values for each grid box.
refl = np.empty((1199,1199))

###fill the refl-matrix with the reflectivity values for each grid box. (Mean reflectivity of all data points lying in the grid box)
for line_nr in range(len(index_matrix)): 				#go through lines of index-matrix
	for row_nr in range(len(index_matrix[line_nr])): 	#go through columns of index-matrix
		
		###for calculating the mean, the reflectivity values are summed and divided by the amount of data points. 
		refl_sum = 0	#for each grid box, set the sum-variable to zero again
		
		###go through each data point lying in this grid box and add the reflectivity-value to the sum-variable
		for data_point in index_matrix[line_nr][row_nr]:
			refl_sum += art_data[data_point[0]][data_point[1]]
		
		###calculate amount of data points lying in the grid-box
		data_count = len(index_matrix[line_nr][row_nr])
		
		###check, if there is at least one data point lying in the grid box and then calculate the mean reflectivity of all data points in this grid box.
		if data_count != 0:
			refl[line_nr][row_nr] = refl_sum / data_count
		else:
			refl[line_nr][row_nr] = np.NaN
			
'''
Say what? Data was transformed to a new, cartesian grid! 
'''



########################################################################
### plot data ###
########################################################################

lon_plot = np.arange(lon_min,lon_max,res_new)
lat_plot = np.arange(lat_min,lat_max,res_new)

xlabel = []
ylabel = []

for x in range(0,1200,100):
	xlabel.append(round(lon_plot[x],2))
	ylabel.append(round(lat_plot[x],2))
	

refl_rev = refl[::-1]
fig,ax = plt.subplots()
sns.heatmap(refl_rev, square=True)
ax.set_yticks(np.arange(1200,0,-100), minor = False)
ax.set_xticklabels(xlabel)
ax.set_yticklabels(ylabel)
ax.set_xticks(np.arange(0,1200,100), minor = False)
ax.yaxis.grid(True, which='major')
ax.xaxis.grid(True, which='major')

plt.title('DWD-data on cartesian grid with resolution of ' + str(resolution) + ' m')
#plt.imshow(refl_rev)
plt.show()

