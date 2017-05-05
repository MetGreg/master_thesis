''' This module contains the Radar, the CartesianCoordinates and the 
MiddleCoordinates class.
Radar: For calculations with radar data of Pattern or DWD.
CartesianCoordinates: Saves cartesian coordinates of radar data.
MiddleCoordinates: Saves polar coordinates of middle of grid boxes.

'''
# Python modules
import wradlib
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt 
import numpy as np


class Radar(object):
    '''Class for general radar data
    
    This class creates a Radar object, which can be used for pattern
    netcdf - data as well as hdf5-data from the 'Deutscher Wetterdienst'
    (DWD). Using this class, it is possible to artificially increase
    the azimuth resolution of the data. You can calculate azimuth-
    and range coordinate arrays. Further, you can calculate the polar
    coordinates of the middle of each polar grid box of the radar data, 
    as well as transforming polar coordinates to longitude/latitude
    cartesian coordinates. Finally, using this class, you can simply
    plot the original reflectivity data.
    
    Note:
        Most of the methods only work, if the radar data was succesfully 
        read in already, using the read_file method of the DwdRadar
        or PatternRadar subclass. 
    
    Attributes:
        res_fac (int): Factor, by which the azimuth angle will be 
            increased artificially.
        
    '''
     
    def __init__(self, radar_par):
        '''Initialization
        
        Saves attributes to object.
        
        Args:
            radar_par (dict): Radar parameters, e.g. name of file, 
                minute to be plotted, processing step, factor to 
                increase azimuth resolution, offset of radars azimuth 
                angle.
        
        '''
        self.res_fac = radar_par['res_fac']
        
    def increase_azi_res(self):
        '''Increase azimuth resolution of radar data array
        
        Increases azimuth resolution of radar dataset artificially by a 
        specific factor.
        
        Returns: 
            (numpy.ndarray): Data array of increased azimuth resolution.
            
        '''          
        # Will be filled with reflectivity values of incr. resolution
        data_inc = []
          
        # Append each line (azimuth) 'res_factor'-times to new array      
        for line in self.data.refl:
            for i in range(self.res_fac):     
                data_inc.append(line)
          
        # Transform to numpy array
        data_inc = np.array(data_inc)
        
        # Return data array of increase resolution
        return data_inc
    
    def get_azi_coords(self):
        '''Calculate azimuth coordinate array
        
        Calculates a coordinate array containing the azimuth 
        coordinates of all radar data points.
        
        Returns:
            (numpy.ndarray): azimuth coordinates of corresponding radar 
                data array.
        
        '''
        # Define shorter names for attributes
        start = self.data.azi_start
        steps = self.data.azi_steps
        ray_nr = self.data.azi_rays
        res_fac = self.res_fac
        
        # Azimuth coordinates of data points
        azi_coords = np.arange(
            start, steps*ray_nr + start, steps/res_fac
            )

        # Take care of transition from 360 to 0
        azi_coords = (azi_coords + 360) % 360
        
        # Return array of azimuth coordinates
        return azi_coords
    
    def get_middle_pixel(self):           
        '''Get coordinates of the center of the grid boxes
     
        Calculates polar coordinates of the middle of each 
        polar grid box of the radar data array. 
        This is done by averaging azimuth angles and range values of 
        two adjacent data points respectively, for all data points.
        
        Returns:
            (MiddleCoordinates object): Object, which saves the 
                polar coordinates of middle pixels as attributes.
                
        '''
        # Create MiddleCoordinates object
        mid_coords = MiddleCoordinates()
        
        # Get azimuth and range coordinates of radar data
        azi_coords = self.get_azi_coords()
        range_coords = self.get_range_coords()
        
        # Get array of azimuth coordinates of middle pixels
        mid_coords.azi = (
            (azi_coords + self.data.azi_steps/(2*self.res_fac)) % 360
            )
            
        # Get array of range coords of middle pixels
        mid_coords.range_ = range_coords - self.data.r_steps/2
        
        # Return coordinates of middle pixels
        return mid_coords
    
    def get_range_coords(self):
        '''Calculate range coordinate array
        
        Calculates a coordinate array containing the range coordinates 
        of all radar data points.
        
        Returns:
            (numpy.ndarray): Range coordinates of corresponding radar 
                data array.
                
        '''
        # Define shorter names for attributes
        start = self.data.r_start
        steps = self.data.r_steps
        bin_nr = self.data.r_bins
        
        # Calculate range coordinates of data points
        range_coords = np.arange(start, steps*bin_nr + start, steps)
        
        # Return array of range coordinates
        return range_coords
   
    def plot(self):
        '''Create plot of radar reflectivity
        
        This method creates a simple plot of original radar reflectivity
        using wradlib. See wradlib.org for more information.

        '''
        # Reflectivity array
        dbz = self.data.refl
        dbz_inc = self.increase_azi_res()
        
        # Get time
        time_start = self.data.time_start
        time_end = self.data.time_end
        
        # Get coordinates of data (transform range to km)
        range_coords = self.get_range_coords()/1000
        azi_coords = self.get_azi_coords()
        
        # Put a mask on the reflectivity array
        mask_ind = np.where(dbz_inc <= np.nanmin(dbz_inc))
        dbz_inc[mask_ind] = np.nan
        ma = np.ma.array(dbz_inc, mask=np.isnan(dbz_inc))
        
        # Create colormap for plot (continously changing colormap)                                                                    
        cmap = mcolors.LinearSegmentedColormap.from_list(
           'my colormap', ['white', 'blue', 'red', 'magenta']
           )   
        
        # Create plot and grid
        cgax, caax, paax, pm = wradlib.vis.plot_cg_ppi(
            ma, range_coords, azi_coords, cmap=cmap, refrac=False,
            vmin=-32.5, vmax=70
            )
        
        # Create colorbar and increase tick labelsize
        cbar = plt.colorbar(pm)
        cbar.ax.tick_params(labelsize=18)
        
        # Set labels
        caax.set_xlabel('x_range [km]', fontsize=18)
        caax.set_ylabel('y_range [km]', fontsize=18)
        cbar.set_label('reflectivity [dbz]', fontsize=18)
        plt.text(1.0, 1.05, 'azimuth', transform=caax.transAxes,
           va='bottom', ha='right', fontsize=18
           )
        
        # Set tick-label size
        caax.tick_params(labelsize=16)
        cgax.axis['top'].major_ticklabels.set_fontsize(16)
        cgax.axis['right'].major_ticklabels.set_fontsize(16)
        
        # Create  title
        plt.title(
            self.name
            + ': '
            + str(time_start.time())
            + ' - '
            + str(time_end.time())
            + ' UTC \n'
            + str(time_start.date()),
            y=1.05, fontsize=22
            )
        
        # Show plot
        plt.show()
 
    def polar_to_cartesian(self, r, az):
        '''Transform polar to cartesian coordinates
        
        Uses a wradlib function to calculate lon/lat cartesian 
        coordinates out of polar coordinates. 

        Args:
            r (numpy.ndarray): Range coordinates.
            az (numpy.ndarray): Azimuth angles with values between 0° 
                and 360°, assumed to start with 0° pointing north and 
                counted positiv clockwise. 
       
        Returns:
            (CartesianCoordinates object): Object, which saves cartesian 
                coordinates of radar data as attributes.
                
        '''
        # Create CartesianCoordinates object
        cart_coords = CartesianCoordinates()
        
        # Transform polar coordinates to lon/lat cart. coordinates
        cart_coords.lon, cart_coords.lat = wradlib.georef.polar2lonlat(
            r, az, (self.data.lon_site, self.data.lat_site)
            ) 
        
        # Return cartesian coordinates
        return cart_coords
        
    def read_file(self):
        '''Reading data file
        
        This method is specified in the subclasses, since reading files
        differs from radar to radar.
        
        Raises:
            NotImplementedError: If this method is called.
        
        '''
        raise NotImplementedError
        
        
