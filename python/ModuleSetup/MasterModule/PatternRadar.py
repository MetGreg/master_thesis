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
    def __init__(self,file_name,minute,offset,proc_key,res_fac):
        
        '''
        Saves name of radar proc_key to object, which defines at which 
        processing step the reflectivity data will be plottet. 
        proc_key must be set in parameters.
        '''
        
        self.file_name = file_name  #name of data file
        self.minute    = minute     #minute to be plotted
        self.name      = 'pattern'  #name of the radar
        self.offset    = offset     #offset of azimuth angle
        self.proc_key  = proc_key   #key of processing step
        self.res_fac   = res_fac    #factor to incr. azi. res.
        
    
    
    

    ####################################################################
    ### method to read in pattern data (nc.files) ###
    ####################################################################    
    def read_file(self):
        
        '''
        Read and save the important (for plotting) information of
        the pattern data. If more information is wished, check the data
        file with ncdump -h or ncview. 
        '''
    
        #create a RadarData-object to generalize the radar-properties.
        radar_data                = RadarData()
        
        #open data file
        nc                        = Dataset(self.file_name, mode='r')
        




        ################################################################
        ### read in data ###
        ################################################################
        
        '''
        reads in the data
        '''

        #lon/lat coords of site
        lon_site    = nc.variables['lon'][:]                                        
        lat_site    = nc.variables['lat'][:]

        #number of azimuth rays
        azi_rays    = nc.dimensions['azi'].size                                    
        
        #number of range bins                                        
        r_bins      = nc.dimensions['range'].size 

        #starting value of azimuth angle
        azi_start   =(nc.variables['azi'][0] + self.offset + 360) % 360  
        
        #starting value of range
        r_start     = nc.variables['range'][0]
        
        #azimuth angle steps between two measurements                                        
        azi_steps   = (nc.variables['azi'][1] - nc.variables['azi'][0]\
                        + 360) % 360
        
        #steps between 2 measurments in range
        r_steps    = nc.variables['range'][1] - nc.variables['range'][0]
                                         
        #array of to data points corresponding azimuth coordinates
        azi_coords  =(nc.variables['azi'][:] + self.offset + 360) % 360
        
        #array of to data points corresponding range coordinates in [m]
        range_coords = nc.variables['range'][:]                                    
        
        #array of measured reflectivity                                        
        refl        = nc.variables[self.proc_key][:][int(self.minute*2)] 
       
        #time at which radar scan started
        time_start  = nc.variables['time_bnds'][int(self.minute*2)][0]
        time_start  = datetime.utcfromtimestamp(time_start)

        #time at which radar scan ended
        time_end    = nc.variables['time_bnds'][int(self.minute*2)][1]            
        time_end    = datetime.utcfromtimestamp(time_end)





        ################################################################
        ### save the data to RadarData object ###
        ################################################################
        
        '''
        saves data to radarData object.
        '''

        #lon/lat coords site
        radar_data.lon_site      = float(lon_site)                                            
        radar_data.lat_site      = float(lat_site)                                            
        
        #number of azimuth rays
        radar_data.azi_rays      = int(azi_rays)  
        
        #number of range bins
        radar_data.r_bins        = int(r_bins)                                                
        
        #starting value of azimuth angle
        radar_data.azi_start     = float(azi_start)

        #starting value of range
        radar_data.r_start       = float(r_start)

        #steps between 2 measurements in azimuth
        radar_data.azi_steps     = float(azi_steps)

        #steps between 2 measurements in range
        radar_data.r_steps       = float(r_steps)

        #array of to data points corresponding azimuth coordinates
        radar_data.azi_coords    = azi_coords
                                                  
        #array of to data points corresponding range coordinates
        radar_data.range_coords  = range_coords
        
        #array of measured reflectivity
        radar_data.refl          = refl                                                  
        
        #time in utc at which radar scan started
        radar_data.time_start    = time_start                            
        
        #time in utc at which radar scan ended
        radar_data.time_end      = time_end                          
        
        #save the data to Pattern object
        self.data                = radar_data
        

