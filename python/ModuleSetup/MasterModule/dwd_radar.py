#DwdRadar class

'''
This file is reserved for the DwdRadar class.
'''





########################################################################
### import modules ###
########################################################################

'''
Imports all modules needed for this class.
'''

#python modules
import h5py
import numpy as np
from datetime import datetime

#MasterModule
from .main_radar import Radar
from .radar_data import RadarData





########################################################################
### dwd class ###
########################################################################
class DwdRadar(Radar):
    
    '''
    DwdRadar class. Contains all methods that are specific designed
    for Dwd-data. Inherits from Radar.
    '''
    



    
    ####################################################################
    ### Initialization - method ###
    ####################################################################
    def __init__(self,radar_par):
        
        '''
        Save name of radar to object and call super class.
        '''
        
        #call init method of super class
        super().__init__(radar_par)

        #save name of radar to object
        self.name = 'dwd'         
        
    
    


    ####################################################################
    ### method to read in dwd-data (hdf5) ###
    ####################################################################
    def read_file(self):
    
        '''
        Reads dwd radar data. Only attributes needed for my calculations 
        are read in. If more information about the file and the 
        attributes is wished, check out the hdf5-file with hdfview or 
        hd5dump -H
        '''
        
        #open file
        with h5py.File(self.file_name,'r') as h5py_file:
            
            #create RadarData-Object to save generalized radar data 
            radar_data = RadarData()
            




            ############################################################
            ### read in radar data ###
            ############################################################
            
            '''
            Reads in radar data.
            '''

            #lon/lat coordinates of radar site
            lon_site     = h5py_file.get('where').attrs['lon']                           
            lat_site     = h5py_file.get('where').attrs['lat']
            
            #elevation of radar beam
            ele          = h5py_file.get('dataset1/where')\
                            .attrs['elangle']

            #number of azimuth rays(360 --> 1° steps)
            azi_rays     = h5py_file.get('dataset1/where')\
                            .attrs['nrays'] 

            #number of radius bins (600 --> 250m steps up to 150000m)                           
            r_bins       = h5py_file.get('dataset1/where')\
                            .attrs['nbins']

            #azimuth angle of first measurement(take care of 360 --> 0°)
            azi_start    = (h5py_file.get('dataset1/where')\
                            .attrs['startaz'] + 360) % 360
            
            #range of first measurement                    
            r_start      = h5py_file.get('dataset1/where')\
                            .attrs['rstart']

            #angle step between 2 measurements
            azi_steps    = h5py_file.get('dataset1/how')\
                            .attrs['angle_step']

            #distance between 2 measurements on radius-axis (250m)                    
            r_steps      = h5py_file.get('dataset1/where').attrs['rscale']                 
 
            #azi coords of data pts (near edge of grid box)
            azi_coords   = np.arange(
                azi_start,azi_steps*azi_rays + azi_start,azi_steps
                )  

            #take care of transition from 360 to 0
            azi_coords   = (azi_coords + 360) % 360
            
            #range coords of data pts in [m] (far edge of grid cell) 
            range_coords = np.arange(
                r_start+r_steps,r_steps*r_bins +r_start+r_steps,r_steps
                )  
            
            #factor to correct the dwd refl to ordinary dbz values      
            gain         = h5py_file.get('dataset1/data1/what')\
                                  .attrs['gain']

            #Offset, to correct the dwd refl to ordinary dbz values 
            offset       = h5py_file.get('dataset1/data1/what')\
                                  .attrs['offset']   
            #uncorrected data 
            refl         = h5py_file.get('dataset1/data1/data')

            #time at which scan started                         
            time_start   = h5py_file.get('how').attrs['startepochs']
            time_start   = datetime.utcfromtimestamp(time_start) 

            #time at which scan ended                       
            time_end     = h5py_file.get('how').attrs['endepochs']                        
            time_end     = datetime.utcfromtimestamp(time_end)





            ############################################################
            ### save data to RadarData-Object ###
            ############################################################
            
            '''
            Saves radar data to object.
            '''

            #lon/lat coordinates of radar site
            radar_data.lon_site     = lon_site                                               
            radar_data.lat_site     = lat_site
            
            #elevation of radar beam
            radar_data.ele          = ele    

            #number of azimuth rays(360 --> 1° steps)
            radar_data.azi_rays     = int(azi_rays)   

            #number of radius bins (600 --> 250m steps up to 150000m)                                    
            radar_data.r_bins       = int(r_bins)                                                

            #starting value of azimuth angle
            radar_data.azi_start    = float(azi_start)

            #starting value of range
            radar_data.r_start      = float(r_start)
            
            #steps between 2 measurements in azimuth
            radar_data.azi_steps    = float(azi_steps)

            #steps between 2 measurements in range
            radar_data.r_steps      = float(r_steps)

            #azi coords of data pts (near edge of grid box)
            radar_data.azi_coords   = azi_coords
            
            #range coords of data pts (far edge of grid cell)
            radar_data.range_coords = range_coords

            #corrected data
            radar_data.refl         = refl * gain + offset    

            #time at which radar scan started in utc                        
            radar_data.time_start   = time_start 
            
            #time at which radar scan ended in utc
            radar_data.time_end     = time_end
                          
            #save RadarData-Object to DwdRadar-Object
            self.data               = radar_data
            
        
        
