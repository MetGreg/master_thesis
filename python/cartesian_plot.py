###program to plot radar data (in polar coordinates) on a new defined cartesian grid

'''
Radar data of pattern or dwd radar will be plotted on a cartesian grid,
which parameters can be defined in parameters.py. 

1. step: Read in radar data.
2. step: Transform polar coordinates of radar data points to lon/lat
3. step: Transform lon/lat coordinates to coordinates in a rotated pole	coordinate system with Hamburg beeing the equator.
4. step: Interpolate radar data in rotated pole coordinates to the new cartesian grid.
5. step: Plot data
'''

###QUESTIONS/to-dos
#-maybe the increase of azimuth resolution can be done more efficiently (np.append/contenate maybe?)
#-Sinn vom Attribute-error
#-modules and objects, where do I have to import modules?
#-how to use objects from different files
#-deal with warnings
#-when do you give variables as an argument to methods, when you don't?
#-difference coordinates/coordinations?
########################################################################
### modules and functions ###
########################################################################

###modules
import cartopy.crs as ccrs
import h5py
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import re
import seaborn as sns
import wradlib
from netCDF4 import Dataset
from pathlib import Path
import parameters





########################################################################
### objects ###
########################################################################





########################################################################
### main Radar-Object ###
########################################################################
class Radar(object):
	
	'''
	This main Radar-Object will get a sub-object for each of the 
	different radars (like pattern and boostedt).
	Methods working in general for the radars are part of main object.
	'''
	
	
	
	
	
	####################################################################
	### initialization ###
	####################################################################
	def __init__(self):
		'''
		Does nothing so far 
		'''
		
		pass
	
	
	
	
	
	####################################################################
	### read_file-method ###
	####################################################################
	def read_file(self):
		
		'''
		This method is specified in sub-objects, since reading files
		differs from radar to radar.
		'''
	
		raise NotImplementedError
	
	
	
	
	
	####################################################################
	### method to increase azimuth resolution by a factor ###
	####################################################################
	def increase_azi_res(self,res_factor):
		
		'''
		Increases azimuth resolution of radar dataset.
		'''
		
		###define empty list which is going to be filled with reflectivity values of increased resolution
		data_inc_res = []
		
		#loop through radar data lines (=azimuths) and fill the new created list with 'res_factor'- number of duplicates of the data line
		for data_line in self.data.refl:	#loop through data lines (=azimuth angles)
			for y in range(res_factor):		#append a data line duplicate 'res_factor'-times
				data_inc_res.append(data_line)
		
		###save artificially increased dataset to object
		self.data.refl_inc = np.array(data_inc_res)
		
	
	
	
	
	####################################################################
	### method to calculate coordinates of middle pixel for each box ###
	####################################################################
	def get_pixel_center(self): 		
	
		'''
		Calculates polar coordination of the middle pixel for each polar
		grid box of rada data.
		'''
			
		###define shorter names for the coordination arrays
		range_coords		= self.data.range_coords
		azi_coords			= self.data.azi_coords_inc
		
		###calculating arrays of middle pixel coordinates
		range_coords 		= np.append(range_coords, range_coords[-1] + (range_coords[-1]-range_coords[-2])) 	#append a new value to the list (which will be used to average the last value)
		range_coords 		= range_coords[:-1] - (range_coords[1:]-range_coords[:-1])/2.						#average all entries by changing one entry after another using two consecutive entries to average.
		azi_coords 			= np.append(azi_coords, azi_coords[-1] + (azi_coords[-1]-azi_coords[-2]))			#append a new value to the list (which is used to average the last value)
		azi_coords 			= azi_coords[:-1] + (azi_coords[1:]-azi_coords[:-1])/2.								#average all entries by changing one entry after another using two consecutive entries to average.
		
		###create a numpy meshgrid, to have easy access to all combinations of range and azimuth
		pixel_center 		= np.meshgrid(range_coords, azi_coords)
		
		return pixel_center
	
	
	
	
	
	####################################################################
	### method to transform polar to cartesian coordinates ###
	####################################################################
	def polar_to_cartesian(self,polar_range,polar_azi):
		
		'''
		Uses a wradlib function to calculate lon/lat coordinates out of 
		polar coordinates. Needs a wradlib environment to work.
		See wradlib.org for more details.
		'''
		
		###transform polar coordinates to lon/lat coordinates
		lon, lat 		= wradlib.georef.polar2lonlat(polar_range,polar_azi,(self.data.lon_site,self.data.lat_site),re=6370040) #lon.shape and lat.shape = (360,600) = (azimuth,range)

		return lon, lat





	####################################################################
	### method to transform cartesian to rotated pole coordinates ###
	####################################################################
	def rotate_pole(self,lon,lat):
		
		'''
		Transforms cartesian coordinates to rotated pole coordinates
		using a function from Claire Merker. 
		(claire.merker@uni-hamburg.de)
		'''		
		
		###coordinates of rotated pole
		rotated_pole 	= [-170.415, 36.0625]
	
		###calculate coordinates in rotated pole coordinate system
		proj 			= ccrs.RotatedPole(rotated_pole[0], rotated_pole[1])
		rotated_coords 	= proj.transform_points(ccrs.Geodetic(), lon, lat)
		
		self.data.lon_rota = rotated_coords[:,:,0]
		self.data.lat_rota = rotated_coords[:,:,1]
		
		
	


