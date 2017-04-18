###PatternRadar class

'''
This file is reserved for the PatternRadar class.
'''





########################################################################
### modules ###
########################################################################

'''
Import all modules needed for this class.
'''

#python modules 
from netCDF4  import Dataset
from datetime import datetime

#MasterModule
from .main_radar import Radar
from .radar_data import RadarData    
    
    
    


########################################################################
### Pattern Class ###    
########################################################################
class PatternRadar(Radar):
    
    '''
    PatternRadar class. Contains all methods specific designed for
    Pattern-data. Inherits from Radar class.
    '''
    
    
    
    
    
    ####################################################################
    ### initialization method ###
    ####################################################################
    def __init__(self,radar_par,offset):
        
        '''
        Saves radar name and radar proc_key to object, which defines at 
        which processing step the reflectivity data will be plottet. 
        proc_key must be set in parameters.
        '''
        
        super().__init__(radar_par)
        
        #save name of the radar to object
        self.name   = 'pattern'

        #save offset, by which the pattern radar is wrong  
        self.offset = offset
    
    
    


    ####################################################################
    ### method to read in pattern data (nc.files) ###
    ####################################################################    
    def read_file(self):
        
        '''
        Read and save the important information of the pattern data. 
        If more information is wished, check the data file with 
        ncdump -h or ncview. 

        Input: None

        Output: None
        '''
    
        #create a RadarData-object to generalize the radar-properties.
        radar_data = RadarData()
        
        #open data file
        nc         = Dataset(self.file_name, mode='r')
        




        ################################################################
        ### read in data ###
        ################################################################
        
        '''
        Reads in the data.
        '''

        #lon/lat coords of site
        lon_site     = nc.variables['lon'][:]                                        
        lat_site     = nc.variables['lat'][:]
        
        #elevation of radar beam
        ele          = nc.variables['ele'][:]

        #number of azimuth rays
        azi_rays     = nc.dimensions['azi'].size                                    
        
        #number of range bins                                        
        r_bins       = nc.dimensions['range'].size 

        #starting value of azimuth angle
        azi_start    =(nc.variables['azi'][0] + self.offset + 360) % 360  
        
        #starting value of range
        r_start      = nc.variables['range'][0]
        
        #azimuth angle steps between two measurements                                        
        azi_steps    = (nc.variables['azi'][1] - nc.variables['azi'][0]\
                        + 360) % 360
        
        #steps between 2 measurments in range
        r_steps = nc.variables['range'][1] - nc.variables['range'][0]
                                         
        #array of to data points corresponding azimuth coordinates
        azi_coords   =(nc.variables['azi'][:] + self.offset + 360) % 360
        
        #array of to data points corresponding range coordinates in [m]
        range_coords = nc.variables['range'][:]                                    
        
        #array of measured reflectivity                                        
        refl = nc.variables[self.proc_key][:][int(self.minute*2)] 
       
        #time at which radar scan started
        time_start   = nc.variables['time_bnds'][int(self.minute*2)][0]
        time_start   = datetime.utcfromtimestamp(time_start)

        #time at which radar scan ended
        time_end     = nc.variables['time_bnds'][int(self.minute*2)][1]            
        time_end     = datetime.utcfromtimestamp(time_end)





        ################################################################
        ### save the data to RadarData object ###
        ################################################################
        
        '''
        Saves data to radarData object.
        '''

        #lon/lat coords site
        radar_data.lon_site     = float(lon_site)                                            
        radar_data.lat_site     = float(lat_site)                                            
        
        #elevation of radar beam
        radar_data.ele          = float(ele)

        #number of azimuth rays
        radar_data.azi_rays     = int(azi_rays)  
        
        #number of range bins
        radar_data.r_bins       = int(r_bins)                                                
        
        #starting value of azimuth angle
        radar_data.azi_start    = float(azi_start)

        #starting value of range
        radar_data.r_start      = float(r_start)

        #steps between 2 measurements in azimuth
        radar_data.azi_steps    = float(azi_steps)

        #steps between 2 measurements in range
        radar_data.r_steps      = float(r_steps)

        #array of to data points corresponding azimuth coordinates
        radar_data.azi_coords   = azi_coords
                                                  
        #array of to data points corresponding range coordinates
        radar_data.range_coords = range_coords
        
        #array of measured reflectivity
        radar_data.refl         = refl                                                  
        
        #time in utc at which radar scan started
        radar_data.time_start   = time_start                            
        
        #time in utc at which radar scan ended
        radar_data.time_end     = time_end                          
        
        #save the data to Pattern object
        self.data               = radar_data
        

