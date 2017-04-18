###GridParameter class

'''
This file is reserved for the GridParameter class.
'''





########################################################################
### class for saving cartesian grid parameters ###
########################################################################
class GridParameter(object):
    
    '''
    Defines cartesian grid parameters as properties.
    '''
    




    ####################################################################
    ### Initialization ###
    ####################################################################
    def __init__(self):
        
        '''
        Does nothing so far
        '''
        
        pass
    
    
    
    
    
    ####################################################################
    ### starting longitude of cartesian grid ###
    ####################################################################
    @property
    def lon_start(self):
        
        '''
        Longitude coordinate (in rotated pole system) at which the
        cartesian grid begins. Must be float.
        '''
        
        try:
            return self._lon_start
        except AttributeError:
            return 0
            
    @lon_start.setter
    def lon_start(self,new_lon_start):
        assert (isinstance(new_lon_start, float),\
                'new_lon_start is not a float'
        self._lon_start = new_lon_start
        
        
        
        
        
    ####################################################################
    ### starting latitude of cartesian grid ###
    ####################################################################
    @property
    def lat_start(self):
        
        '''
        Latitude coordinate (in rotated pole system) at which the
        cartesian grid begins. Must be float.
        '''
        
        try:
            return self._lat_start
        except AttributeError:
            return 0
            
    @lat_start.setter
    def lat_start(self,new_lat_start):
        assert (isinstance(new_lat_start, float),\
                'new_lat_start is not a float'
        self._lat_start = new_lat_start
        
        
        
        
        
    ####################################################################
    ### ending longitude of cartesian grid ###
    ####################################################################
    @property
    def lon_end(self):
        
        '''
        Longitude coordinate (in rotated pole system) at which the
        cartesian grid ends. Must be float.
        '''
        
        try:
            return self._lon_end
        except AttributeError:
            return 0
            
    @lon_end.setter
    def lon_end(self,new_lon_end):
        assert (isinstance(new_lon_end, float),\
                'new_lon_end is not a float'
        self._lon_end = new_lon_end
        
        
        
        
        
    ####################################################################
    ### ending latitude of cartesian grid ###
    ####################################################################
    @property
    def lat_end(self):
        
        '''
        Latitude coordinate (in rotated pole system) at which the
        cartesian grid ends. Must be float.
        '''
        
        try:
            return self._lat_end
        except AttributeError:
            return 0
            
    @lat_end.setter
    def lat_end(self,new_lat_end):
        assert (isinstance(new_lat_end, float),\
                'new_lat_end is not a float'
        self._lat_end = new_lat_end
        
        
        
        
        
    ####################################################################
    ### grid resolution in meters ###
    ####################################################################
    @property
    def res_m(self):
        
        '''
        Resolution of cartesian grid in m. Must be float.
        '''
        
        try:
            return self._res_m
        except AttributeError:
            return 0
            
    @res_m.setter
    def res_m(self,new_res_m):
        assert isinstance(new_res_m, float),\
                'new_res_m is not a float'
        self._res_m = new_res_m





    ####################################################################
    ### grid resolution in degrees ###
    ####################################################################
    @property
    def res_deg(self):
        
        '''
        Resolution of cartesian grid in degree. Must be float.
        '''
        
        try:
            return self._res_deg
        except AttributeError:
            return 0
            
    @res_deg.setter
    def res_deg(self,new_res_deg):
        assert isinstance(new_res_deg, float),\
                'new_res_deg is not a float'
        self._res_deg = new_res_deg
    
    
    
    
        
    ####################################################################
    ### number of grid - rows ###
    ####################################################################
    @property
    def lon_dim(self):
        
        '''
        Number of rows (lons) in cartesian grid. Must be an integer.
        '''
        
        try:
            return self._lon_dim
        except AttributeError:
            return 0
            
    @lon_dim.setter
    def lon_dim(self,new_lon_dim):
        assert isinstance(new_lon_dim, int),\
                'new_lon_dim is not an integer'
        self._lon_dim = new_lon_dim    
        
        
        
        
        
    ####################################################################
    ### number of grid - lines ###
    ####################################################################
    @property
    def lat_dim(self):
        
        '''
        Number of lines (lat) of cartesian grid. Must be an integer.
        '''
        
        try:
            return self._lat_dim
        except AttributeError:
            return 0
            
    @lat_dim.setter
    def lat_dim(self,new_lat_dim):
        assert isinstance(new_lat_dim, int),\
                'new_lat_dim is not an integer'
        self._lat_dim = new_lat_dim
    
        
        
    

    ###################################################################
    ### rotated coordinates of grid center ###
    ###################################################################
    @property
    def site(self):
        
        '''
        Rotated coordinates pattern site. Must be list with
        two entries.
        '''
        
        try:
            return self._site
        except AttributeError:
            return 0
    
    @site.setter
    def site(self,new_site):
        assert isinstance(new_site, list), 'new_site is not a list'
        assert len(new_site) == 2, 'new_site has not the length of 2'
        self._site = new_site
        
    
    
    
    
    ###################################################################
    ### maximum range to be interpolated to grid ###
    ###################################################################
    @property
    def max_range(self):
        
        '''
        Maximum range to center of grid, that will be plotted. Must be
        float.
        '''
        
        try:
            return self._max_range
        except AttributeError:
            return 0
            
    @max_range.setter
    def max_range(self,new_max_range):
        assert isinstance(new_max_range, float),\
                'new_max_range is not a float'
        self._max_range = new_max_range
