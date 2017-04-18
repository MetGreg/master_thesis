###ReflDiffPlot class

'''
This file is reserved for the ReflDiffPlot class.
'''





########################################################################
### Modules ###
########################################################################

'''
Import all modules needed for this class.
'''

#python modules
import matplotlib.pyplot as plt
from skimage import measure

#MasterModule
from .grid_plot import GridPlot






########################################################################
### ReflDiffPlot class ###
########################################################################
class ReflDiffPlot(GridPlot):
    
    '''
    Class for plots differences in reflectivity between 2 radars 
    (Pattern and or Dwd) on a cartesian grid. Inherits from GridPlot.
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
    ### plot differences between radars ###
    ####################################################################
    def make_plot(self,l_refl,radar_names,title):
        
        '''
        Plots the differences in reflectivity between two radars on a 
        cartesian grid.
       
        Input: List of two radar data arrays, list of the corresponding 
        radar names and the title of the plot.

        Output: None
        '''

        #get reflectiviy differences        
        refl_diff = l_refl[1] - l_refl[0]

        #create subplot
        fig,ax = plt.subplots() 
        
        #create heatmap                                                                                                              
        plt.imshow(refl_diff[::-1],vmin=-70,vmax=70,cmap='bwr',zorder=1)      
        
        #colorbar
        cb = plt.colorbar()
        cb.set_label('reflectivity [dbz]',fontsize=20)
        cb.ax.tick_params(labelsize=18)
        
        #plot isolines around rain areas, if wished
        if self.log_iso == True:
            
            #find contours of first radar around rain areas
            contour1 = measure.find_contours(
                l_refl[0][::-1],self.rain_th
                )
            
            #find contours of second radar around rain areas
            contour2 = measure.find_contours(
                l_refl[1][::-1],self.rain_th
                )
        
            #plot contours of radar1
            for n, contour in enumerate(contour1):
               plt.plot(
                    contour[:,1],contour[:,0],linewidth=1,color='b',
                    label=radar_names[0],
                    )
            
            #plot contours of radar2
            for n, contour in enumerate(contour2):
                plt.plot(
                    contour[:,1],contour[:,0],linewidth=1,color='r',
                    label=radar_names[1],
                    )
            
            #remove all labels except one of each radar
            lines = ax.get_lines()
            for line in lines[1:-1]:
                line.set_label('')
        
            #legend
            plt.legend(fontsize=18)
        
        #put mask in front of data
        plt.imshow(self.mask[::-1],cmap=self.cm_mask,zorder=2)
           
        #grid
        ax.grid(color='k')
        ax.set_axisbelow(False)
       
        #x- and y-tick positions
        ax.set_xticks(self.lon_ticks)                
        ax.set_yticks(self.lat_ticks)                
        
        #x- and y-tick labels
        ax.set_xticklabels(self.lon_label,fontsize=18)                                        
        ax.set_yticklabels(
            self.lat_label,fontsize=18,rotation='horizontal'
            )                                        
        
        #label x- and y-axis                                                  
        plt.xlabel('r_lon', fontsize=20)                                    
        plt.ylabel('r_lat', fontsize=20)    
        
        #title
        plt.title(title,fontsize=20)

        #take care of layout
        plt.tight_layout()

        #show  
        plt.show()                                                                