class CartesianCoordinates(Radar):
    '''Saves cartesian coordinates of radar data'''
    
    def __init__(self):
        '''Initialization of object
        
        Does nothing so far.
        
        '''
        pass
    
    @property
    def lon(self):
        '''Longitude coordinates
        
        Longitude coordinates of radar data. Must be numpy.ndarray.
        
        '''
        try:
            return self._lon
        except AttributeError:
            return 0
    
    @lon.setter
    def lon(self, new_lon):
        assert(
            isinstance(new_lon, np.ndarray)
            ), 'new_lon not a numpy.ndarray'
        self._lon = new_lon
    
    @property
    def lat(self):
        '''Latitude coordinates
        
        Latitude coordinates of radar data. Must be numpy.ndarray.
        
        '''
        try:
            return self._lat
        except AttributeError:
            return 0
    
    @lat.setter
    def lat(self, new_lat):
        assert(
            isinstance(new_lat, np.ndarray)
            ), 'new_lat not a numpy.ndarray'
        self._lat = new_lat


class MiddleCoordinates(Radar):
    '''Saves coordinates of grid box middle pixels'''
    
    def __init__(self):
        '''Initialization of object
        
        Does nothing so far.
        
        '''
        pass
       
    @property
    def azi(self):
        '''Azimuth coordinates
        
        Azimuth coordinates of grid box mids. Must be numpy.ndarray.
        
        '''
        try:
            return self._azi
        except AttributeError:
            return 0
    
    @azi.setter
    def azi(self, new_azi):
        assert(
            isinstance(new_azi, np.ndarray)
            ), 'new_azi not a numpy.ndarray'
        self._azi = new_azi
    
    @property
    def range_(self):
        '''Range coordinates
        
        Range coordinates of grid box mids. Must be numpy.ndarray.
        
        '''
        try:
            return self._range_
        except AttributeError:
            return 0
    
    @range_.setter
    def range_(self, new_range_):
        assert(
            isinstance(new_range_, np.ndarray)
            ), 'new_range_ not a numpy.ndarray'
        self._range_ = new_range_
    
