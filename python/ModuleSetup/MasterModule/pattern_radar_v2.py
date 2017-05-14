'''Class for version 2 of pattern radar data in 
`netCDF <https://www.unidata.ucar.edu/software/netcdf/>`_-format

'''
# Python modules 
from datetime import datetime
from netCDF4 import Dataset

# MasterModule
from .main_radar import Radar
from .radar_data import RadarData    

    
class PatternRadarV2(Radar):
    '''Class for version 2 of Pattern radar data in `netCDF <https://www.unidata.ucar.edu/software/netcdf/>`_-format
    
    This class is designed for the new processing (started at May 2017) 
    of data coming from the 'Precipitation and Attenuation Estimates 
    from a High-Resolution Weather Radar Network' (PATTERN) in 
    `netCDF <https://www.unidata.ucar.edu/software/netcdf/>`_-format. 
    It is a subclass of the more general :any:`Radar` class. Using this 
    class, a newly created PATTERN data file can be read in. 
    
    Note:
        There will be no distinction between starting and ending time 
        for the version 2 of pattern radar files.
        
    Attributes:
        name (:any:`str`): Name of operating institute. 'PATTERN' in 
            this case.
        offset (:any:`int`): Angle, by which the pattern radar is 
            rotated.
        data (:any:`RadarData`): Used to save all kind of general radar 
            data and meta data.
        
    '''
    
    def __init__(self, radar_par):
        '''Initialization of object
        
        Saves attributes to the object and calls the 
        :any:`Radar.__init__`-method.
        
        Args:
            radar_par (dict): Radar parameters, e.g. name of file, 
                minute to be plotted, processing step, factor to 
                increase azimuth resolution, offset of radars azimuth 
                angle.
                
        '''
        # Call init method of super class
        super().__init__(radar_par)
        
        # Save attributes
        self.name = 'PATTERN'
        self.offset = radar_par['offset']
        
    def read_file(self, radar_par):
        '''Read in data
        
        Reads pattern radar data and saves data to object. Only 
        attributes needed for my calculations are read in. If more 
        information about the file and the attributes is wished, check 
        out the 
        `netCDF <https://www.unidata.ucar.edu/software/netcdf/>`_-file 
        with ncview or ncdump -h.
        
        Args:
            radar_par (dict): Radar parameters, e.g. name of file, 
                minute to be plotted, processing step, factor to 
                increase azimuth resolution, offset of radars azimuth 
                angle.
                
        '''
        minute = radar_par['minute']
        
        # Create a RadarData object to generalize the radar properties
        radar_data = RadarData()
        
        # Open data file
        nc = Dataset(radar_par['file'], mode='r')

        # lon/lat coords of site
        if nc.longitude[-1] == 'E':
            radar_data.lon_site = float(nc.longitude[:-1])
        elif nc.longitude[-1] == 'W':
            radar_data.lon_site = -1*float(nc.longitude[:-1])
        if nc.latitude[-1] == 'N':
            radar_data.lat_site = float(nc.latitude[:-1])
        elif nc.latitude[-1] == 'S':
            radar_data.lat_site = -1*float(nc.latitude[:-1])
        
        # Elevation of radar beam
        radar_data.ele = nc.elevation

        # Number of azimuth rays
        radar_data.azi_rays = nc.dimensions['ang'].size                                    
        
        # Number of range bins                                        
        radar_data.r_bins = nc.dimensions['dist'].size 

        # Starting value of azimuth angle
        radar_data.azi_start = (
            (nc.variables['Azimuth'][0] + self.offset + 360) % 360  
            )
          
        # Starting value of range
        radar_data.r_start = float(nc.variables['Distance'][0])
        
        # Azimuth angle steps between two measurements                                        
        radar_data.azi_steps = (
            (nc.variables['Azimuth'][1] 
            - nc.variables['Azimuth'][0] 
            + 360) 
            % 360
            )
          
        # Steps between 2 measurments in range
        radar_data.r_steps = (
            nc.variables['Distance'][1] - nc.variables['Distance'][0]
            )
                                         
        # Array of measured reflectivity                                        
        radar_data.refl = nc.variables[
            'Att_Corr_Xband_Reflectivity'][:][int(minute*2)
            ] 
       
        # Time at which radar scan started
        time_start = nc.variables['Time'][int(minute*2)]
        radar_data.time_start = datetime.utcfromtimestamp(time_start)

        # Time at which radar scan ended
        time_end = nc.variables['Time'][int(minute*2)]           
        radar_data.time_end = datetime.utcfromtimestamp(time_end)

        # Save the data to Pattern object
        self.data = radar_data
        

