###CartesianGrid class

'''
This file is reserved for the CartesianGrid class.
'''





########################################################################
### modules ###
########################################################################

'''
Import all modules needed for this class.
'''

#python modules
import numpy as np
import wradlib





########################################################################
### CartesianGrid class ###
########################################################################
class CartesianGrid(object):
    
    '''
    Object for a new defined cartesian grid. Data from different radars
    can be interpolated to this grid. --> Different radars comparable.
    '''
    
    
    
    
    
    ####################################################################
    ### Initialization method ###
    ####################################################################
    def __init__(self,grid_par):
        
        '''
        Saves the grid paramaters to a GridParameter-object.
        '''
        




        ################################################################
        ### read in grid definition ###
        ################################################################

        '''
        Reads the grid definition, as defined in parameters.py
        '''
        
        pat_site   = grid_par[0]        #rot. coords of pattern site
        max_range  = grid_par[2]        #max. range (m) of pat radar 
        res        = float(grid_par[3]) #grid resolution in m
        grid_shape = grid_par[1]        #shape of the grid

        #get starting and ending coords of cartesian grid in rot coords
        lon_start = pat_site[0] - 1/(60*1852/(res*grid_shape[0]/2))
        lon_end   = pat_site[0] + 1/(60*1852/(res*grid_shape[0]/2))                                      
        lat_start = pat_site[1] - 1/(60*1852/(res*grid_shape[1]/2))                                    
        lat_end   = pat_site[1] + 1/(60*1852/(res*grid_shape[1]/2))                                        
        




        ################################################################
        ### save grid definition to object ###
        ################################################################

        '''
        Saves grid definition to object.
        '''
        
        #coords of grid corners
        self.lon_start  = lon_start                                    
        self.lon_end    = lon_end                                      
        self.lat_start  = lat_start                                    
        self.lat_end    = lat_end                                        
        
        #rotated coords of pattern site
        self.pat_site   = pat_site

        #maximum range of pattern radar in m                                       
        self.max_range  = max_range

        #resolution in m                                    
        self.res_m      = res  

        #resolution in ° 
        #1° = 60 NM = 60*1852 m --> 250m = 1°/(60*1852/250)                                 
        self.res_deg    = 1/(60*1852/res)                         
        
        #number of rows and lines in cartesian grid-matrix
        self.lon_dim    = grid_shape[0]    
        self.lat_dim    = grid_shape[1]     
        
        #get coordinates of grid boxes in rotated coords
        lon = np.linspace(self.lon_start, self.lon_end, self.lon_dim)
        lat = np.linspace(self.lat_start, self.lat_end, self.lat_dim)

        #save coords to object
        self.rot_coords = np.array((lon,lat))




    
    ####################################################################
    ### Create index-matrix ###
    ####################################################################
    def create_index_matrix(self,index_matrix_file,coords_rot):
        
        '''
        Method to create and save index-matrix. This is an array, that
        has exactly the shape of the cartesian grid. It has an entry
        for each grid box. This entry will be an array, containing (for 
        each data point falling into this grid box) the location (in 
        form of an index) of the data point in the radar data array. 
        
        Input: Name of the matrix-file, array of rotated coordinates of 
        data. 

        Output: None  
        '''
        
        #can take a while (depending on resolution)
        print('No Index-Matrix present yet. Calculating the matrix...')

        #get rotated lon and lat
        lon_rot = coords_rot[:,:,0]
        lat_rot = coords_rot[:,:,1]

        #calculate lon-indices of cart. grid boxes for radar data array
        lon_index = np.floor((lon_rot - self.lon_start)/self.res_deg)

        #calculate lat-indices of cart. grid boxes for radar data array
        lat_index = np.floor((lat_rot - self.lat_start)/self.res_deg)
        
        #create empty array with shape of cart. grid 
        a_index   = np.empty(
                        (self.lat_dim,self.lon_dim),
                        dtype = np.object_
                        )
       
        #loop through all radar data points and save their location    
        for line_nr in range(self.lat_dim):
             for row_nr in range(self.lon_dim):
                
                #find indices of data array, where data lies
                indices = np.where(np.logical_and(
                    lon_index == row_nr,lat_index == line_nr)
                    )
                
                #append loc. of data point to index array entry
                a_index[line_nr][row_nr] = indices
    
        #save indices to .dat-file
        a_index.dump(index_matrix_file)
            
        



    ####################################################################
    ### Interpolation method ###
    ####################################################################
    def data2grid(self,index_matrix_file,coords_rot,refl_data):

        '''
        Interpolates radar data to new cartesian grid. The reflectivity
        value of an interpolated grid box is the mean reflectivity of 
        all data points falling into this grid box.
        The index-matrix has an entry for each grid box, containing the 
        indices (in the radar data array) of the data points falling 
        into this grid box. --> Calculate mean of these data points and
        save it to the corresponding refl-array entry.

        Input: Name of matrix-file, array of rotated coordinates of
        data, array of radar data.

        Output: Array with shape of CartesianGrid, containing the 
        interpolated radar data.
        '''

        #get rotated lon and lat
        lon_rot = coords_rot[:,:,0]
        lat_rot = coords_rot[:,:,1]

        #load index matrix
        a_index = np.load(index_matrix_file)

        #array with shape of cart. grid for saving interpolated data
        refl = np.empty((self.lat_dim,self.lon_dim))
        
        #calculate lon-indices of cart. grid boxes for radar data array
        lon_index = np.floor((lon_rot - self.lon_start)/self.res_deg)

        #calculate lat-indices of cart. grid boxes for radar data array
        lat_index = np.floor((lat_rot - self.lat_start)/self.res_deg)

        #loop through index matrix
        for line_nr in range(self.lat_dim):
            for row_nr in range(self.lon_dim):
                
                #get values of radar data array
                values = refl_data[a_index[line_nr][row_nr]]
                
                #save mean reflectivity to refl-array
                refl[line_nr][row_nr] = np.mean(values)

        #return interpolated reflectivity
        return refl





    ####################################################################
    ### Distance of grid boxes to input location ###
    ####################################################################
    def get_distance(self,site):

        '''
        Calculates the distance (in meters) between a grid box of the 
        cartesian grid and the input location (usually a radar site, but
        other locations are also possible.). 
        1. step: Calculate for lon- and lat-direction respectively the
            difference in rotated coords between grid box and location.
        2. step: Transform difference in rotated coordinates to meters.
        3. step: Use pythagoras to calculate the distance between grid
            box and site.
        
        Input: Rotated coords of radar site.

        Output: Array with shape of CartesianGrid, containing the 
        distances of each grid box to the radar site.

        '''

        #coords of site in lon/lat
        lon_site = site[0]
        lat_site = site[1]
        
        #get distance in m for lon and lat-direction
        lon_dist = (self.rot_coords[0] - lon_site)*60*1852
        lat_dist = (self.rot_coords[1] - lat_site)*60*1852

        #create meshgrid to have all possible combinations
        lon_dist,lat_dist = np.meshgrid(lon_dist,lat_dist)
        
        #calculate distance to radar site for each grid box
        a_dist = np.sqrt((lon_dist)**2+ (lat_dist)**2)
       
        #return distance array
        return a_dist





    ####################################################################
    ### Mask around pattern area ###
    ####################################################################
    def get_mask(self):
        
        '''
        Gets a mask of the same shape as the cartesian grid. All grid
        boxes, which are not in the pattern area will be masked.
        The distance between each grid box to the pattern site is
        calculated. A grid box is considered out of range
        (and thus masked), if the distance between its mid to the 
        pattern site is larger than the pattern range.

        Input: None

        Output: Boolean array with shape of CartesianGrid. All
        entries, that shall be masked, are True, all other entries are
        False.
        '''

        #create empty array with shape of cart grid for the mask
        a_mask = np.empty((self.lat_dim,self.lon_dim),dtype = bool)

        #get distance of grid boxes to pattern site
        dist = self.get_distance(self.pat_site)
        
        #get mask array
        a_mask[dist <= self.max_range] = False
        a_mask[dist > self.max_range]  = True

        #return mask
        return a_mask





    ####################################################################
    ### beam height ###
    ####################################################################
    def get_beam_height(self,site_coords,elevation):

        '''
        Calculates for each grid box the beam height above the ground 
        of a given radar.

        Input: Rotated coordinates of radar site, elevation of radar 
        beam.

        Output: Array with shape of CartesianGrid containing for each
        grid box the height of the middle of the radar beam in m.
        '''
        
        #get distance of grid box to radar site 
        a_dist = self.get_distance(site_coords)
        
        #get height of radar beam at each grid box
        beam_heights = wradlib.georef.beam_height_n(a_dist,elevation)
    


        return beam_heights





   
