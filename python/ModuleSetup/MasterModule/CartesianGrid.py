########################################################################
### class for a new defined cartesian grid ###
########################################################################





########################################################################
### modules ###
########################################################################
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sb
from .GridParameter import GridParameter





########################################################################
### CartesianGrid class ###
########################################################################
class CartesianGrid:
	
	'''
	Object for a new defined cartesian grid, which can be used to plot
	data from different radars.
	'''
	
	
	
	
	
	###################################################################
	### Initialization method ###
	###################################################################
	def __init__(self,grid_par,radar):
		
		'''
		Saves the grid paramaters to a GridParameter-object.
		'''
		
		###create gridParameter object, which has defined grid parameters
		grid 		= GridParameter()
		
		###read the grid definition
		lon_start 	= grid_par[0][0]								#starting longitude
		lon_end		= grid_par[0][1]								#ending longitude
		lat_start 	= grid_par[1][0]								#starting latitude
		lat_end		= grid_par[1][1]								#ending latitude
		center		= grid_par[2]									#rotated coords of center of grid (=site coords of pattern radar)
		max_range		= grid_par[3]									#maximum range of pattern radar in m
		resolution	= float(grid_par[4])							#grid resolution in m
		
		###save grid definition to gridParameter-object
		grid.lon_start = lon_start									#starting longitude
		grid.lon_end 	= lon_end										#ending longitude
		grid.lat_start = lat_start									#starting latitude
		grid.lat_end 	= lat_end										#ending latitude
		grid.center	= center										#rotated coords of center of grid
		grid.max_range	= max_range									#maximum range of pattern radar in m
		grid.res_m	= resolution									#resolution in m
		grid.res_deg	= 1/(60*1852/resolution) 						#resolution in ° --> 1° equals 60 NM, equals 60*1852 m. --> 250m equals 1°/(60*1852/250)
		grid.lon_dim	= int(np.ceil((lon_end - lon_start)/grid.res_deg))	#number of rows in cartesian grid-matrix
		grid.lat_dim	= int(np.ceil((lat_end - lat_start)/grid.res_deg)) 	#number of lines in cartesian grid-matrix
		
		###save grid parameter object to CartesianGrid-object
		self.par 		= grid
	
	
	
	
	
	####################################################################
	### Create index-matrix ###
	####################################################################
	def create_index_matrix(self,radar,index_matrix_file):
		
		'''
		Method to create index-matrix
		'''
		
		###Can take a while (depending on resolution)
		print('No Index-Matrix present yet. Calculating the matrix...')
		
		###For each data point, calculate the lat- and lon-index of the grid box (of new grid), in which the radar data point lies.  
		lon_index 	= np.floor((radar.data.lon_rota - self.par.lon_start)/self.par.res_deg)
		lat_index 	= np.floor((radar.data.lat_rota - self.par.lat_start)/self.par.res_deg)		
			
		###create empty matrix with shape of (lat_dim, lon_dim) which is (number of lines, number of rows) of new cartesian grid.
		index_matrix 	= np.empty((self.par.lat_dim,self.par.lon_dim), dtype=np.object_)
	
		###fill empty matrix with empty lists, to be able to save more than one location, in case more than one radar data point falls into the same grid box
		for line_nr in range(len(index_matrix)):																					#lines of index-matrix (latitudes)
			for row_nr in range(len(index_matrix[line_nr])): 																		#rows of index-matrix (longitudes)
				index_matrix[line_nr][row_nr] = []																					#change entry of index matrix to empty list
		
		###loop through all radar data points and write the location (location = index in array of polar coordinates) of data points, which are not outside of new grid boundaries to the corresponding list of the index-matrix. 		
		for azi_nr in range(len(lon_index)):																						#lines of lon/lat_index (azimuth angles)
			for range_nr in range(len(lon_index[azi_nr])): 
				
				###get distance between data point and grid center
				distance = self.get_distance(radar,azi_nr,range_nr)
				
				###check, if distance is within maximum range to be plotted
				if distance <= self.par.max_range:
					index_matrix[int(lat_index[azi_nr][range_nr])][int(lon_index[azi_nr][range_nr])].append([azi_nr,range_nr]) 	#append grid box of new cartesian grid (=entry of index-matrix), in which the radar data point falls, with location of radar data point. 
				
		###save matrix to dat.file
		index_matrix.dump(index_matrix_file)
			
	
	
	
	
	####################################################################
	### Interpolation method ###
	####################################################################
	def data_to_grid(self,index_matrix_file,radar):
		
		'''
		Interpolates radar data to new cartesian grid. The reflectivity
		value of a grid box is the mean reflectivity of all data points
		falling into this grid box.
		'''
		
		###load the index-matrix	
		index_matrix = np.load(index_matrix_file)
		
		###create an empty array with the same shape as the new cartesian grid, which will contain the averaged (interpolated) values 
		refl = np.empty((self.par.lat_dim,self.par.lon_dim))
		
		###fill the refl-matrix with the interpolated reflectivity values for each grid box. 
		for line_nr in range(self.par.lat_dim): 				#go through lines of index-matrix (latitudes)
			for row_nr in range(self.par.lon_dim):		 		#go through columns of index-matrix (longitudes)
				
				###for calculating the mean, the reflectivity values are summed and divided by the amount of data points. 
				refl_sum = 0	#for each grid box, set the sum-variable to zero again
				
				###go through each data point lying in this grid box and add the reflectivity-value to the sum-variable
				for data_point in index_matrix[line_nr][row_nr]:
					refl_sum += radar.data.refl_inc[data_point[0]][data_point[1]]
				
				###calculate amount of data points lying in the grid-box
				data_count = len(index_matrix[line_nr][row_nr])
				
				###check, if there is at least one data point lying in the grid box and then calculate the mean reflectivity of all data points in this grid box.
				if data_count != 0:
					refl[line_nr][row_nr] = refl_sum / data_count
				###if no data point was lying in the grid-box, set it to NaN
				else:
					refl[line_nr][row_nr] = np.NaN
					
		return refl
				
	
	
	
	
	###################################################################
	### Distance of data point to center of grid ###
	###################################################################
	def get_distance(self,radar,azi_nr,range_nr):
		
		'''
		Calculates distance of a data point to the center of grid.
		'''
		
		###get lat/lon coordinates of data point
		lon 			= radar.data.lon_rota[azi_nr][range_nr]
		lat 			= radar.data.lat_rota[azi_nr][range_nr]
		
		###get difference of coordinates in °
		lon_diff 		= lon - self.par.center[0]
		lat_diff 		= lat - self.par.center[1]
		
		###get difference in m
		lon_diff_m 	= lon_diff*60*1852
		lat_diff_m 	= lat_diff*60*1852
		
		###get distance in m
		distance 		= np.sqrt(lon_diff_m**2 + lat_diff_m**2)
		
		return distance
