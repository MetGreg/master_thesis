########################################################################
### main Radar-Object ###
########################################################################





########################################################################
### modules ###
########################################################################
import wradlib.georef as geo
import cartopy.crs as ccrs
import numpy as np





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
          copy each line 'res_factor' times to a new list. 
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
          
     
     
     
     
     ###################################################################
     ### calculate coordinates of middle pixel for each box ###
     ###################################################################
     def get_pixel_center(self):           
     
          '''
          Calculates polar coordination of the middle pixel for each 
          polar grid box of radar data. 
          This is done by averaging azimuth angles and range values of 
          two adjacent data points respectively, for all data points. 
          Range coordinates of data points are at the far edge of the
          corresponding grid cell and azimuth coordinates are at the 
          near edge. This means, to obtain the coordinates of the middle 
          pixel of the last grid cell, the coordinates of the last data 
          point have to be averaged with coordinates of an additional 
          data point, which is artificially added.
          The coordinates of the middle pixels are then saved
          in form of a numpy meshgrid, which gives access to all
          combinations of range and azimuth coordinates.
          '''
               
          #define shorter names for the coordination arrays
          range_coords = self.data.range_coords
          azi_coords   = self.data.azi_coords_inc
          
          #append range coord of additional data point
          range_coords = np.append(
                                   range_coords, 
                                   range_coords[-1]\
                                   +(range_coords[-1]-range_coords[-2])
                                   )   
          
          #average all range coords
          range_coords = range_coords[:-1] -\
                         (range_coords[1:]-range_coords[:-1])\
                         /2. 
        
          #append azi coord of additional data point
          azi_coords   = np.append(
                                   azi_coords, azi_coords[-1] +\
                                   (azi_coords[-1]-azi_coords[-2])
                                   )                       
 
          #average all azi coords
          azi_coords   = azi_coords[:-1] +\
                         (azi_coords[1:]-azi_coords[:-1])\
                         /2.    
          
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
          lon,lat = geo.polar2lonlat(
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
          
          
     
