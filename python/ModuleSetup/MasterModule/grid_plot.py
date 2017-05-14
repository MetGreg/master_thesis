'''Class for general plots on cartesian grids'''

# Python modules
import numpy as np
from matplotlib.colors import LinearSegmentedColormap as lsc

# MasterModule
from .cartesian_grid import CartesianGrid


class GridPlot(CartesianGrid):
    '''Class for plotting on a cartesian grid
    
    This class is a subclass of the :any:`CartesianGrid` class and the 
    super class of :any:`ReflPlot`, :any:`HeightsPlot` and 
    :any:`ReflDiffPlot`. This class only saves all general attributes, 
    which are the same for all kind of plots on a cartesian grid.
    
    Attributes:
        log_iso (:any:`bool`): If True --> isolines around rain areas will be 
            plotted.
        rain_th (:any:`int`): Dbz threshold, at which rain is assumed.
        lon_plot (:any:`numpy.ndarray`): All longitude ticks.
        lat_plot (:any:`numpy.ndarray`): All latitude ticks.
        lon_ticks (:any:`numpy.ndarray`): Longitude ticks, which will be 
            labeled.
        lat_ticks (:any:`numpy.ndarray`): Latitute ticks, which will be 
            labeled.
        lon_label (:any:`numpy.ndarray`): Labels of Longitude ticks.
        lat_label (:any:`numpy.ndarray`): Labels of Latitude ticks.
        mask (:any:`numpy.ndarray`): Mask array.
        cm_mask (:any:`matplotlib.colors.LinearSegmentedColormap`): 
            Colormap for the mask.
        
    '''

    def __init__(self, grid_par, plot_par):
        '''Initialization of GridPlot
        
        Calls the :any:`CartesianGrid.__init__`-method and saves all 
        general attributes needed for creating a plot on a cartesian 
        grid.        
        
        Args:
            grid_par (dict): Grid parameters, e.g. location, resolution
                and shape.
            plot_par (dict): Plot parameters, e.g. number of grid lines,
                logical variabel whether to plot rain area contours,
                dbz threshold, height isolines, mask range
                
        '''
        # Call initialization method of super class
        super().__init__(grid_par)

        # Get number of labeled ticks in plot
        tick_nr = plot_par['tick_nr']

        # If log_iso == True --> draw isolines around rain areas        
        self.log_iso = plot_par['log_iso']

        # Get threshold, at which rain is assumed
        self.rain_th = plot_par['rain_th']

        # Get x,y array to plot contour plots
        self.lon_plot = np.arange(self.lon_shape)
        self.lat_plot = np.arange(self.lat_shape)
        
        # Get lon, lat ticks to be labeled
        self.lon_ticks = np.linspace(0, self.lon_shape - 1, num=tick_nr)
        self.lat_ticks = np.linspace(0, self.lat_shape - 1, num=tick_nr)

        # Getting rot. lon-coords of grid lines to be labeled
        self.lon_label = np.around(
            np.linspace(self.corners.lon_start, self.corners.lon_end,
            num=tick_nr), decimals=2
            )

        # Getting rot. lat-coords of grid lines to be labeled                        
        self.lat_label = np.around(
            np.linspace(self.corners.lat_start, self.corners.lat_end,
            num=tick_nr), decimals=2
            )

        # Get mask for grid boxes outside of pattern range
        self.mask = self.get_mask(plot_par['max_range'])

        # Create colormap for the mask
        colors = ['#00000000', 'grey']
        self.cm_mask = lsc.from_list('cm_mask', colors)
       
    def make_plot(self):
        '''Create a plot on a cartesian grid
        
        This method belongs to specific subclasses :any:`ReflPlot`,
        :any:`HeightsPlot` or :any:`ReflDiffPlot`. When the method is 
        called from this superclass, raise an Error.
        
        Raises:
            NotImplementedError: If this method is called.
        
        '''
        # Raise error
        raise NotImplementedError
