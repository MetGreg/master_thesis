########################################################################
### main Radar-Object ###
########################################################################





########################################################################
### modules ###
########################################################################
import wradlib
import cartopy.crs as ccrs
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors 




########################################################################
### Main Radar class ###
########################################################################
class Radar(object):
     
     '''
     This main Radar-Object will get a sub-object for each of the 
     different radars (like pattern and boostedt).
     Methods working in general for the radars are part of main object.
     '''
     
     
     
     
     
     ###################################################################
     ### initialization ###
     ###################################################################
     def __init__(self):
          '''
          Does nothing so far 
          '''
          
          pass
     
     
     
     
     
     ###################################################################
     ### read_file-method ###
     ###################################################################
     def read_file(self):
          
          '''
          This method is specified in sub-objects, since reading files
          differs from radar to radar.
          '''
     
          raise NotImplementedError
     
     
     
     
     
     ###################################################################
     ### method to increase azimuth resolution by a factor ###
     ###################################################################
     def increase_azi_res(self):
          
          '''
          Increases azimuth resolution of radar dataset. This is done
          by looping through the data lines (azimuth angles) and
          copy each line 'res_fac' times to a new list. 
          This is equivalent to dividing all grid boxes into 
          'res_fac' sub-grid boxes, when the coordinates of the sub grid
          boxes are adjusted (growing with 1/x ° instead of 1°).
          '''
          
          #will be filled with reflectivity values of incr. resolution
          data_inc_res = []
          
          #loop through radar data lines (=azimuth angles)
          for data_line in self.data.refl:

               #append data line duplicate 'res_factor'-times         
               for i in range(self.res_fac):     
                    data_inc_res.append(data_line)
          
          #save artificially increased dataset to object
          self.data.refl_inc = np.array(data_inc_res)
         
          #azi. coords of data pts with artificially incr. res.
          azi_coords_inc = np.arange(
                            self.data.azi_start,
                            self.data.azi_steps*self.data.azi_rays\
                            + self.data.azi_start,
                            self.data.azi_steps/self.res_fac
                            )

          #take care of transition from 360 to 0
          self.data.azi_coords_inc = (azi_coords_inc + 360) % 360

     


     
     ###################################################################
     ### calculate coordinates of middle pixel for each box ###
     ###################################################################
     def get_pixel_center(self):           
     
          '''
          Calculates polar coordination of the middle pixel for each 
          polar grid box of radar data. 
          This is done by averaging azimuth angles and range values of 
          two adjacent data points respectively, for all data points.
          
          The average can be calculated simply by adding (subtracting) 
          half of the step to each value for data points at the near 
          (far) edge of the grid box. (only works, if angle and range
          step between 2 measurements don't change)
        
          The coordinates of the middle pixels are then saved
          in form of a numpy meshgrid, which gives access to all
          combinations of range and azimuth coordinates.
          '''
               
          #define shorter names for the coordination arrays
          range_coords = self.data.range_coords
          azi_coords   = self.data.azi_coords_inc
          
          #get array of azi coords of middle pixels
          azi_coords   = (azi_coords + self.data.azi_steps/\
                            (2*self.res_fac)) % 360
         
          #get array of range coords of middle pixels
          range_coords = range_coords - self.data.r_steps/2
           
          #create a numpy meshgrid
          pixel_center = np.meshgrid(range_coords, azi_coords)
          
          #return coords of middle pixels
          return pixel_center
     
     
     
     
     
     ###################################################################
     ### method to transform polar to cartesian coordinates ###
     ###################################################################
     def polar_to_cartesian(self,polar_range,polar_azi):
          
          '''
          Uses a wradlib function to calculate lon/lat cartesian 
          coordinates out of polar coordinates. Needs a wradlib 
          environment to work. See wradlib.org for more details.
          '''
          
          #transform polar coordinates to lon/lat cart. coordinates
          #lon.shape and lat.shape = (360,600) = (azimuth,range)
          lon,lat = wradlib.georef.polar2lonlat(
                        polar_range, polar_azi,
                        (self.data.lon_site, self.data.lat_site),
                        re=6370040
                        ) 

          #return cartesian coordinates
          return lon, lat





     ###################################################################
     ### method to transform cartesian to rotated pole coordinates ###
     ###################################################################
     def rotate_pole(self,lon,lat):
          
          '''
          Transforms cartesian coordinates to rotated pole coordinates
          using a function from Claire Merker. 
          (claire.merker@uni-hamburg.de)
          '''          
          
          #coordinates of rotated pole
          rotated_pole = [-170.415, 36.0625]
     
          #get projection
          proj         = ccrs.RotatedPole(
                                rotated_pole[0], 
                                rotated_pole[1]
                                )
          #calculate coordinates in rotated pole coordinate system
          coords_rot   = proj.transform_points(
                                ccrs.Geodetic(), lon, lat
                                )
          
          #return rotated coordinates
          return coords_rot
          
          
     


     ####################################################################
     ### method to plot radar data ###
     ####################################################################
     def plot(self):

        '''
        This method plots radar data without any interpolating.
        '''
        




        ################################################################
        ### prepare plot ###
        ################################################################

        '''
        prepares the plot by getting data and coordinates as well as
        turning them into 1D-arrays. (For easier plotting)
        '''

        #reflectivity array
        dbz          = self.data.refl
        
        #get time
        time_start   = self.data.time_start
        time_end     = self.data.time_end

        #get coordinates of data
        range_coords = self.data.range_coords
        azi_coords   = self.data.azi_coords

        #create mehsgrid to get all combinations of range and azimuth
        r,theta      = np.meshgrid(range_coords,azi_coords)

        #make angle, range and reflectivity arrays 1-D
        r            = np.reshape(r,len(range_coords)*len(azi_coords))
        theta        = np.reshape(
                    np.pi/180*theta,len(range_coords)*len(azi_coords)
                    )
        refl = np.reshape(dbz,len(range_coords)*len(azi_coords))






        ################################################################
        ### actual plot ###
        ################################################################
        
        '''
        plots data 
        '''

        #create colormap for plot (continously changing colormap)                                                                    
        cmap     = mcolors.LinearSegmentedColormap.from_list(
           'my colormap',['white','blue','red','magenta']
           )   
        
        #create plot and grid
        cgax, caax, paax, pm = wradlib.vis.plot_cg_ppi(
            dbz, range_coords, azi_coords, cmap = cmap, 
            vmin = -32.5, vmax = 70
                                                      )
        
        #create colorbar
        plt.colorbar(pm)
        
        #show plot
        plt.show()
        
        
