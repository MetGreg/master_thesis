########################################################################
### sub-class for Dwd-data ###
########################################################################





########################################################################
### import modules ###
########################################################################
import h5py
import numpy as np
from datetime import datetime
from .MainRadar import Radar
from .RadarData import RadarData





########################################################################
### dwd class ###
########################################################################
class Dwd(Radar):
	
	'''
	Sub-Object of Radar. Contains all methods that are specific designed
	for Dwd-data.
	'''
	
	
	
	
	
	####################################################################
	### Initialization - method ###
	####################################################################
	def __init__(self,file_name,res_factor):
		
		'''
		Save name of radar to object
		'''
	
		self.name 		= 'dwd' 		#name of radar
		self.file_name 	= file_name 	#name of data file
		self.res_factor	= res_factor 	#factor, by which resolution of the radar data will be increased artificially
	
	
	
	####################################################################
	### method to read in dwd-data (hdf5) ###
	####################################################################
	def read_file(self):
	
		'''
		Reads dwd radar. Only attributes needed for my calculations are 
		read in. If more information about the file and the attributes 
		is wished, check out the hdf5-file with hdfview or 
		hd5dump -H
		'''
		
		###open file
		with h5py.File(self.file_name,'r') as h5py_file:
			
			###create RadarData-Object to save radar data generalized to this object	
			radar_data = RadarData()
			
			###read radar data
			lon_site					= h5py_file.get('where').attrs['lon']							#longitude coordinates of radar site
			lat_site					= h5py_file.get('where').attrs['lat']							#latitude coordinates of radar site
			r_bins					= h5py_file.get('dataset1/where').attrs['nbins']					#number of radius bins (600 --> 250m steps up to 150000m)
			r_start					= h5py_file.get('dataset1/where').attrs['rstart']					#range of first measurement
			r_steps					= h5py_file.get('dataset1/where').attrs['rscale'] 				#distance between 2 measurements on radius-axis (250m)
			azi_rays					= h5py_file.get('dataset1/where').attrs['nrays'] 					#number of azimuth rays(360 --> 1° steps)
			azi_start					= h5py_file.get('dataset1/where').attrs['startaz'] 				#azimuth angle of first measurement
			azi_steps					= h5py_file.get('dataset1/how').attrs['angle_step'] 				#angle step between 2 measurements
			gain 					= h5py_file.get('dataset1/data1/what').attrs['gain']				#factor (gain), which is needed to correct the dwd reflectivity to normal dbz values 
			offset 					= h5py_file.get('dataset1/data1/what').attrs['offset']				#Offset. Also needed to correct the dwd reflectivity to normal dbz values 
			refl						= h5py_file.get('dataset1/data1/data')							#uncorrected data 
			time_start				= h5py_file.get('how').attrs['startepochs']						#time at which scan started in epochs (linux time)
			time_end					= h5py_file.get('how').attrs['endepochs']						#time at which scan ended in epochs (linux time)
			
			
			###save data to RadarData-Object
			radar_data.lon_site			= lon_site												#longitude coordinates of radar site
			radar_data.lat_site			= lat_site												#latitude coordinates of radar site
			radar_data.r_bins			= int(r_bins)												#number of radius bins (600 --> 250m steps up to 150000m)
			radar_data.azi_rays			= int(azi_rays)											#number of azimuth rays(360 --> 1° steps)
			radar_data.range_coords		= np.arange(r_start+r_steps,r_steps*r_bins+r_start+r_steps,r_steps)	#array containing range coordinates of data points (at far edge of grid box)
			radar_data.azi_coords		= np.arange(azi_start,azi_steps*azi_rays,azi_steps)				#array containing azimuth coordinates of data points (at near edge of grid box)
			radar_data.azi_coords_inc	= np.arange(azi_start,azi_steps*azi_rays,azi_steps/self.res_factor)	#array containing azimuth coordinates of data points with artificially increased resolution
			radar_data.refl			= refl * gain + offset										#corrected data
			radar_data.time_start		= datetime.utcfromtimestamp(time_start)							#time at which radar scan started in utc
			radar_data.time_end			= datetime.utcfromtimestamp(time_end)							#time at which radar scan ended in utc
			
			###save RadarData-Object (which contains all the saved data) to DWD-Object
			self.data 				= radar_data
			
		
		
