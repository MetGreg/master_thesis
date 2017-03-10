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
    ### Interpolate data to grid ###
    ####################################################################
    def data2grid(self,radar):
        
        '''
        Radar data will be interpolated to cartesian grid, by averaging
        all the data, that falls into the same cartesian grid box.
        This is done by the following steps:
        1. For all radar data points (in rotated coordinates), calculate
            the indices of the cartesian grid boxes, in which the data 
            points would fall.
        2. Create 2 numpy arrays (filled with zeros) with exactly the 
            same shape as the cartesian grid. (One entry for each 
            cartesian grid box).
            1st numpy array = refl_matrix 
            2nd numpy array = count_matrix 
        3. Loop through radar data. For each data point, the index of 
            the corresponding cartesian grid box was calculated in 
            step 1. 
            --> add the reflectivity value of the data point to the 
            corresponding entry of the refl_matrix.
            --> add one to the corresponding entry of the count matrix.
        4. To obtain the average reflectivity for each grid box,
            divide the refl_matrix by the count_matrix.
        Only data points in range of pattern radar will be considered.
        This will be tested by calculating the distance of each data 
        point to the pattern radar site (in step 3).
        '''
        
        #calculate lon-indices of cart. grid boxes, for radar data array
        lon_index = np.floor(
                        (radar.data.lon_rota-self.par.lon_start)\
                        /self.par.res_deg
                        )

        #calculate lat-indices of cart. grid boxes, for radar data array
        lat_index = np.floor(
                        (radar.data.lat_rota-self.par.lat_start)\
                        /self.par.res_deg
                        )        
            
        #create array with shape of cartesian grid for refl values
        a_refl      = np.zeros(
                        (self.par.lat_dim,self.par.lon_dim),
                        )

        #create array with shape of cartesian grid to count data points
        a_count     = np.zeros(
                        (self.par.lat_dim,self.par.lon_dim)
                        )        

        #loop through radar data (looping with indices)
        for azi_nr in range(len(radar.data.refl_inc)):                                                                                        
            for range_nr in range(len(radar.data.refl_inc[azi_nr])): 
                
                #get distance between data point and grid center
                distance = self.get_distance(radar,azi_nr,range_nr)
                
                #check, if data point is within pattern radar area
                if distance <= self.par.max_range:
                    
                    #add the refl value to correct entry of refl_array
                    a_refl[int(lat_index[azi_nr][range_nr])]  \
                            [int(lon_index[azi_nr][range_nr])]\
                            += radar.data.refl_inc[azi_nr][range_nr]     
                    
                    #add one to the correct entry of count_array
                    a_count[int(lat_index[azi_nr][range_nr])] \
                            [int(lon_index[azi_nr][range_nr])]\
                            += 1
        
        #to avoid dividing by zero, set all zeros to np.NaNs
        a_count[a_count == 0 ] = np.NaN
        
        #calculate average reflectivities
        refl_avg = a_refl/a_count
        
        #return interpolated reflectivity array
        return refl_avg
    
    


   
    ###################################################################
    ### Distance of data point to center of grid ###
    ###################################################################
    def get_distance(self,radar,azi_nr,range_nr):
        
        '''
        Calculates distance of a data point to the pattern radar site.
        '''
        
        #get lat/lon coordinates of data point
        lon             = radar.data.lon_rota[azi_nr][range_nr]
        lat             = radar.data.lat_rota[azi_nr][range_nr]
        
        #get difference of coordinates in °
        lon_diff         = lon - self.par.site[0]
        lat_diff         = lat - self.par.site[1]
        
        #get difference in m
        lon_diff_m     = lon_diff*60*1852
        lat_diff_m     = lat_diff*60*1852
        
        #get distance in m
        distance         = np.sqrt(lon_diff_m**2 + lat_diff_m**2)
        
        return distance
