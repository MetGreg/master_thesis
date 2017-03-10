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
    def __init__(self,file_name,res_fac):
        
        '''
        Save name of radar to object
        '''

        self.name      = 'dwd'         #name of radar
        self.file_name = file_name     #name of data file
        self.res_fac   = res_fac       #factor to inc. azi. res
    
    
    


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
            reads in radar data
            '''

            #lon/lat coordinates of radar site
            lon_site   = h5py_file.get('where').attrs['lon']                           
            lat_site   = h5py_file.get('where').attrs['lat']

            #number of radius bins (600 --> 250m steps up to 150000m)                           
            r_bins     = h5py_file.get('dataset1/where').attrs['nbins']

            #range of first measurement                    
            r_start    = h5py_file.get('dataset1/where').attrs['rstart']

            #distance between 2 measurements on radius-axis (250m)                    
            r_steps    = h5py_file.get('dataset1/where').attrs['rscale']                 
            
            #number of azimuth rays(360 --> 1° steps)
            azi_rays   = h5py_file.get('dataset1/where').attrs['nrays']                    
            
            #azimuth angle of first measurement
            azi_start  = h5py_file.get('dataset1/where')\
                                  .attrs['startaz']
            
            #angle step between 2 measurements
            azi_steps  = h5py_file.get('dataset1/how')\
                                  .attrs['angle_step']
            
            #factor to correct the dwd refl to ordinary dbz values      
            gain       = h5py_file.get('dataset1/data1/what')\
                                  .attrs['gain']

            #Offset, to correct the dwd refl to ordinary dbz values 
            offset     = h5py_file.get('dataset1/data1/what')\
                                  .attrs['offset']   
            #uncorrected data 
            refl       = h5py_file.get('dataset1/data1/data')

            #time at which scan started in epochs (linux time)                            
            time_start = h5py_file.get('how').attrs['startepochs']

            #time at which scan ended in epochs (linux time)                        
            time_end   = h5py_file.get('how').attrs['endepochs']                        
            




            ############################################################
            ### save data to RadarData-Object ###
            ############################################################
            
            '''
            saves radar data to object
            '''

            #lon/lat coordinates of radar site
            radar_data.lon_site       = lon_site                                               
            radar_data.lat_site       = lat_site

            #number of radius bins (600 --> 250m steps up to 150000m)                                    
            radar_data.r_bins         = int(r_bins)                                                

            #number of azimuth rays(360 --> 1° steps)
            radar_data.azi_rays       = int(azi_rays)                                          
            
            #range coords of data pts (far edge of grid cell)
            radar_data.range_coords   = np.arange(
                                            r_start+r_steps,
                                            (r_steps*r_bins\
                                            +r_start+r_steps),
                                            r_steps
                                            )    
            
            #azi coords of data pts (near edge of grid box)
            radar_data.azi_coords     = np.arange(
                                            azi_start,
                                            azi_steps*azi_rays,
                                            azi_steps
                                            )    
            #azi. coords of data pts with artificially incr. res.
            radar_data.azi_coords_inc = np.arange(
                                            azi_start,
                                            azi_steps*azi_rays,
                                            azi_steps/self.res_fac
                                            )
 
            #corrected data
            radar_data.refl           = refl * gain + offset    

            #time at which radar scan started in utc                        
            radar_data.time_start     = datetime.utcfromtimestamp(
                                                time_start
                                                )    
            
            #time at which radar scan ended in utc
            radar_data.time_end       = datetime.utcfromtimestamp(
                                                time_end
                                                ) 
                          
            #save RadarData-Object to DWD-Object
            self.data                 = radar_data
            
        
        