########################################################################
### sub-class for Dwd-data ###
########################################################################		
class Dwd(Radar):
	
	'''
	Sub-Object of Radar. Contains all methods that are specific designed
	for Dwd-data.
	'''
	
	
	
	
	
	####################################################################
	### Initialization - method ###
	####################################################################
	def __init__(self):
		
		'''
		Save name of radar to object
		'''
	
		self.name = 'dwd' #name of radar
	
	
	
	
	
	####################################################################
	### method to read in dwd-data (hdf5) ###
	####################################################################
	def read_file(self,data_file):
	
		'''
		Reads dwd radar. Only attributes needed for my calculations are 
		read in. If more information about the file and the attributes 
		is wished, check out the hdf5-file with hdfview or 
		hd5dump -H
		'''
		
		###open file
		with h5py.File(data_file,'r') as h5py_file:
			
			###create RadarData-Object to save radar data generalized to this object	
			radar_data = RadarData()
			
			###read radar data
			lon_site					= h5py_file.get('where').attrs['lon']								#longitude coordinates of radar site
			lat_site					= h5py_file.get('where').attrs['lat']								#latitude coordinates of radar site
			r_bins						= h5py_file.get('dataset1/where').attrs['nbins']					#number of radius bins (600 --> 250m steps up to 150000m)
			r_start						= h5py_file.get('dataset1/where').attrs['rstart']					#range of first measurement
			r_steps						= h5py_file.get('dataset1/where').attrs['rscale'] 					#distance between 2 measurements on radius-axis (250m)
			azi_rays					= h5py_file.get('dataset1/where').attrs['nrays'] 					#number of azimuth rays(360 --> 1° steps)
			azi_start					= h5py_file.get('dataset1/where').attrs['startaz'] 					#azimuth angle of first measurement
			azi_steps					= h5py_file.get('dataset1/how').attrs['angle_step'] 				#angle step between 2 measurements
			gain 						= h5py_file.get('dataset1/data1/what').attrs['gain']				#factor (gain), which is needed to correct the dwd reflectivity to normal dbz values 
			offset 						= h5py_file.get('dataset1/data1/what').attrs['offset']				#Offset. Also needed to correct the dwd reflectivity to normal dbz values 
			refl						= h5py_file.get('dataset1/data1/data')								#uncorrected data 
			
			###save data to RadarData-Object
			radar_data.lon_site			= lon_site															#longitude coordinates of radar site
			radar_data.lat_site			= lat_site															#latitude coordinates of radar site
			radar_data.r_bins			= int(r_bins)														#number of radius bins (600 --> 250m steps up to 150000m)
			radar_data.azi_rays			= int(azi_rays)														#number of azimuth rays(360 --> 1° steps)
			radar_data.range_coords		= np.arange(r_start+r_steps,r_steps*r_bins+r_start+r_steps,r_steps)	#array containing range coordinates of data points (at far edge of grid box)
			radar_data.azi_coords		= np.arange(azi_start,azi_steps*azi_rays,azi_steps)					#array containing azimuth coordinates of data points (at near edge of grid box)
			radar_data.azi_coords_inc	= np.arange(azi_start,azi_steps*azi_rays,azi_steps/res_factor)		#array containing azimuth coordinates of data points with artificially increased resolution
			radar_data.refl				= refl * gain + offset												#corrected data
			
			###save RadarData-Object (which contains all the saved data) to DWD-Object
			self.data 					= radar_data
			
		
		
		
		
