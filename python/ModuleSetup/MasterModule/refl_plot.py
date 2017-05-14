'''Class for plots of reflectivity on cartesian grids'''

# Python modules
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as lsc

# MasterModule
from .grid_plot import GridPlot


class ReflPlot(GridPlot):
    '''Class for plotting reflectivity data on a cartesian grid
    
    This is a subclass of the :any:`GridPlot` class. Using this class, 
    you can plot interpolated radar reflectivity on a cartesian grid. 
    
    '''

    def __init__(self, grid_par, plot_par):
        '''Initialization of object
        
        While initializing, only the :any:`GridPlot.__init__`-method 
        will be called.
        
        Args:
            grid_par (dict): Grid parameters, e.g. location, resolution
                and shape.
            plot_par (dict): Plot parameters, e.g. number of grid lines,
                logical variabel whether to plot rain area contours,
                dbz threshold, height isolines, mask range.
                
        '''
        super().__init__(grid_par, plot_par)

    def make_plot(self, refl_array, title):
        '''Create a plot of radar reflectivity on a cartesian grid
        
        Plots interpolated reflectivity data on a cartesian grid 
        using imshow.

        Args:
            refl_array (numpy.ndarray): Reflectivity data to be plotted.
            title (str): Title of plot.
        
        '''
        # Create colormap for plot (continously changing colormap)                                                                    
        cmap = lsc.from_list(
            'my colormap', ['white', 'blue', 'red', 'magenta']
            )

        # Create subplot
        fig, ax = plt.subplots(figsize=(8,8))

        # Create imshow plot
        plt.imshow(refl_array[::-1], cmap=cmap, zorder=1)                  
        
        # Colorbar
        cb = plt.colorbar()
        cb.set_label('reflectivity [dbz]', fontsize=18)
        cb.ax.tick_params(labelsize=16)
        
        # Plot the mask
        plt.imshow(self.mask[::-1], cmap =self.cm_mask, zorder=2)
        
        # Set ticks
        ax.set_xticks(self.lon_ticks)                
        ax.set_yticks(self.lat_ticks)                
       
        # Set labels
        ax.set_xticklabels(self.lon_label, fontsize=16)
        ax.set_yticklabels(
            self.lat_label, fontsize=16, rotation='horizontal'
            )

        # Grid
        ax.grid(color='k')
        ax.set_axisbelow(False)

        # Label x- and y-axis                                                  
        plt.xlabel('r_lon', fontsize=18)                                    
        plt.ylabel('r_lat', fontsize=18)    
        
        # Title 
        plt.title(title, fontsize=20)   
        
        # Prevent parts of the image to be cut off
        plt.tight_layout()

        # Show  
        plt.show()  
