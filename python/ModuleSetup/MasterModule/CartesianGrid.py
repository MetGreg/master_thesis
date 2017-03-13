########################################################################
### class for a new defined cartesian grid ###
########################################################################





########################################################################
### modules ###
########################################################################
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sb
from .GridParameter import GridParameter





########################################################################
### CartesianGrid class ###
########################################################################
class CartesianGrid:
    
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
        
        #create gridParameter object, which has defined grid parameters
        grid           = GridParameter()
        




        ################################################################
        ### read in grid definition ###
        ################################################################

        '''
        reads the grid definition, as defined in parameters.py
        '''
        
        lon_start      = grid_par[0][0]     #starting longitude
        lon_end        = grid_par[0][1]     #ending longitude
        lat_start      = grid_par[1][0]     #starting latitude
        lat_end        = grid_par[1][1]     #ending latitude
        site           = grid_par[2]        #rot. coords of pattern site
        max_range      = grid_par[3]        #max. range (m) of pat radar 
        res            = float(grid_par[4]) #grid resolution in m
        




        ################################################################
        ###save grid definition to gridParameter-object ###
        ################################################################

        '''
        saves grid definition to object
        '''
        
        #coords of grid corners
        grid.lon_start = lon_start                                    
        grid.lon_end   = lon_end                                        
        grid.lat_start = lat_start                                    
        grid.lat_end   = lat_end                                        
        
        #rotated coords of pattern site
        grid.site      = site

        #maximum range of pattern radar in m                                       
        grid.max_range = max_range

        #resolution in m                                    
        grid.res_m     = res  

        #resolution in ° 
        #1° = 60 NM = 60*1852 m --> 250m = 1°/(60*1852/250)                                 
        grid.res_deg   = 1/(60*1852/res)                         
        
        #number of rows and lines in cartesian grid-matrix
        grid.lon_dim   = int(np.ceil((lon_end-lon_start)/grid.res_deg))    
        grid.lat_dim   = int(np.ceil((lat_end-lat_start)/grid.res_deg))     
        
        #save grid parameter object to CartesianGrid-object
        self.par       = grid
    




    ####################################################################
    ### Create index-matrix ###
    ####################################################################
    def create_index_matrix(self,radar,index_matrix_file):
        
        '''
        Method to create and save index-matrix. This is an array, that
        has exactly the shape of the cartesian grid. It has an entry
        for each grid box. This entry will be a list, which has an entry
        for each radar data point falling into the corresponding grid
        box. This list entry will then be the location (index) of the 
        data point in the radar data array.        
        '''
        
        #can take a while (depending on resolution)
        print('No Index-Matrix present yet. Calculating the matrix...')

        #calculate lon-indices of cart. grid boxes for radar data array
        lon_index = np.floor(
                        (radar.data.lon_rota - self.par.lon_start)\
                        /self.par.res_deg
                        )

        #calculate lat-indices of cart. grid boxes for radar data array
        lat_index 	= np.floor(
                        (radar.data.lat_rota - self.par.lat_start)\
                        /self.par.res_deg
                        )
        
        #create empty array with shape of cart. grid 
        a_index 	= np.empty(
                        (self.par.lat_dim,self.par.lon_dim),
                        dtype=np.object_
                        )

        #fill empty index array with empty lists
        for line_nr in range(len(a_index)):
            for row_nr in range(len(a_index[line_nr])):
                a_index[line_nr][row_nr] = []

        #loop through all radar data points and save their location	
        for azi_nr in range(len(lon_index)):
            for range_nr in range(len(lon_index[azi_nr])):

                #get distance between data point and grid center
                distance = self.get_distance(radar,azi_nr,range_nr)

                #check, if distance is within max range to be plotted
                if distance <= self.par.max_range:

                    #append loc. of data point to index array entry
                    a_index[int(lat_index[azi_nr][range_nr])]\
                                [int(lon_index[azi_nr][range_nr])]\
                                .append([azi_nr,range_nr]) 	
        
        #save index array to .dat file
        a_index.dump(index_matrix_file)

    


    
    ####################################################################
    ### Interpolation method ###
    ####################################################################
    def data2grid(self,index_matrix_file,radar):

        '''
        Interpolates radar data to new cartesian grid. The reflectivity
        value of an interpolated grid box is the mean reflectivity of 
        all data points falling into this grid box.
        Interpolated value for a grid box is calculating by looping 
        through the index-matrix. The index-matrix has an entry for each
        grid box, containing the indices in the radar data array of the
        data points falling into this grid box. --> Sum reflectivity 
        values of all data points in the grid box and divide it by the
        amount of data points falling into this grid box to obtain
        the averaged (interpolated) reflectivity.
        '''

        #load the index-matrix
        a_index = np.load(index_matrix_file)

        #array with shape of cart. grid for saving interpolated data
        refl = np.empty((self.par.lat_dim,self.par.lon_dim))
	
        #loop through index matrix
        for line_nr in range(self.par.lat_dim):
            for row_nr in range(self.par.lon_dim):
                
                #set reflectivity sum to zero for each grid box
                refl_sum = 0
                
                #loop through all data points of the current grid box
                for data_point in a_index[line_nr][row_nr]:
                    
                    #add the refl. value to the sum variable
                    refl_sum += radar.data.refl_inc\
                                    [data_point[0]][data_point[1]]
                
                #get amount of data pts falling into the grid box
                data_count = len(a_index[line_nr][row_nr])
                
                #avoid division by zero
                if data_count == 0:
                    refl[line_nr][row_nr] = np.NaN
                
                #calculate and save average reflectivity
                else:
                    refl[line_nr][row_nr] = refl_sum / data_count
            
        #return interpolated reflectivity
        return refl

	




    ####################################################################
    ### Distance of data point to pattern site ###
    ####################################################################
    def get_distance(self,radar,azi_nr,range_nr):
        
        '''
        calculates the distance (in meters) between a data point 
        (in rotated coords) and the site coords 
        (also in rotated coords). Input: Index of data point in radar
        data array. 
        '''
        
        #lon/lat coords of data point out of index of radar data array
        lon 			= radar.data.lon_rota[azi_nr][range_nr]
        lat             = radar.data.lat_rota[azi_nr][range_nr]
	   
        #difference in lon/lat between data point and site coords
        lon_diff 		= lon - self.par.site[0]
        lat_diff 		= lat - self.par.site[1]

        #calculate lon/lat difference in meter
        lon_diff_m 	    = lon_diff*60*1852
        lat_diff_m 	    = lat_diff*60*1852

        #get distance
        distance 		= np.sqrt(lon_diff_m**2 + lat_diff_m**2)

        #return distance
        return distance
	
