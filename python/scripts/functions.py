'''This module contains all functions used for the MasterModule'''

# Python modules
import cartopy.crs as ccrs

def rotate_pole(lon, lat):
    '''Transform cartesian to rotated pole coordinates
    
    Transforms cartesian coordinates to rotated pole coordinates
    using a function from Claire Merker. Hamburg is near the equator in
    these rotated pole coordinates.
    (claire.merker@uni-hamburg.de)
    
    Args:
        lon (numpy.ndarray): Longitude coordinates to be transformed.
        lat (numpy.ndarray): Latitude coordinates to be transformed.
    
    Returns:
        (numpy.ndarray): Rotated pole coordinates.

    '''          
    # Coordinates of rotated pole
    rotated_pole = [-170.415, 36.0625]
    
    # Get projection
    proj = ccrs.RotatedPole(rotated_pole[0], rotated_pole[1])
    
    # Calculate coordinates in rotated pole coordinate system
    coords_rot = proj.transform_points(ccrs.Geodetic(), lon, lat)

    # Return rotated coordinates
    return coords_rot
    