########################################################################
### sub-class for Pattern-data ###
########################################################################		
class Pattern(Radar):
	
	'''
	Sub-Object of Radar. Contains all methods specific designed for
	Pattern-data.
	'''
	
	
	
	
	
	####################################################################
	### initialization method ###
	####################################################################
	def __init__(self,refl_key):
		
		'''
		Saves name of radar refl_key to object, which defines at which 
		processing step the reflectivity data will be plottet. 
		refl_key must be set in parameters.
		'''
		
		self.refl_key 	= refl_key	#processing step
		self.name 		= 'pattern' #name of the radar
	
	
	
	
	
	####################################################################
	### method to read in pattern data (nc.files) ###
	####################################################################	
	def read_file(self,data_file):
		
		'''
		Read and save the important (for plotting) information of
		the pattern data. If more information is wished, check the data
		file with ncdump -h or ncview. 
		'''
	
		###create a RadarData-object to generalize the radar-properties.
		radar_data 					= RadarData()
		
		###open data file
		nc 							= Dataset(data_file, mode='r')
		
		###read all important informations
		lon_site					= nc.variables['lon'][:]										#longitude coordinate of radar site
		lat_site					= nc.variables['lat'][:]										#latitude coordinate of radar site
		r_bins						= nc.dimensions['range'].size									#number of range bins
		azi_rays					= nc.dimensions['azi'].size 									#number of azimuth rays
		azi_start					= nc.variables['azi'][0]										#starting value of azimuth angle
		azi_steps					= nc.variables['azi'][1] - azi_start							#azimuth angle steps between two measurements
		range_coords				= nc.variables['range'][:]										#array of to data points corresponding range coordinates
		azi_coords					= nc.variables['azi'][:]										#array of to data points corresponding azimuth coordinates
		refl						= nc.variables[self.refl_key][:][int((minute - 0.5)*2)]			#array of measured reflectivity
		
		###save the data to RadarData object
		radar_data.lon_site			= float(lon_site)												#longitude coordinate of radar site
		radar_data.lat_site			= float(lat_site)												#latitude coordinate of radar site
		radar_data.r_bins			= int(r_bins)													#number of range bins
		radar_data.azi_rays			= int(azi_rays)													#number of azimuth rays
		radar_data.range_coords		= range_coords													#array of to data points corresponding range coordinates
		radar_data.azi_coords		= azi_coords													#array of to data points corresponding azimuth coordinates
		radar_data.azi_coords_inc	= np.arange(azi_start,azi_steps*azi_rays,azi_steps/res_factor)	#array of corresponding azimuth coordinates to data points with artificially increased resolution
		radar_data.refl				= refl															#array of measured reflectivity
		
		###save the data to Pattern object
		self.data 					= radar_data
		




