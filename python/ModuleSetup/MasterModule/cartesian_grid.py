'''Class for cartesian grids covering a defined area'''

# Python modules
import numpy as np
import wradlib

# MasterModule
from .grid_corners import GridCorners
from .grid_coordinates import GridCoordinates


class CartesianGrid(object):
    '''Class for cartesian grids covering a defined area.
    
    This Class creates a cartesian grid with specific resolution and 
    covering a specific area. When creating an object of this class,
    the grid parameters, e.g resolution, area covered and the 
    coordinates of each grid box are saved as attributes. 
    Using this class, it is possible to convert distances in meters to 
    lon/lat differences in degrees and vice versa. Also you can 
    calculate and save the grid indices of the cartesian grid, which 
    are corresponding to an array of rotated pole coordinates. Radar 
    data can be interpolated to this cartesian grid. The distance to a 
    given location as well as the beam height of a radar can be 
    calculated for each grid box. Also, a mask at a specific distance
    around the middle of the grid can be created. Finally, the 
    coordinates of the grid boxes as well as the coordinates of the 
    grid corners can be calculated.
    
    Note:
        This class should only be used for a cartesian grid near the 
        equator, where the skewness of the longitudes is negligible, so
        that angles can be converted to distances without any 
        complicated geometry. Consider using rotated pole coordinates 
        to rotate your grid to the equator.
            
    Attributes:
        lon_site (:any:`float`): Longitude coordinate of grid middle.
        lat_site (:any:`float`): Latitude coordinate of grid middle.
        res_m (:any:`float`): Grid resolution in meters.
        res_deg (:any:`float`): Grid resolution in degree.
        lon_shape (:any:`int`): Number of longitude grid boxes.
        lat_shape (:any:`int`): Number of latitude grid boxes.
        corners (:any:`GridCorners`): Object with coordinates of grid
            corners as attributes.
        coords (:any:`GridCoordinates`): Object with coordinates of grid 
            boxes as attributes.
            
    '''
    
    def __init__(self, grid_par):
        '''Initialization of object
        
        Initializing the object will save the attributes of the 
        cartesian grid to the object. 
        
        Args:
            grid_par (dict): Grid parameters, e.g. location, resolution,
                shape.
                
        '''
        # Save location, resolution and shape
        self.lon_site = grid_par['lon']
        self.lat_site = grid_par['lat']
        self.res_m = grid_par['res']
        self.res_deg = self.meter2deg(grid_par['res'])
        self.lon_shape = grid_par['lon_shape']
        self.lat_shape = grid_par['lat_shape']
         
        # Get and save lon/lat coordinates of grid corners
        self.corners = self.get_grid_corners()
        
        # Get grid boxes coordinates
        self.coords = self.get_coordinates()
       
    def create_index_matrix(self, index_file, lon, lat):
        '''Create index file
        
        Creates and saves the 'index matrix', which is an array with 
        exactly the shape of the cartesian grid. For each grid box, it
        is calculated which of the input array elements fall into this
        grid box. The location of these elements in the input array 
        (in form of indices) is then saved to the index matrix.
        
        Args:
            index_file (str): Name of the output '.dat' file.
            lon (numpy.ndarray): Longitudes of input data.
            lat (numpy.ndarray): Latitudes of input data.
        
        '''
        # This can take a while (depending on resolution and grid size)
        print('No Index-Matrix present yet. Calculating the matrix...')
       
        # Calculate to input coords corresponding indices of grid boxes
        lon_index = np.floor(
            (lon - self.corners.lon_start)/self.res_deg
            )
        lat_index = np.floor(
            (lat - self.corners.lat_start)/self.res_deg
            )
        
        # Create an array with shape of the cart grid (to save locations)
        a_index = np.empty(
            (self.lat_shape, self.lon_shape), dtype=np.object_
            )
       
        # Save indices of input array elements, falling into the boxes  
        for line_nr in range(self.lat_shape):
             for row_nr in range(self.lon_shape):
                
                # Get indices of input array elements, lying in this box
                indices = np.where(np.logical_and(
                    lon_index == row_nr, lat_index == line_nr)
                    )
                
                # Save indices to index matrix
                a_index[line_nr][row_nr] = indices
    
        # Save index matrix to .dat-file
        a_index.dump(index_file)
   
    def data2grid(self, index_file, refl_data):
        '''Interpolate radar data to cartesian grid
        
        Interpolates radar data to the cartesian grid, by averaging all
        data points falling into the same grid box.
        
        Args:
            index_file (str): Name of the index file. For each grid box,
                this file contains the indices in the input data array
                of the data points falling into this grid box. 
            refl_data (numpy.ndarray): Input reflectivity data.
            
        Returns:
            (numpy.ndarray): To cartesian grid interpolated reflectivity
            data.
                
        '''
        # Load index matrix
        a_index = np.load(index_file)

        # Array with shape of cart. grid for saving interpolated data
        refl = np.empty((self.lat_shape, self.lon_shape))

        # Loop through index matrix to interpolate data
        for line_nr in range(self.lat_shape):
            for row_nr in range(self.lon_shape):
                
                # Get values of radar data array
                values = refl_data[a_index[line_nr][row_nr]]
                
                # Save mean reflectivity to refl-array
                refl[line_nr][row_nr] = np.mean(values)

        # Return interpolated reflectivity
        return refl

    def deg2meter(self, degrees):
        '''Convert difference in lon/lat to distance in meters.
        
        This method converts a given coordinate difference of the 
        cartesian grid to the corresponding distance in meters.

        Args:
            degrees (numpy.ndarray): Difference in degrees in lon/lat 
                coordinates, to be converted to a distance in meters.
        
        Returns:
            (numpy.ndarray): To the difference in lon/lat coordinates 
            corresponding distance in meters.
            
        '''
        # Calculate distance
        distance = degrees*60*1852
        
        # Return distance
        return distance
   
    def get_beam_height(self, lon_site, lat_site, elevation):
        '''Calculate height of a radar beam 
        
        Calculates for each grid box the beam height above the ground 
        for a radar at a given location. 

        Args:
            lon_site (float): Longitude coordinate of the radar site.
            lat_site (float): latitude coordinate of the radar site.
            elevation (float): Elevation of the radar beam.
        
        Returns:
            (numpy.ndarray): Heights of radar beam above ground in 
            meters.
                
        '''
        # Get distance of grid box to radar site 
        a_dist = self.get_distance(lon_site, lat_site)
        
        # Get height of radar beam at each grid box
        beam_heights = wradlib.georef.beam_height_n(a_dist, elevation)
        
        # Return the beam heights array
        return beam_heights

    def get_coordinates(self):
        '''Get array of coordinates for all grid boxes
        
        This method calculates for each grid box the longitude/latitude
        coordinates.
        
        Returns:
            (GridCoordinates): Object, where grid coordinates are
            saved as attributes.
                
        '''
        # Create grid_coords object
        grid_coords = GridCoordinates()
        
        # Get longitude and latitude coordinates
        grid_coords.lon = np.linspace(
            self.corners.lon_start, self.corners.lon_end, self.lon_shape
            )
        grid_coords.lat = np.linspace(
            self.corners.lat_start, self.corners.lat_end, self.lat_shape
            )
        
        # Return coordinates as numpy meshgrid
        return grid_coords
    
    def get_distance(self, lon_site, lat_site):
        '''Get distance of each grid box to input location 
        
        Calculates the distance (in meters) between each grid box of the 
        cartesian grid and the input location.
            
        Args:
            lon_site (float): Longitude coordinate of location, to which
                the distance will be calculated.
            lat_site (float): latitude coordinate of location, to which
                the distance will be calculated.
                 
        Returns:
            (numpy.ndarray): Distance of each grid box to the input 
            location.

        '''
        # Get numpy meshgrid
        lon, lat = np.meshgrid(self.coords.lon, self.coords.lat)
        
        # Get difference in degrees for lon and lat direction
        lon_dist = lon - lon_site
        lat_dist = lat - lat_site
        
        # Convert difference in degrees to distance in m
        lon_dist_m = self.deg2meter(lon_dist)
        lat_dist_m = self.deg2meter(lat_dist)

        # Calculate distance to radar site using pythagoras
        a_dist = np.sqrt(lon_dist_m**2 + lat_dist_m**2)
       
        # Return distance array
        return a_dist

    def get_grid_corners(self):
        '''Calculate coordinates of grid corners
        
        This method calculates the coordinates of the corners of the
        cartesian grid.
        
        Returns:
            (GridCorners): Object, which saves coordinates of 
            grid corners as attributes.
        
        ''' 
        #create grid_corners object
        grid_corners = GridCorners()
        
        # Get lon and lat range of the grid area
        lon_range = self.meter2deg(self.res_m*self.lon_shape)
        lat_range = self.meter2deg(self.res_m*self.lat_shape)
        
        # Calculate starting end ending lon/lat
        grid_corners.lon_start = self.lon_site - lon_range/2
        grid_corners.lon_end = self.lon_site + lon_range/2
        grid_corners.lat_start = self.lat_site - lat_range/2
        grid_corners.lat_end = self.lat_site + lat_range/2
        
        # Return grid corners
        return grid_corners
   
    def get_mask(self, max_range):
        '''Mask grid area where distance exceeds maximum range
        
        Creates a mask array with the same shape as the cartesian grid,
        for all grid boxes exceeding a specific (input) range to the 
        middle of the grid.
        
        Args:
            max_range (float): Maximum range, all grid boxes exceeding
                this range will be masked.
        
        Returns:
            (numpy.ndarray): Boolean array with the same shape as 
            the cartesian grid, where "True" means masked, and 
            "False" means not masked.
                 
        '''
        # Create empty array with shape of cartesian grid. 
        a_mask = np.empty(
            (self.lat_shape, self.lon_shape), dtype = bool
            )

        # Calculate the distance of grid boxes to middle of grid
        dist = self.get_distance(self.lon_site, self.lat_site)
        
        # Create mask array
        a_mask[dist <= max_range] = False
        a_mask[dist > max_range] = True

        # Return mask array
        return a_mask

    def meter2deg(self, distance):
        '''Convert distance to difference in lon/lat coordinates
        
        This method converts a given distance in meters to the 
        corresponding difference in lon/lat coordinates of the 
        cartesian grid.
        
        Args:
            distance (numpy.ndarray): Distance in meters to be 
                converted to lon/lat differences.
        
        Returns:
            (numpy.ndarray): To the distance corresponding difference in
            lon/lat coordinates in degrees.
            
        '''
        # Calculate to distance corresponding angle
        degrees = 1/(60*1852/distance)
        
        # Return angle
        return degrees
    
