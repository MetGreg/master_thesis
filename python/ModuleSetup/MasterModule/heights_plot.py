'''Class for plots of heights on cartesian grids'''

# Python modules
import matplotlib.pyplot as plt
import numpy.ma as ma

# MasterModule
from .grid_plot import GridPlot


class HeightsPlot(GridPlot):
    '''Class for plots of beam heights on a cartesian grid
    
    This class is the subclass of the :any:`GridPlot` class. Using this 
    class, one can create a plot of height isolines on a cartesian grid.
    
    Attributes:
        height_iso (:any:`numpy.ndarray`): Array of height isolines to 
            be plotted.
        
    '''

    def __init__(self, grid_par, plot_par):
        '''Initialization of object
        
        Calls the :any:`GridPlot.__init__`-method and saves attributes.
        
        Args:
            grid_par (dict): Grid parameters, e.g. location, resolution
                and shape.
            plot_par (dict): Plot parameters, e.g. number of grid lines,
                logical variabel whether to plot rain area contours,
                dbz threshold, height isolines, mask range.
                
        '''
        
        # Call init method of super class
        super().__init__(grid_par, plot_par)

        # Get isolines to be plotted
        self.height_iso = plot_par['height_iso']
       
    def make_plot(self, heights, title):
        '''Make plot of beam heights
        
        Plots heights of beam as isolines on a cartesian grid.
        
        Args:
            heights (numpy.ndarray): Heights to be plotted.
            title (str): Title of the plot.
            
        '''

        # Create masked array for plot
        masked_height = ma.masked_array(heights, mask=self.mask)
        
        # Create subplot
        fig, ax = plt.subplots(figsize=(8,8)) 
  
        # Plot the contours
        CS = plt.contour(
            self.lon_plot, self.lat_plot, masked_height[::-1],
            self.height_iso, colors='k', zorder=1
            )

        # Plot the mask
        plt.imshow(self.mask[::-1], cmap=self.cm_mask, zorder=2)
       
        # Label the contours
        plt.clabel(CS, fontsize=18, fmt='%1.0f')

        # Set ticks
        ax.set_xticks(self.lon_ticks)                
        ax.set_yticks(self.lat_ticks)                
       
        # Set labels
        ax.set_xticklabels(self.lon_label, fontsize=18)
        ax.set_yticklabels(
            self.lat_label, fontsize=18, rotation='horizontal'
            )
        
        # Grid
        ax.grid(color='k')
        ax.set_axisbelow(False) 

        # Label x- and y-axis                                                  
        plt.xlabel('r_lon', fontsize=20)                                    
        plt.ylabel('r_lat', fontsize=20)    

        # Title                           
        plt.title(title, fontsize=24)
        
        # Prevent parts of picture to be cut off
        plt.tight_layout()
        
        # Show plot
        plt.show()
