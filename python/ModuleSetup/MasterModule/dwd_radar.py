'''This module only contains the DwdRadar class, which can be used for 
a typical Dwd datafile in hdf5-format.

'''
# Python modules
import h5py
import numpy as np
from datetime import datetime

# MasterModule
from .main_radar import Radar
from .radar_data import RadarData


class DwdRadar(Radar):
    '''Class for Dwd radar data in hdf5-format
    
    This class is designed for data coming from the "Deutscher 
    Wetterdienst" in hdf5-format. It is a subclass of the more general
    "Radar" class. Using this class, an hdf5-file from the DWD can be 
    read in to save all important information.
    
    Attributes:
        name (str): Name of the operating institute. In this case 'DWD'.
        offset (int): Angle, by which the radar is rotated. 0 for DWD
            radar.
        data (RadarData object): Used to save all kind of general radar 
            data and meta data.
            
    '''
    
    def __init__(self, radar_par):
        '''Initialization of object
        
        Saves attributes to object and calls Initialization method of 
        super class.
        
        Args:
            radar_par (dict): Radar parameters, e.g. name of file, 
                minute to be plotted, processing step, factor to 
                increase azimuth resolution, offset of radars azimuth 
                angle.
                
        '''
        # Call init method of super class
        super().__init__(radar_par)
        
        # Save attributes to object
        self.name = 'dwd'
        self.offset = 0 # dwd radar has no offset         
        
    def read_file(self, radar_par):
        '''Read in data
        
        Reads dwd radar data and saves data to object. Only attributes 
        needed for my calculations are read in. If more information 
        about the file and the attributes is wished, check out the 
        hdf5-file with hdfview or hd5dump -H.
       
        Args:
            radar_par (dict): Radar parameters, e.g. name of file, 
                minute to be plotted, processing step, factor to 
                increase azimuth resolution, offset of radars azimuth 
                angle.
            
        '''
        # Open file
        with h5py.File(radar_par['file'], 'r') as h5py_file:
            
            # Create RadarData-Object to save generalized radar data 
            radar_data = RadarData()
            
            # lon/lat coordinates of radar site
            radar_data.lon_site = h5py_file.get('where').attrs['lon']                           
            radar_data.lat_site = h5py_file.get('where').attrs['lat']
            
            # Elevation of radar beam
            radar_data.ele = (
                h5py_file.get('dataset1/where').attrs['elangle']
                )
            
            # Number of azimuth rays(360 --> 1° steps)
            radar_data.azi_rays = (
                h5py_file.get('dataset1/where').attrs['nrays'] 
                )
                
            # Number of radius bins (600 --> 250m steps up to 150000m)                           
            radar_data.r_bins = (
                h5py_file.get('dataset1/where').attrs['nbins']
                )
                
            # Azimuth angle of first measurement
            radar_data.azi_start = (
                h5py_file.get('dataset1/where').attrs['startaz']
                )
                
           # Range of first measurement                    
            radar_data.r_start = (
                h5py_file.get('dataset1/where').attrs['rstart']
                )
                
            # Angle step between 2 measurements
            radar_data.azi_steps = (
                h5py_file.get('dataset1/how').attrs['angle_step']
                )
                
            # Distance between 2 measurements on radius-axis (250m)                    
            radar_data.r_steps = (
                h5py_file.get('dataset1/where').attrs['rscale']                 
                )
                
            # Factor to correct the dwd refl to ordinary dbz values      
            gain = h5py_file.get('dataset1/data1/what').attrs['gain']

            # Offset, to correct the dwd refl to ordinary dbz values 
            offset = (
                h5py_file.get('dataset1/data1/what').attrs['offset']   
                )
                
            # Uncorrected data 
            refl = h5py_file.get('dataset1/data1/data')
            
            # Corrected data
            radar_data.refl = refl*gain + offset    

            # Time at which scan started                         
            time_start = h5py_file.get('how').attrs['startepochs']
            radar_data.time_start = datetime.utcfromtimestamp(
                time_start
                ) 
            
            # Time at which scan ended                       
            time_end = h5py_file.get('how').attrs['endepochs']                        
            radar_data.time_end = datetime.utcfromtimestamp(time_end)
            
            # Save RadarData-Object to DwdRadar-Object
            self.data = radar_data