########################################################################
### class for saving general radar properties ###
########################################################################	
class RadarData:
	
	'''
	Used to define general, for different radars identical 
	radar data properties. 
	'''
	
	
	
	
	
	####################################################################
	### initialization method ###
	####################################################################
	def __init__(self):
		
		'''
		Does nothing so far
		'''
		
		pass





	####################################################################
	### longitude coordinate of radar site ###
	####################################################################
	@property
	def lon_site(self):
		
		'''
		longitude coordinate of radar location. Must be set as float.
		'''
		
		try:
			return self._lon_site
		except AttributeError:
			return 0
		
			
	@lon_site.setter
	def lon_site(self, new_lon_site):
		assert isinstance(new_lon_site, float), 'new site_longitude not a float'
		self._lon_site = new_lon_site
	
	
	
	
	
	####################################################################
	### latitude coordinate of radar site###
	####################################################################
	@property
	def lat_site(self):
		
		'''
		latitude coordinate of radar location. Must be set as float.
		'''
		
		try:
			return self._lat_site
		except AttributeError:
			return 0
	
			
	@lat_site.setter
	def lat_site(self, new_lat_site):
		assert isinstance(new_lat_site, float), 'new site_latitude not a float'
		self._lat_site = new_lat_site
	
	
	
	
	
	####################################################################
	### number of range bins###
	####################################################################
	@property
	def r_bins(self):
		
		'''
		Number of range bins. Must be a float.
		'''
		
		try:
			return self._r_bins
		except AttributeError:
			return 0
		
			
	@r_bins.setter
	def r_bins(self, new_r_bins):
		assert isinstance(new_r_bins, int), 'new r_bins not an integer' 
		self._r_bins = new_r_bins
	
	
	
	
	
	####################################################################
	### number of azimuth rays ###
	####################################################################
	@property
	def azi_rays(self):
		
		'''
		Number of azimuth rays. Usually 360. Must be a float
		'''
		
		try:
			return self._azi_rays
		except AttributeError:
			return 0	
		
			
	@azi_rays.setter
	def azi_rays(self, new_azi_rays):
		assert isinstance(new_azi_rays, int), 'new azi_rays not an integer' 
		self._azi_rays = new_azi_rays
		
	
	
	
	
	####################################################################
	### range coordinates ###
	####################################################################
	@property
	def range_coords(self):
		
		'''
		Numpy array of to the reflectivity data corresponding 
		range (distance) from radar. Must be 1D numpy array
		'''
		
		try:
			return self._range_coords
		except AttributeError:
			return 0
	
			
	@range_coords.setter
	def range_coords(self, new_range_coords):
		assert isinstance(new_range_coords, np.ndarray), 'new range_coords not a numpy array' 
		assert len(new_range_coords.shape) == 1, 'new range_coords is not 1D'
		self._range_coords = new_range_coords
	
	
	
	
	
	####################################################################
	### azimuth coordinates ###
	####################################################################
	@property
	def azi_coords(self):
		'''
		Numpy array of corresponding azimuth to the reflectivity data. 
		Must be 1D numpy array
		'''
		try:
			return self._azi_coords
		except AttributeError:
			return 0
			
	@azi_coords.setter
	def azi_coords(self, new_azi_coords):
		assert isinstance(new_azi_coords, np.ndarray), 'new azi_coords not a numpy array' 
		assert len(new_azi_coords.shape) == 1, 'new azi_coords is not 1D'
		self._azi_coords = new_azi_coords
	
	
	
	
	
	####################################################################
	### azimuth coordinates of artificially increased resolution ###
	####################################################################
	@property
	def azi_coords_inc(self):
		
		'''
		Numpy array of corresponding azimuth to the reflectivity data 
		with artificially increased azimuth resolution. 
		Must be 1D numpy array
		'''
		
		try:
			return self._azi_coords_inc
		except AttributeError:
			return 0
		
	@azi_coords_inc.setter
	def azi_coords_inc(self, new_azi_coords_inc):
		assert isinstance(new_azi_coords_inc, np.ndarray), 'new azi_coords_inc not a numpy array' 
		assert len(new_azi_coords_inc.shape) == 1, 'new azi_coords_inc is not 1D'
		self._azi_coords_inc = new_azi_coords_inc
	
	
	
	
	
	####################################################################
	### longitude coordinates in rotated pole coordinates ###
	####################################################################
	@property
	def lon_rota(self):
		
		'''
		Longitude coordinates of data points in rotated pole coordinate 
		system. Must be 2D numpy array.
		'''
		
		try:
			return self._lon_rota
		except AttributeError:
			return 0
		
			
	@lon_rota.setter
	def lon_rota(self, new_lon_rota):
		assert isinstance(new_lon_rota, np.ndarray), 'new lon_rota is no numpy array'
		assert len(new_lon_rota.shape) == 2, 'new lon_rota is not 2-dimensional'
		self._lon_rota = new_lon_rota
		
	
	
	
	
	
	####################################################################
	### latitude coordinates in rotated pole coordinates ###
	####################################################################
	@property
	def lat_rota(self):
		
		'''
		Latitude coordinates of data points in rotated pole coordinate 
		system. Must be 2D numpy array.
		'''
		
		try:
			return self._lat_rota
		except AttributeError:
			return 0
		
			
	@lat_rota.setter
	def lat_rota(self, new_lat_rota):
		assert isinstance(new_lat_rota, np.ndarray), 'new lat_rota is no numpy array'
		assert len(new_lat_rota.shape) == 2, 'new lat_rota is not 2-dimensional'
		self._lat_rota = new_lat_rota
		
		
		
		
		
	####################################################################
	### reflectivity data ###
	####################################################################	
	@property
	def refl(self):
		
		'''
		Reflectivity measured by the radar. Must be a 2D numpy array.
		'''
		
		try:
			return self._refl
		except AttributeError:
			return 0
		
			
	@refl.setter
	def refl(self, new_refl):
		assert isinstance(new_refl, np.ndarray), 'new refl is no numpy array'
		assert len(new_refl.shape) == 2, 'new refl is not 2-dimensional'
		self._refl = new_refl





	####################################################################
	### reflectivity data with increased azimuth resolution ###
	####################################################################
	@property
	def refl_inc(self):
		
		'''
		Reflectivity array with artificially increased azimuth 
		resolution. Must be 2D numpy array.
		'''
		
		try:
			return self._refl_inc
		except AttributeError:
			return 0
		
			
	@refl_inc.setter
	def refl_inc(self, new_refl_inc):
		assert isinstance(new_refl_inc, np.ndarray), 'new refl_inc is no numpy array'
		assert len(new_refl_inc.shape) == 2, 'new refl_inc is not 2-dimensional'
		self._refl_inc = new_refl_inc





