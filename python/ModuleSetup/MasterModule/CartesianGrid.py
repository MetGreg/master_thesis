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
from skimage import measure
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
        for each grid box. This entry will be an array, containing (for 
        each data point falling into this grid box) the location (in 
        form of an index )of the data point in the radar data array.  
        '''
        
        #can take a while (depending on resolution)
        print('No Index-Matrix present yet. Calculating the matrix...')

        #calculate lon-indices of cart. grid boxes for radar data array
        lon_index = np.floor(
                        (radar.data.lon_rota - self.par.lon_start)\
                        /self.par.res_deg
                        )

        #calculate lat-indices of cart. grid boxes for radar data array
        lat_index = np.floor(
                        (radar.data.lat_rota - self.par.lat_start)\
                        /self.par.res_deg
                        )
        
        #create empty array with shape of cart. grid 
        a_index   = np.empty(
                        (self.par.lat_dim,self.par.lon_dim),
                        dtype = np.object_
                        )

       
        #loop through all radar data points and save their location    
        for line_nr in range(self.par.lat_dim):
             for row_nr in range(self.par.lon_dim):
                
                #find indices of data array, where data lies
                indices = np.where(np.logical_and(lon_index == row_nr,lat_index == line_nr))
                
                #append loc. of data point to index array entry
                a_index[line_nr][row_nr] = indices
    
        a_index.dump(index_matrix_file)
            
        



    ####################################################################
    ### Interpolation method ###
    ####################################################################
    def data2grid(self,index_matrix_file,radar):

        '''
        Interpolates radar data to new cartesian grid. The reflectivity
        value of an interpolated grid box is the mean reflectivity of 
        all data points falling into this grid box.
        The index-matrix has an entry for each grid box, containing the 
        indices (in the radar data array) of the data points falling 
        into this grid box. --> Calculate mean of these data points and
        save it to the corresponding refl-array entry.
        '''

        a_index = np.load(index_matrix_file)

        #array with shape of cart. grid for saving interpolated data
        refl = np.empty((self.par.lat_dim,self.par.lon_dim))
        
        #calculate lon-indices of cart. grid boxes for radar data array
        lon_index = np.floor(
                        (radar.data.lon_rota - self.par.lon_start)\
                        /self.par.res_deg
                        )

        #calculate lat-indices of cart. grid boxes for radar data array
        lat_index = np.floor(
                        (radar.data.lat_rota - self.par.lat_start)\
                        /self.par.res_deg
                        )

        #loop through index matrix
        for line_nr in range(self.par.lat_dim):
            for row_nr in range(self.par.lon_dim):
                
                #get values of radar data array
                values = radar.data.refl_inc[a_index[line_nr][row_nr]]
                
                #save mean reflectivity to refl-array
                refl[line_nr][row_nr] = np.mean(values)

        #return interpolated reflectivity
        return refl

    




    ####################################################################
    ### Mask around pattern area ###
    ####################################################################
    def get_mask(self):
        
        '''
        Gets a mask of the same shape as the cartesian grid. All grid
        boxes, which are not in the pattern area will be masked.
        The distance between each grid box to the pattern grid box is
        calculated. The pattern grid box is the grid box in which the
        pattern radar is located. A grid box is considered out of range
        (and thus masked), if the distance between its mid to the mid
        of the pattern grid box is larger than the pattern range.
        '''

        #create empty array with shape of cart grid for the mask
        a_mask = np.empty(
                    (self.par.lat_dim,self.par.lon_dim),
                    )

        #coordinates of radar site in rotated pole coordinates
        lon_site  = self.par.site[0]
        lat_site  = self.par.site[1]

        #get lon-index of grid box in which the radar site is located
        site_lon_index = np.floor(
            (lon_site - self.par.lon_start) / self.par.res_deg
            )

        #get lat index of grid box in which the radar site is located
        site_lat_index = np.floor(
            (lat_site - self.par.lat_start) / self.par.res_deg
            )
        
        #create numpy array of lon at lat indices of grid boxes
        lon_index = np.arange(self.par.lon_dim)
        lat_index = np.arange(self.par.lat_dim)

        #create meshgrid out of grid box indices
        x_index, y_index = np.meshgrid(lon_index,lat_index)

        #calculate distance to radar site for each grid box
        dist = np.sqrt(
              ((site_lon_index-x_index) * self.par.res_m)**2\
            + ((site_lat_index-y_index) * self.par.res_m)**2
            )
        
        #get mask array
        a_mask[dist <= self.par.max_range] = False
        a_mask[dist > self.par.max_range]  = True
        
        #return mask
        return a_mask





    ####################################################################
    ### Distance of data point to pattern site ###
    ####################################################################
    def dist_polar2radar(self,radar,lon,lat):
        
        '''
        calculates the distance (in meters) between a data point 
        (in rotated pole coords) and the site coords 
        (also in rotated pole coords). Input: lon/lat of data point in 
        rotated pole coordinates.
        '''
        
        #difference in lon/lat between data point and site coords
        lon_diff         = lon - self.par.site[0]
        lat_diff         = lat - self.par.site[1]

        #calculate lon/lat difference in meter
        lon_diff_m       = lon_diff*60*1852
        lat_diff_m       = lat_diff*60*1852

        #get distance
        distance         = np.sqrt(lon_diff_m**2 + lat_diff_m**2)

        #return distance
        return distance
    
    
    
    
    
    ####################################################################
    ### Distance of grid boxes to radar site ###
    ####################################################################
    def dist_grid2radar(self,radar):

        '''
        Calculates the distance (in meters) between a grid box of the 
        cartesian grid and the radar site. 
        First, calculates rotated coords of radar site. This can be 
        transformed to an index of the cartesian grid. -->
        Index of grid box, in which radar site lies is known.
        --> Get distance of each grid box to radar site, by multiplying
        differences in x- and y- indices with the length of a grid box
        and using pythagoras.        
        '''
        
        #create empty array with shape of cart grid for saving distances
        a_dist = np.empty(
                        (self.par.lat_dim,self.par.lon_dim),
                        )

        #coordinates of radar site in polar coordinates
        lon_site  = radar.data.lon_site
        lat_site  = radar.data.lat_site
        
        #calculate rotated coords of radar site
        coords_rot = radar.rotate_pole(
            np.array(lon_site),np.array(lat_site)
            ) 

        #get lon-index of grid box in which the radar site is located
        lon_index = np.floor(
                        (coords_rot[0][0] - self.par.lon_start)\
                        /self.par.res_deg
                        )

        #get lat index of grid box in which the radar site is located
        lat_index = np.floor(
                        (coords_rot[0][1] - self.par.lat_start)\
                        /self.par.res_deg
                        )

        #loop through cartesian grid, calc distance for each grid box
        for line_nr in range(self.par.lat_dim):
            for row_nr in range(self.par.lon_dim):
                
                #calc dist in y- and x-axis between site and grid box
                lon_dist = (lon_index - line_nr)*self.par.res_m
                lat_dist = (lat_index - row_nr)*self.par.res_m

                #calc dist between site and grid box using pythagoras
                a_dist[line_nr][row_nr] = np.sqrt(
                    lon_dist**2 + lat_dist**2
                    )
       
        #return distance array
        return a_dist





    ####################################################################
    ### plot radar data on cartesian grid ###
    ####################################################################
    def plot_data(self,tick_nr,radar,refl):
        
        '''
        Plots radar data on a cartesian grid.
        '''





        ################################################################
        ### prepare plot ###
        ################################################################
        
        '''
        prepares plot by defining labling lists, ticks, cmaps etc 
        '''
        
        #getting rot. lon-coords of grid lines to be labeled
        lon_plot = np.around(
                    np.linspace(
                        self.par.lon_start,
                        self.par.lon_end,
                        num = tick_nr
                               ),decimals = 2
                            )
                             
        #getting rot. lat-coords of grid lines to be labeled                        
        lat_plot = np.around(
                    np.linspace(
                        self.par.lat_start,
                        self.par.lat_end,
                        num = tick_nr
                               ),decimals = 2
                            )
        
        #maximum number of grid lines (lon_dim = lat_dim)
        ticks    = self.par.lon_dim
        
        #create colormap for plot (continously changing colormap)                                                                    
        cmap     = mcolors.LinearSegmentedColormap.from_list(
                   'my colormap',['white','blue','red','magenta']
                   )    
        
        
        
        
        
        ################################################################
        ### plot data ###
        ################################################################
        
        '''
        Plots interpolated radar data on the new cartesian grid using 
        seaborn.
        '''
        
        #create heatmap  
        mask = self.get_mask()         
        
        #create seaborn plot
        ax =  sb.heatmap(
            refl, mask = mask,vmin = 5, vmax = 70, cmap = cmap
            )                  
        
        #x- and y-tick positions
        ax.set_xticks(np.linspace(0,ticks,num=tick_nr), minor = False)                
        ax.set_yticks(np.linspace(0,ticks,num=tick_nr), minor = False)                
        
        #x- and y-tick labels
        ax.set_xticklabels(lon_plot,fontsize = 16)                                        
        ax.set_yticklabels(lat_plot,fontsize = 16,rotation='horizontal')                                        
        
        #label colorbar
        ax.collections[0].colorbar.set_label('reflectivity [dbz]',
            fontsize=18
            )
            
        #change tick size of colorbar
        ax.collections[0].colorbar.ax.tick_params(labelsize = 18)
       
        #grid
        ax.xaxis.grid(True, which='major', color = 'k')                                
        ax.yaxis.grid(True, which='major', color = 'k')
        
        #put grid in front of data                        
        ax.set_axisbelow(False)  
        
        #label x- and y-axis                                                  
        plt.xlabel('r_lon', fontsize = 18)                                    
        plt.ylabel('r_lat', fontsize = 18)    
        
        #title 
        plt.title(                                   \
                  str(radar.name)                    \
                  +'-data: '                         \
                  + str(radar.data.time_start.time())\
                  + ' - '                            \
                  + str(radar.data.time_end.time())  \
                  +'\n'                              \
                  + str(radar.data.time_end.date()),
                  fontsize = 20
                 )   
        
        #show  
        plt.show()                                                                
        
                
        
    

    ####################################################################
    ### plot differences between radars ###
    ####################################################################
    def plot_diff(self,tick_nr,l_refl,log_iso,rain_th,radar1,radar2):
        
        '''
        plots the differences between two radars on the cartesian grid.
        '''
        
        
        
        
        
        ################################################################
        ### prepare plot ###
        ################################################################
        
        '''
        prepares plot by defining labling lists etc. 
        '''
        
        #get differences of two radar data arrays
        refl_diff = l_refl[1] - l_refl[0]

        #getting rot. lon-coords of grid lines to be labeled
        lon_plot = np.around(
                    np.linspace(
                        self.par.lon_start,
                        self.par.lon_end,
                        num = tick_nr
                               ),decimals = 2
                            )
                             
        #getting rot. lat-coords of grid lines to be labeled                        
        lat_plot = np.around(
                    np.linspace(
                        self.par.lat_start,
                        self.par.lat_end,
                        num = tick_nr
                               ),decimals = 2
                            )
        
        #maximum number of grid lines (lon_dim = lat_dim)
        ticks = self.par.lon_dim
        
        
        
        
        
        ################################################################
        ### actual plot ###
        ################################################################
                
        '''
        Plots difference matrix on the new cartesian grid using seaborn.
        '''
        
        #create subplot
        fig,ax = plt.subplots() 
        
        #create heatmap                                                                                                              
        sb.heatmap(refl_diff,vmin = -70, vmax = 70,cmap = 'bwr')                  
        
        #x- and y-tick positions
        ax.set_xticks(np.linspace(0,ticks,num=tick_nr), minor = False)                
        ax.set_yticks(np.linspace(0,ticks,num=tick_nr), minor = False)                
        
        #x- and y-tick labels
        ax.set_xticklabels(lon_plot,fontsize = 16)                                        
        ax.set_yticklabels(lat_plot,fontsize = 16,rotation='horizontal')                                        
        
        #grid
        ax.xaxis.grid(True, which='major',color = 'k')                                
        ax.yaxis.grid(True, which='major',color = 'k')
        
        #put grid in front of data                        
        ax.set_axisbelow(False)  
        
        #label x- and y-axis                                                  
        plt.xlabel('r_lon', fontsize = 18)                                    
        plt.ylabel('r_lat', fontsize = 18)    
        
        #plot isolines, if wished
        if log_iso == True:
            
            #contours around rain-areas
            contour1 = measure.find_contours(l_refl[0][::-1], rain_th)
            contour2 = measure.find_contours(l_refl[1][::-1], rain_th)
        
            #plot contours of radar1
            for n, contour in enumerate(contour1):
                ax.plot(contour[:,1], contour[:,0], linewidth=1, 
                    color = 'b', label = 'dwd'
                    )
            
            #plot contours of radar2
            for n, contour in enumerate(contour2):
                ax.plot(contour[:,1],contour[:,0], linewidth=1, 
                    color='r',label = 'pattern'
                    )
            
            #remove all labels except one of each radar
            lines = ax.get_lines()
            for line in lines[1:-1]:
                line.set_label('')
        
            #legend
            plt.legend(fontsize = 16)
        
        #title                           
        plt.title(
                  radar2.name +                                     \
                  '(' + str(radar2.data.time_start.time()) + ' - '  \
                  + str(radar2.data.time_end.time()) + ')'          \
                  + ' minus ' + radar1.name                         \
                  + '(' + str(radar1.data.time_start.time()) + ' - '\
                  + str(radar1.data.time_end.time()) + ')\n'        \
                  +str(radar1.data.time_end.date()),
                  fontsize = 20
                  )
        
        #show  
        plt.show()                                                                
        
        
        
        

    ####################################################################
    ### plot heights ###
    ####################################################################
    def plot_heights(self,heights,isolines,tick_nr,radar):

        '''
        Plots heights of radar beam as isolines
        '''
    




        ################################################################
        ### prepare plot ###
        ################################################################
        
        '''
        prepares plot by defining labling lists etc. 
        '''
        
        
        #getting rot. lon-coords of grid lines to be labeled
        lon_plot = np.around(
                    np.linspace(
                        self.par.lon_start,
                        self.par.lon_end,
                        num = tick_nr
                               ),decimals = 2
                            )
                             
        #getting rot. lat-coords of grid lines to be labeled                        
        lat_plot = np.around(
                    np.linspace(
                        self.par.lat_start,
                        self.par.lat_end,
                        num = tick_nr
                               ),decimals = 2
                            )
        
        #maximum number of grid lines (lon_dim = lat_dim)
        ticks = self.par.lon_dim





        ################################################################
        ### actual plot ###
        ################################################################
                
        '''
        Plots heights of radar beam as isolines on the cartesian grid
        '''

        #create subplot
        fig,ax = plt.subplots(figsize=(8,8)) 

        #x- and y-tick positions
        ax.set_xticks(np.linspace(0,ticks,num=tick_nr), minor = False)                
        ax.set_yticks(np.linspace(0,ticks,num=tick_nr), minor = False)                
        
        #x- and y-tick labels
        ax.set_xticklabels(lon_plot,fontsize = 16)                                        
        ax.set_yticklabels(lat_plot,fontsize = 16,rotation='horizontal')                                        
        
        #grid
        ax.xaxis.grid(True, which='major',color = 'k')                                
        ax.yaxis.grid(True, which='major',color = 'k')
        
        #put grid in front of data                        
        ax.set_axisbelow(False)  
        
        #label x- and y-axis                                                  
        plt.xlabel('r_lon', fontsize = 18)                                    
        plt.ylabel('r_lat', fontsize = 18)    
        
        #contours of heights
        for isoline in isolines:

            #find contours
            contours = measure.find_contours(heights, isoline)
       
            #plot contours
            for n, contour in enumerate(contours):
                ax.plot(contour[:,1], contour[:,0], linewidth=1, 
                    color = 'b'
                    )
        
        #legend
        plt.legend(fontsize = 16)
    
        #title                           
        plt.title(
                  radar.name + ' - heights',
                  fontsize = 20
                  )

        #show plot
        plt.show()
