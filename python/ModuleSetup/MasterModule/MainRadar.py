########################################################################
### main Radar-Object ###
########################################################################





########################################################################
### modules ###
########################################################################
import wradlib
import cartopy.crs as ccrs
import numpy as np





########################################################################
### Main Radar class ###
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
		
	
