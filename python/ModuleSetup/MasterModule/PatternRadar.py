########################################################################
### sub-class for Pattern-data ###
########################################################################





########################################################################
### modules ###
########################################################################
import numpy as np
from datetime import datetime
from netCDF4 import Dataset
from .MainRadar import Radar
from .RadarData import RadarData	
	
	
	

########################################################################
### Pattern Class ###	
########################################################################
class Pattern(Radar):
	
	'''
	Sub-Object of Radar. Contains all methods specific designed for
	Pattern-data.
	'''
	
	
	
	
	
	####################################################################
	### initialization method ###
	####################################################################
	def __init__(self,refl_key,minute,file_name,res_factor):
		
		'''
		Saves name of radar refl_key to object, which defines at which 
		processing step the reflectivity data will be plottet. 
		refl_key must be set in parameters.
		'''
		
		self.file_name		= file_name	#name of data file
		self.minute		= minute		#minute of file, that shall be plottd
		self.name 		= 'pattern' 	#name of the radar
		self.refl_key 		= refl_key	#processing step
		self.res_factor	= res_factor	#factor, by which the azimuth resoltion will be artificially increased
		
	
	
	
	
	####################################################################
	### method to read in pattern data (nc.files) ###
	####################################################################	
	def read_file(self):
		
		'''
		Read and save the important (for plotting) information of
		the pattern data. If more information is wished, check the data
		file with ncdump -h or ncview. 
		'''
	
		###create a RadarData-object to generalize the radar-properties.
		radar_data 				= RadarData()
		
		###open data file
		nc 						= Dataset(self.file_name, mode='r')
		
		###read all important informations
		lon_site					= nc.variables['lon'][:]										#longitude coordinate of radar site
		lat_site					= nc.variables['lat'][:]										#latitude coordinate of radar site
		r_bins					= nc.dimensions['range'].size									#number of range bins
		azi_rays					= nc.dimensions['azi'].size 									#number of azimuth rays
		azi_start					= nc.variables['azi'][0]										#starting value of azimuth angle
		azi_steps					= nc.variables['azi'][1] - azi_start							#azimuth angle steps between two measurements
		range_coords				= nc.variables['range'][:]									#array of to data points corresponding range coordinates
		azi_coords				= nc.variables['azi'][:]										#array of to data points corresponding azimuth coordinates
		refl						= nc.variables[self.refl_key][:][int((self.minute - 0.5)*2)]		#array of measured reflectivity
		time_start				= nc.variables['time_bnds'][int((self.minute - 0.5)*2)][0]			#time in epoch (linux time) at which radar scan started
		time_end					= nc.variables['time_bnds'][int((self.minute - 0.5)*2)][1]			#time in epoch (linux time) at which radar scan ended
		
		###save the data to RadarData object
		radar_data.lon_site			= float(lon_site)											#longitude coordinate of radar site
		radar_data.lat_site			= float(lat_site)											#latitude coordinate of radar site
		radar_data.r_bins			= int(r_bins)												#number of range bins
		radar_data.azi_rays			= int(azi_rays)											#number of azimuth rays
		radar_data.range_coords		= range_coords												#array of to data points corresponding range coordinates
		radar_data.azi_coords		= azi_coords												#array of to data points corresponding azimuth coordinates
		radar_data.azi_coords_inc	= np.arange(azi_start,azi_steps*azi_rays,azi_steps/self.res_factor)	#array of corresponding azimuth coordinates to data points with artificially increased resolution
		radar_data.refl			= refl													#array of measured reflectivity
		radar_data.time_start		= datetime.utcfromtimestamp(time_start)							#time in utc at which radar scan started
		radar_data.time_end			= datetime.utcfromtimestamp(time_end)							#time in utc at which radar scan ended
		
		###save the data to Pattern object
		self.data 				= radar_data
		

