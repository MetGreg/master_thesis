###functions

'''
This file is reserved for all functions of the MasterModule.
'''





########################################################################
### Modules ###
########################################################################

'''
Import modules needed for all functions.
'''

import cartopy.crs as ccrs





###################################################################
### Transform cartesian to rotated pole coordinates ###
###################################################################
def rotate_pole(lon,lat):
    
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
    
