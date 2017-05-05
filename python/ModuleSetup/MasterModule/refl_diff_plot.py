'''This module only contains the ReflDiffPlot class, which can be used
to plot reflectivity differences on a cartesian grid.

'''
# Python modules
import matplotlib.pyplot as plt
from skimage import measure

# MasterModule
from .grid_plot import GridPlot


class ReflDiffPlot(GridPlot):
    '''Class for difference plots on a cartesian grid
    
    This class is a subclass of the GridPlot class. It can be used to
    plot reflectivity differences of two radars (Pattern or DWD) on a 
    cartesian grid.
    
    '''

    def __init__(self, grid_par, plot_par):
        '''Initialization of object
        
        Calls init-method of super class.
       
        Args:
            grid_par (dict): Grid parameters, e.g. location, resolution
                and shape.
            plot_par (dict): Plot parameters, e.g. number of grid lines,
                logical variabel whether to plot rain area contours,
                dbz threshold, height isolines, mask range.
                
        '''
        
        # Call init method of super class
        super().__init__(grid_par, plot_par)

    def make_plot(self, data1, data2, name1, name2, title):
        '''Make plot of reflectivity differences
        
        Plots the differences in reflectivity between two radars on a 
        cartesian grid.
       
        Args:
            data1 (numpy.ndarray): Data of first radar.
            data2 (numpy.ndarray): Data of second radar.
            name1 (str): Name of first radar.
            name2 (str): Name of second radar.
            title (str): Title of the plot.
            
        '''
        # Get reflectiviy differences        
        refl_diff = data2 - data1

        # Create subplot
        fig, ax = plt.subplots() 
        
        # Create heatmap                                                                                                              
        plt.imshow(
            refl_diff[::-1], vmin=-70, vmax=70, cmap='bwr', zorder=1
            )      
        
        # Colorbar
        cb = plt.colorbar()
        cb.set_label('reflectivity [dbz]', fontsize=20)
        cb.ax.tick_params(labelsize=18)
        
        # Plot isolines around rain areas, if wished
        if self.log_iso:
            
            # Find contours of first radar around rain areas
            contour1 = measure.find_contours(
                data1[::-1], self.rain_th
                )
            
            # Find contours of second radar around rain areas
            contour2 = measure.find_contours(
                data2[::-1], self.rain_th
                )
        
            # Plot contours of radar1
            for n, contour in enumerate(contour1):
               plt.plot(
                    contour[:,1], contour[:,0], linewidth=1, color='b',
                    label=name1,
                    )
            
            # Plot contours of radar2
            for n, contour in enumerate(contour2):
                plt.plot(
                    contour[:,1], contour[:,0], linewidth=1, color='r',
                    label=name2,
                    )
            
            # Remove all labels except one of each radar
            lines = ax.get_lines()
            for line in lines[1:-1]:
                line.set_label('')
        
            # Legend
            plt.legend(fontsize=18)
        
        # Put mask in front of data
        plt.imshow(self.mask[::-1], cmap=self.cm_mask, zorder=2)
           
        # Grid
        ax.grid(color='k')
        ax.set_axisbelow(False)
       
        # x- and y-tick positions
        ax.set_xticks(self.lon_ticks)                
        ax.set_yticks(self.lat_ticks)                
        
        # x- and y-tick labels
        ax.set_xticklabels(self.lon_label, fontsize=18)                                        
        ax.set_yticklabels(
            self.lat_label, fontsize=18, rotation='horizontal'
            )                                        
        
        # Label x- and y-axis                                                  
        plt.xlabel('r_lon', fontsize=20)                                    
        plt.ylabel('r_lat', fontsize=20)    
        
        # Title
        plt.title(title, fontsize=20)

        # Take care of layout
        plt.tight_layout()

        # Show  
        plt.show()                                                                
