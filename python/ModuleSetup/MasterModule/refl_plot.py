###ReflPlot class

'''
This file is reserved for the ReflPlot class.
'''





########################################################################
### Modules ###
########################################################################

'''
Import all modules needed for this class.
'''

#python modules
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as lsc

#MasterModule
from .grid_plot      import GridPlot





########################################################################
### ReflPlot class ###
########################################################################
class ReflPlot(GridPlot):
    
    '''
    Class for plots reflectivity data on a cartesian grid. Inherits from 
    GridPlot.
    '''





    ####################################################################
    ### Initialization ###
    ####################################################################
    def __init__(self,grid_par,plot_par):
    
        '''
        Calls init-method of super class.
        '''
        
        #call init method of super class
        super().__init__(grid_par,plot_par)

        



    ####################################################################
    ### make plot ###
    ####################################################################
    def make_plot(self,refl_array,title):

        '''
        Plots interpolated reflectivity data on a cartesian grid 
        using imshow.

        Input: Reflectivity array to be plotted, title for plot.

        Output: None
        '''

        #create colormap for plot (continously changing colormap)                                                                    
        cmap = lsc.from_list(
            'my colormap',['white','blue','red','magenta']
            )

        #create subplot
        fig,ax = plt.subplots()

        #create imshow plot
        plt.imshow(refl_array[::-1],cmap=cmap,zorder=1)                  
        
        #colorbar
        cb = plt.colorbar()
        cb.set_label('reflectivity [dbz]',fontsize=18)
        cb.ax.tick_params(labelsize=16)
        
        #plot the mask
        plt.imshow(self.mask[::-1],cmap =self.cm_mask,zorder=2)
        
        #set ticks
        ax.set_xticks(self.lon_ticks)                
        ax.set_yticks(self.lat_ticks)                
       
        #set labels
        ax.set_xticklabels(self.lon_plot,fontsize=16)
        ax.set_yticklabels(
            self.lat_plot,fontsize=16,rotation='horizontal'
            )

        #grid
        ax.grid(color='k')
        ax.set_axisbelow(False)

        #label x- and y-axis                                                  
        plt.xlabel('r_lon',fontsize=18)                                    
        plt.ylabel('r_lat',fontsize=18)    
        
        #title 
        plt.title(title,fontsize=20)   
        
        #prevent parts of picture to be cut off
        plt.tight_layout()

        #show  
        plt.show()  
