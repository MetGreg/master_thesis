########################################################################
### class for saving general radar properties ###
########################################################################





########################################################################
### modules ###
########################################################################
import numpy as np





########################################################################
### Radardata class ###
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