########################################################################
### class for the new defined cartesian grid ###
########################################################################
class CartesianGrid:
	
	'''
	Object for a new defined cartesian grid, which can be used to plot
	data from different radars.
	'''
	
	
	
	
	
	####################################################################
	### Initialization method ###
	####################################################################
	def __init__(self,grid_par,radar):
		
		'''
		Saves the grid paramaters to a GridParameter-object.
		'''
		
		###create gridParameter object, which has defined grid parameters
		grid = GridParameter()
		
		###read the grid definition
		lon_start 		= grid_par[0][0]									#starting longitude
		lon_end			= grid_par[0][1]									#ending longitude
		lat_start 		= grid_par[1][0]									#starting latitude
		lat_end			= grid_par[1][1]									#ending latitude
		resolution		= float(grid_par[2])								#grid resolution in m
		
		###If lon/lat_start/end is min/max, whole data shall be plotted and min/max lon/lat must be calculated
		if lon_start == 'min':
			lon_start = min(np.reshape(radar.data.lon_rota,radar.data.azi_rays*radar.data.r_bins*res_factor))
		if lon_end == 'max':
			lon_end = max(np.reshape(radar.data.lon_rota,radar.data.azi_rays*radar.data.r_bins*res_factor))
		if lat_start == 'min':
			lat_start = min(np.reshape(radar.data.lat_rota,radar.data.azi_rays*radar.data.r_bins*res_factor))
		if lat_end == 'max':
			lat_end = max(np.reshape(radar.data.lat_rota,radar.data.azi_rays*radar.data.r_bins*res_factor))
	
		###save grid definition to gridParameter-object
		grid.lon_start 	= lon_start											#starting longitude
		grid.lon_end 	= lon_end											#ending longitude
		grid.lat_start 	= lat_start											#starting latitude
		grid.lat_end 	= lat_end											#ending latitude
		grid.res_m		= resolution										#resolution in m
		grid.res_deg	= 1/(60*1852/resolution) 							#resolution in ° --> 1° equals 60 NM, equals 60*1852 m. --> 250m equals 1°/(60*1852/250)
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
		index_matrix = np.empty((self.par.lat_dim,self.par.lon_dim), dtype=np.object_)
	
		###fill empty matrix with empty lists, to be able to save more than one location, in case more than one radar data point falls into the same grid box
		for line_nr in range(len(index_matrix)):																					#lines of index-matrix (latitudes)
			for row_nr in range(len(index_matrix[line_nr])): 																		#rows of index-matrix (longitudes)
				index_matrix[line_nr][row_nr] = []																					#change entry of index matrix to empty list
		
		###loop through all radar data points and write the location (location = index in array of polar coordinates) of data points, which are not outside of new grid boundaries to the corresponding list of the index-matrix. 		
		for azi_nr in range(len(lon_index)):																						#lines of lon/lat_index (azimuth angles)
			for range_nr in range(len(lon_index[azi_nr])): 																			#rows of lon/lat_index (ranges)
				if (lat_index[azi_nr][range_nr] <= self.par.lat_dim -1  and lat_index[azi_nr][range_nr] >= 0): 							#check, if data point is north or east of grid boundary 
					if (lon_index[azi_nr][range_nr] <= self.par.lon_dim -1 and lon_index[azi_nr][range_nr] >= 0): 						#check, if data point is south or west of grid boundary
						index_matrix[int(lat_index[azi_nr][range_nr])][int(lon_index[azi_nr][range_nr])].append([azi_nr,range_nr]) 	#append grid box of new cartesian grid (=entry of index-matrix), in which the radar data point falls, with location of radar data point. 
				
		###save matrix to dat.file
		index_matrix.dump(index_matrix_file)
			
	
	
	
	
	####################################################################
	### Interpolation method ###
	####################################################################
	def data_to_grid(self,index_matrix_file):
		
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
				
	
		
	

