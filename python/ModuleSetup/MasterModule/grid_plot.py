###GridPlot class

'''
This file is reserved for the GridPlot Class.
'''





########################################################################
### modules ###
########################################################################

'''
Imports all modules needed for this class.
'''

#python modules
import numpy as np
from matplotlib.colors import LinearSegmentedColormap as lsc

#MasterModule
from .cartesian_grid import CartesianGrid





########################################################################
### GridPlot class ###
########################################################################
class GridPlot(CartesianGrid):
    
    '''
    GridPlot class for all plot objectives of a cartesian grid. Inherits
    from CartesianGrid object.
    '''

    



    ####################################################################
    ### Initialization ###
    ####################################################################
    def __init__(self,grid_par,plot_par):
        
        '''
        Saves all general attributes needed for creating a plot on a
        cartesian grid.        
        '''
        
        #call init of super class
        super().__init__(grid_par)

        #get number of labeled ticks in plot
        tick_nr        = plot_par[0]

        #if log_iso == True --> draw isolines around rain areas        
        self.log_iso   = plot_par[1]

        #get threshold, at which rain is assumed
        self.rain_th   = plot_par[2]

        #get x,y array to plot contour plots
        self.lon_plot  = np.arange(self.lon_dim)
        self.lat_plot  = np.arange(self.lat_dim)
        
        #get lon, lat ticks to be labeled
        self.lon_ticks = np.linspace(0,self.lon_dim-1,num=tick_nr)
        self.lat_ticks = np.linspace(0,self.lat_dim-1,num=tick_nr)

        #getting rot. lon-coords of grid lines to be labeled
        self.lon_label = np.around(
            np.linspace(self.lon_start,self.lon_end,num=tick_nr), 
            decimals=2
            )

        #getting rot. lat-coords of grid lines to be labeled                        
        self.lat_label = np.around(
            np.linspace(self.lat_start,self.lat_end,num=tick_nr),
            decimals=2
            )

        #get mask for grid boxes outside of pattern range
        self.mask      = self.get_mask()

        #create colormap for the mask
        colors         = ['#00000000','grey']
        self.cm_mask = lsc.from_list('cm_mask',colors)
       
       




    ####################################################################
    ### make plot ###
    ####################################################################
    def make_plot(self):

        '''
        This method belongs to specific plotting classes, which inherit
        from this GridPlot class.
        '''

        raise NotImplementedError
