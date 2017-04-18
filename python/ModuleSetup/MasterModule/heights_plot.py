###HeightsPlot class

'''
This file is reserved for the HeightsPlot class.
'''





########################################################################
### Modules ###
########################################################################

'''
Import all modules needed for this class.
'''

#python modules
import numpy.ma          as ma
import matplotlib.pyplot as plt

#MasterModule
from .grid_plot import GridPlot





########################################################################
### HeightsPlot class ###
########################################################################
class HeightsPlot(GridPlot):
    
    '''
    Class for plots of beam heights on a cartesian grid. Inherits from 
    GridPlot.
    '''





    ####################################################################
    ### Initialization ###
    ####################################################################
    def __init__(self,grid_par,plot_par):
    
        '''
        Calls init-method of super class and saves isolines 
        (to be plotted) to object.
        '''
        
        #call init method of super class
        super().__init__(grid_par,plot_par)

        #get isolines to be plotted
        self.height_iso = plot_par[3]





    ####################################################################
    ### make plot ###
    ####################################################################
    def make_plot(self,heights,title):

        '''
        Plots heights of beam as isolines on a cartesian grid.
        '''

        #create masked array for plot
        masked_height = ma.masked_array(heights,mask=self.mask)

        #create subplot
        fig,ax = plt.subplots() 
  
        #plot the contours
        CS = plt.contour(
            self.lon_plot,self.lat_plot,masked_height[::-1],
            self.height_iso,colors='k',zorder=1
            )

        #plot the mask
        plt.imshow(self.mask[::-1],cmap=self.cm_mask,zorder=2)
       
        #label the contours
        plt.clabel(CS,fontsize=18,fmt='%1.0f')

        #set ticks
        ax.set_xticks(self.lon_ticks)                
        ax.set_yticks(self.lat_ticks)                
       
        #set labels
        ax.set_xticklabels(self.lon_label,fontsize=18)
        ax.set_yticklabels(
            self.lat_label,fontsize=18,rotation='horizontal'
            )
        
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
