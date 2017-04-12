########################################################################
### class for a new defined cartesian grid ###
########################################################################





########################################################################
### modules ###
########################################################################
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as lsc
from skimage import measure
import seaborn as sb





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
        




        ################################################################
        ### read in grid definition ###
        ################################################################

        '''
        Reads the grid definition, as defined in parameters.py
        '''
        
        pat_site  = grid_par[0]        #rot. coords of pattern site
        max_range = grid_par[2]        #max. range (m) of pat radar 
        res       = float(grid_par[3]) #grid resolution in m
        shape     = grid_par[1]        #shape of the grid

        lon_start = pat_site[0] - 1/(60*1852/(res*shape[0]/2))
        lon_end   = pat_site[0] + 1/(60*1852/(res*shape[0]/2))                                      
        lat_start = pat_site[1] - 1/(60*1852/(res*shape[1]/2))                                    
        lat_end   = pat_site[1] + 1/(60*1852/(res*shape[1]/2))                                        
        


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
        self.pat_site       = pat_site

        #maximum range of pattern radar in m                                       
        self.max_range  = max_range

        #resolution in m                                    
        self.res_m      = res  

        #resolution in ° 
        #1° = 60 NM = 60*1852 m --> 250m = 1°/(60*1852/250)                                 
        self.res_deg    = 1/(60*1852/res)                         
        
        #number of rows and lines in cartesian grid-matrix
        self.lon_dim    = shape[0]    
        self.lat_dim    = shape[1]     
        
        #get coordinates of grid boxes in rotated coords
        lon = np.linspace(self.lon_start, self.lon_end, self.lon_dim)
        lat = np.linspace(self.lat_start, self.lat_end, self.lat_dim)

        #save coords to object
        self.rot_coords = np.array((lon,lat))




    
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
                        (radar.data.lon_rota - self.lon_start)\
                        /self.res_deg
                        )

        #calculate lat-indices of cart. grid boxes for radar data array
        lat_index = np.floor(
                        (radar.data.lat_rota - self.lat_start)\
                        /self.res_deg
                        )
        
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
        refl = np.empty((self.lat_dim,self.lon_dim))
        
        #calculate lon-indices of cart. grid boxes for radar data array
        lon_index = np.floor(
                        (radar.data.lon_rota - self.lon_start)\
                        /self.res_deg
                        )

        #calculate lat-indices of cart. grid boxes for radar data array
        lat_index = np.floor(
                        (radar.data.lat_rota - self.lat_start)\
                        /self.res_deg
                        )

        #loop through index matrix
        for line_nr in range(self.lat_dim):
            for row_nr in range(self.lon_dim):
                
                #get values of radar data array
                values = radar.data.refl_inc[a_index[line_nr][row_nr]]
                
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
        other locations are also possible.). Input site locations must
        be in rotated coordinates.
        1. step: Calculate for lon- and lat-direction respectively the
            difference in rotated coords between grid box and location.
        2. step: Transform difference in rotated coordinates to meters.
        3. step: Use pythagoras to calculate the distance between grid
            box and site.
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
        prepares plot by defining labling lists, ticks, mask, cmap etc. 
        '''
        
        #getting rot. lon-coords of grid lines to be labeled
        lon_plot = np.around(
            np.linspace(self.lon_start, self.lon_end, num=tick_nr),
            decimals=2
            )
                             
        #getting rot. lat-coords of grid lines to be labeled                        
        lat_plot = np.around(
            np.linspace(self.lat_start, self.lat_end, num=tick_nr),
            decimals=2
            )

        #create colormap for plot (continously changing colormap)                                                                    
        cmap = lsc.from_list(
            'my colormap',['white','blue','red','magenta']
            )    
        
        #colormap for mask
        cm_mask = lsc.from_list('cm_mask',['#00000000','grey'])

        #get mask for grid boxes outside of pattern range
        mask = self.get_mask()         
      




        ################################################################
        ### plot data ###
        ################################################################
        
        '''
        Plots interpolated radar data on the new cartesian grid using 
        imshow.
        '''
        
        #create subplot
        fig,ax = plt.subplots()

        #create imshow plot
        plt.imshow(refl[::-1],cmap=cmap,zorder=1)                  
        
        #colorbar
        cb = plt.colorbar()
        cb.set_label('reflectivity [dbz]',fontsize=18)
        cb.ax.tick_params(labelsize=16)
        
        #plot the mask
        plt.imshow(mask[::-1],cmap =cm_mask,zorder=2)
        
        #set ticks
        ax.set_xticks(np.linspace(0,self.lon_dim-1,num=tick_nr))                
        ax.set_yticks(np.linspace(0,self.lat_dim-1,num=tick_nr))                
       
        #set labels
        ax.set_xticklabels(lon_plot,fontsize=16)
        ax.set_yticklabels(lat_plot,fontsize=16,rotation='horizontal')

        #grid
        ax.grid(color='k')
        ax.set_axisbelow(False)

        #label x- and y-axis                                                  
        plt.xlabel('r_lon',fontsize=18)                                    
        plt.ylabel('r_lat',fontsize=18)    
        
        #title 
        plt.title(                                   \
                  str(radar.name)                    \
                  +'-data: '                         \
                  + str(radar.data.time_start.time())\
                  + ' - '                            \
                  + str(radar.data.time_end.time())  \
                  +'\n'                              \
                  + str(radar.data.time_end.date()),
                  fontsize=20
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
            np.linspace(self.lon_start,self.lon_end,num=tick_nr),
            decimals=2
            )
                             
        #getting rot. lat-coords of grid lines to be labeled                        
        lat_plot = np.around(
            np.linspace(self.lat_start,self.lat_end,num=tick_nr),
            decimals=2
            )
        
        #get the mask for grid boxes outside of pattern range
        mask = self.get_mask()

        #create colormap for the mask
        colors = ['#00000000','grey']
        cmap   = lsc.from_list('cm_mask',colors)
        




        ################################################################
        ### actual plot ###
        ################################################################
                
        '''
        Plots difference array on the new cartesian grid using imshow.
        '''
        
        #create subplot
        fig,ax = plt.subplots() 
        
        #create heatmap                                                                                                              
        plt.imshow(refl_diff[::-1],vmin=-70,vmax=70,cmap='bwr',zorder=1)      
        
        #colorbar
        cb = plt.colorbar()
        cb.set_label('reflectivity [dbz]',fontsize=20)
        cb.ax.tick_params(labelsize=18)
        
        #plot isolines around rain areas, if wished
        if log_iso == True:
            
            #contours around rain-areas
            contour1 = measure.find_contours(l_refl[0][::-1],rain_th)
            contour2 = measure.find_contours(l_refl[1][::-1],rain_th)
        
            #plot contours of radar1
            for n, contour in enumerate(contour1):
               plt.plot(
                    contour[:,1],contour[:,0],linewidth=1,color='b',
                    label='dwd',
                    )
            
            #plot contours of radar2
            for n, contour in enumerate(contour2):
                plt.plot(
                    contour[:,1],contour[:,0],linewidth=1,color='r',
                    label='pattern',
                    )
            
            #put mask in front of data
            plt.imshow(mask[::-1],cmap=cmap,zorder=2)
            
            #remove all labels except one of each radar
            lines = ax.get_lines()
            for line in lines[1:-1]:
                line.set_label('')
        
            #legend
            plt.legend(fontsize=18)
        
        #grid
        ax.grid(color='k')
        ax.set_axisbelow(False)
       
        #x- and y-tick positions
        ax.set_xticks(np.linspace(0,self.lon_dim-1,num=tick_nr))                
        ax.set_yticks(np.linspace(0,self.lat_dim-1,num=tick_nr))                
        
        #x- and y-tick labels
        ax.set_xticklabels(lon_plot,fontsize=18)                                        
        ax.set_yticklabels(lat_plot,fontsize=18,rotation='horizontal')                                        
        
        #label x- and y-axis                                                  
        plt.xlabel('r_lon', fontsize=20)                                    
        plt.ylabel('r_lat', fontsize=20)    

        #title                           
        plt.title(
                  radar2.name +                                     \
                  '(' + str(radar2.data.time_start.time()) + ' - '  \
                  + str(radar2.data.time_end.time()) + ')'          \
                  + ' minus ' + radar1.name                         \
                  + '(' + str(radar1.data.time_start.time()) + ' - '\
                  + str(radar1.data.time_end.time()) + ')\n'        \
                  +str(radar1.data.time_end.date()),
                  fontsize=24
                  )
        
        #show  
        plt.show()                                                                
        
        
        
        

    ####################################################################
    ### plot heights ###
    ####################################################################
    def plot_heights(self,heights,isolines,tick_nr,title):

        '''
        Plots heights of radar beam as isolines.
        '''
    




        ################################################################
        ### prepare plot ###
        ################################################################
        
        '''
        prepares plot by defining labling lists, masks etc. 
        '''

        #getting rot. lon-coords of grid lines to be labeled
        lon_plot = np.around(
            np.linspace(self.lon_start,self.lon_end,num=tick_nr), 
            decimals=2
            )

        #getting rot. lat-coords of grid lines to be labeled                        
        lat_plot = np.around(
            np.linspace(self.lat_start,self.lat_end,num=tick_nr),
            decimals=2
            )

        #get mask for grid boxes outside of pattern range
        mask = self.get_mask()

        #create masked array for plot
        masked_height = ma.masked_array(heights,mask=mask)

        #create colormap for the mask
        colors = ['#00000000','grey']
        cmap   = lsc.from_list('cm_mask',colors)
       




        ################################################################
        ### actual plot ###
        ################################################################
                
        '''
        Plots heights of radar beam as isolines on the cartesian grid.
        '''

        #create subplot
        fig,ax = plt.subplots() 
  
        #plot the contours
        CS = plt.contour(
            np.arange(self.lon_dim),np.arange(self.lat_dim), 
            masked_height[::-1],isolines,colors='k',zorder=1
            )

        #plot the mask
        plt.imshow(mask[::-1],cmap=cmap,zorder=2)
       
        #label the contours
        plt.clabel(CS,fontsize=18,fmt='%1.0f')

        #set ticks
        ax.set_xticks(np.linspace(0,self.lon_dim-1,num=tick_nr))                
        ax.set_yticks(np.linspace(0,self.lat_dim-1,num=tick_nr))                
       
        #set labels
        ax.set_xticklabels(lon_plot,fontsize=18)
        ax.set_yticklabels(lat_plot,fontsize=18,rotation='horizontal')
        
        #grid
        ax.grid(color='k')
        ax.set_axisbelow(False) 

        #label x- and y-axis                                                  
        plt.xlabel('r_lon',fontsize=20)                                    
        plt.ylabel('r_lat',fontsize=20)    

        #title                           
        plt.title(title,fontsize=24)
        
        #prevent parts of picture to be cut off
        plt.tight_layout()

        #show plot
        plt.show()