########################################################################
### class for saving cartesian grid parameters ###
########################################################################
class GridParameter:
	
	'''
	Defines cartesian grid parameters as properties.
	'''
	
	def __init__(self):
		
		'''
		Does nothing so far
		'''
		
		pass
	
	
	
	
	
	####################################################################
	### starting longitude of cartesian grid ###
	####################################################################
	@property
	def lon_start(self):
		
		'''
		Longitude coordinate (in rotated pole system) at which the
		cartesian grid begins. Must be float or 'min', which means
		smallest longitude of all radar data points is starting lon.
		'''
		
		try:
			return self._lon_start
		except AttributeError:
			return 0
			
	@lon_start.setter
	def lon_start(self,new_lon_start):
		assert (isinstance(new_lon_start, float) or new_lon_start == 'min'), 'new_lon_start is not a float or "min"'
		self._lon_start = new_lon_start
		
		
		
		
		
	####################################################################
	### starting latitude of cartesian grid ###
	####################################################################
	@property
	def lat_start(self):
		
		'''
		Latitude coordinate (in rotated pole system) at which the
		cartesian grid begins. Must be float or 'min', which means
		smallest latitude of all radar data points is starting lat.
		'''
		
		try:
			return self._lat_start
		except AttributeError:
			return 0
			
	@lat_start.setter
	def lat_start(self,new_lat_start):
		assert (isinstance(new_lat_start, float) or new_lat_start == 'min'), 'new_lat_start is not a float or "min"'
		self._lat_start = new_lat_start
		
		
		
		
		
	####################################################################
	### ending longitude of cartesian grid ###
	####################################################################
	@property
	def lon_end(self):
		
		'''
		Longitude coordinate (in rotated pole system) at which the
		cartesian grid ends. Must be float or 'max', which means
		largest longitude of all radar data points is ending lon.
		'''
		
		try:
			return self._lon_end
		except AttributeError:
			return 0
			
	@lon_end.setter
	def lon_end(self,new_lon_end):
		assert (isinstance(new_lon_end, float) or new_lon_end == 'max'), 'new_lon_end is not a float or "max"'
		self._lon_end = new_lon_end
		
		
		
		
		
	####################################################################
	### ending latitude of cartesian grid ###
	####################################################################
	@property
	def lat_end(self):
		
		'''
		Latitude coordinate (in rotated pole system) at which the
		cartesian grid ends. Must be float or 'max', which means
		largest latitude of all radar data points is ending lat.
		'''
		
		try:
			return self._lat_end
		except AttributeError:
			return 0
			
	@lat_end.setter
	def lat_end(self,new_lat_end):
		assert (isinstance(new_lat_end, float) or new_lat_end == 'max'),'new_lat_end is not a float or "max"'
		self._lat_end = new_lat_end
		
		
		
		
		
	####################################################################
	### grid resolution in meters ###
	####################################################################
	@property
	def res_m(self):
		
		'''
		Resolution of cartesian grid in m. Must be float.
		'''
		
		try:
			return self._res_m
		except AttributeError:
			return 0
			
	@res_m.setter
	def res_m(self,new_res_m):
		assert isinstance(new_res_m, float), 'new_res_m is not a float'
		self._res_m = new_res_m





	####################################################################
	### grid resolution in degrees ###
	####################################################################
	@property
	def res_deg(self):
		
		'''
		Resolution of cartesian grid in degree. Must be float.
		'''
		
		try:
			return self._res_deg
		except AttributeError:
			return 0
			
	@res_deg.setter
	def res_deg(self,new_res_deg):
		assert isinstance(new_res_deg, float), 'new_res_deg is not a float'
		self._res_deg = new_res_deg
	
	
	
	
		
	####################################################################
	### number of grid - rows ###
	####################################################################
	@property
	def lon_dim(self):
		
		'''
		Number of rows (lons) in cartesian grid. Must be an integer.
		'''
		
		try:
			return self._lon_dim
		except AttributeError:
			return 0
			
	@lon_dim.setter
	def lon_dim(self,new_lon_dim):
		assert isinstance(new_lon_dim, int), 'new_lon_dim is not an integer'
		self._lon_dim = new_lon_dim	
		
		
		
		
		
	####################################################################
	### number of grid - lines ###
	####################################################################
	@property
	def lat_dim(self):
		
		'''
		Number of lines (lat) of cartesian grid. Must be an integer.
		'''
		
		try:
			return self._lat_dim
		except AttributeError:
			return 0
			
	@lat_dim.setter
	def lat_dim(self,new_lat_dim):
		assert isinstance(new_lat_dim, int), 'new_lat_dim is not an integer'
		self._lat_dim = new_lat_dim
	
		
		
		
				
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
	radar = Pattern('dbz')
elif re.search('level2_hdcp2',file_name):
	radar = Pattern(refl_key)

### read in data
radar.read_file(file_name)





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
index_matrix_file 	= 'index_matrix_'+str(radar.name)+'_'+str(new_grid.par.lon_start)+'_'+str(new_grid.par.lon_end)+'_'+str(new_grid.par.lat_start)+'_'+str(new_grid.par.lat_end)+'_'+str(new_grid.par.res_m)+'_'+ str(res_factor)+'.dat'
		
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

reflectivity = new_grid.data_to_grid(index_matrix_file)





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

