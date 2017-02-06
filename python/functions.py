########################################################################
### function to read in dwd-data in hdf5 format ###
########################################################################
def read_dwd_hdf5(data_file):
	


	####################################################################
	### modules ###
	####################################################################
	
	import h5py
	
		
		
	####################################################################
	### read in hdf5-file ###
	####################################################################
		
	class DWD_hdf5:
		
		def __init__(self,data_file):
			
			with h5py.File(data_file,'r') as h5py_file:
				
				
				
				########################################################
				### read in some attributes saved in the hdf5 file ###
				########################################################
				
				'''
				Only attributes needed for my calculations are read in 
				here. There's more information in the hdf5-file though. 
				If more information about the file and the attributes 
				is wished, check out the hdf5-file with hdfview or 
				hd5dump -H
				'''
				
				###information about the coords and height of radar
				self.height			= h5py_file.get('where').attrs['height']
				self.lat			= h5py_file.get('where').attrs['lat']
				self.lon			= h5py_file.get('where').attrs['lon']
				self.quantity		= h5py_file.get('dataset1/data1/what').attrs['quantity'] 	#quantity should be dbzh (horizontal reflectivity). This is the case for data1 (probabably for alle files). Check this once, to make sure it is the case.
				self.nbins			= h5py_file.get('dataset1/where').attrs['nbins']			#dimension of radius  (600 --> 250m steps up to 150000m)
				self.nrays			= h5py_file.get('dataset1/where').attrs['nrays'] 			#dimension of azimuth (360 --> 1° steps)
				self.rscale			= h5py_file.get('dataset1/where').attrs['rscale'] 			#distance between 2 measurements on radius-axis (250m)
				
				###factor (gain) and offset. Needed to correct the dwd reflectivity to normal dbz values 
				gain 				= h5py_file.get('dataset1/data1/what').attrs['gain']		
				offset 				= h5py_file.get('dataset1/data1/what').attrs['offset']		
				
				###save data
				data				= h5py_file.get('dataset1/data1/data')	#uncorrected data 
				self.data			= data * gain + offset					#corrected data
			
	
	
	dwd = DWD_hdf5(data_file)
	
	
	return dwd
	


########################################################################
### function to calculate pixel center of radar coordinates ###
########################################################################

'''
Radar data is saved at specific points in polar coordinates. But
a radar measurement is valid for a box, not only for one point.
This function calculates the coordinates of the center of each 
measurement box.
It is assumed, that for a box, the related data point is at the far edge 
in range and at the near edge in azimuth compared to the radar location.
(structure of pattern data).
'''

def get_pixel_center(rad_range, rad_azimuth): 
	
	
	
	####################################################################
	### modules ###
	####################################################################
	
	import numpy as np
	
	
	
	####################################################################
	### Calculate polar coords of middle pixel for each box ###
	####################################################################
	
	rad_range 	= np.append(rad_range, rad_range[-1] + (rad_range[-1]-rad_range[-2]))
	rad_range 	= (rad_range[:-1] - (rad_range[1:]-rad_range[:-1])/2.)
	rad_azimuth = np.append(rad_azimuth, rad_azimuth[-1] + (rad_azimuth[-1]-rad_azimuth[-2]))
	rad_azimuth = (rad_azimuth[:-1] + (rad_azimuth[1:]-rad_azimuth[:-1])/2.)
	  
	pixel_center 	= np.meshgrid(rad_range, rad_azimuth)
	
	return pixel_center



########################################################################
### function to bring lon/lat coordinates to rotated pole coordinates ##
########################################################################

def rotate_pole(lon,lat):
	
	
	
	####################################################################
	### modules ###
	####################################################################
	
	import cartopy.crs as ccrs
	
	
	
	####################################################################
	### coordinate transformation ###
	####################################################################
	
	### coordinates rotated pole
	rotated_pole = [-170.415, 36.0625]

	###calculate coordinates in rotated pole coordinate system
	proj = ccrs.RotatedPole(rotated_pole[0], rotated_pole[1])
	rotated_coords = proj.transform_points(ccrs.Geodetic(), lon, lat)
	
	return rotated_coords



########################################################################
### function to create index-matrix ####################################
########################################################################

'''
For my work, it is necessary to bring the data to a different
coordinate system. 
This function is used to create a matrix, that - for each grid point of 
the new coordinate system - contains information about which data points
of the old coordinate system fall into this grid point.  
The Index-Matrix is then saved to a dat.file to avoid calculating the
matrix again and again.
'''

def get_index(lon_index,lat_index):
	
	###modules
	import numpy as np
	
	###define name of output file
	output_file = 'index_matrix.dat'
	
	###create empty matrix of shape (1199,1199) which is the resolution of the new coordinate system (shouldn't be hardcoded)
	
	####################################################################
	###CHANGE HARDCODING!!!
	####################################################################
	index_matrix = np.empty((1199,1199,), dtype=np.object_)

	###fill empty matrix with empty lists, to be able to save more than one location, in case more than one data point of old coordinate system falls into the new grid box
	for line_nr in range(len(index_matrix)):
		for row_nr in range(len(index_matrix[line_nr])):
			index_matrix[line_nr][row_nr] = []
	
	
	
	###go through each grid box of the old coordinate system and write location of this data point to the corresponding list in the index-matrix 		
	for azi_nr in range(len(lon_index)):
		for range_nr in range(len(lon_index[azi_nr])):
			
			index_matrix[lat_index[azi_nr][range_nr]][lon_index[azi_nr][range_nr]].append([azi_nr,range_nr])
	
	###save matrix into dat.file
	index_matrix.dump(output_file)
	
	

########################################################################
### ###
########################################################################

def raise_azi_res(data,factor):
	
	import numpy as np
	
	art_data = []
	
	for azi_data in data:
		for y in range(factor):
			art_data.append(azi_data)
			
	return art_data
