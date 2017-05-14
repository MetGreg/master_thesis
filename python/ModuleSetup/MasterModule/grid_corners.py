'''Class for saving coordinates of grid corners'''


class GridCorners(object):
    '''Saves coordinates of grid corners'''
    
    def __init__(self):
        '''Initialization of object
        
        Does nothing so far.
        
        '''
        pass
        
    @property
    def lat_end(self):
        '''Ending latitude of grid
        
        Ending latitude of cartesian grid. 
        Must be a :any:`float`.
        
        '''
        try:
            return self._lat_end
        except AttributeError:
            return 0
        
    @lat_end.setter
    def lat_end(self, new_lat_end):
        assert(
            isinstance(new_lat_end, float)
            ), 'new_lat_end not a float'
        self._lat_end = new_lat_end

    @property
    def lat_start(self):
        '''Starting latitude of grid
        
        Starting latitude of cartesian grid. 
        Must be a :any:`float`.
        
        '''
        try:
            return self._lat_start
        except AttributeError:
            return 0
        
    @lat_start.setter
    def lat_start(self, new_lat_start):
        assert(
            isinstance(new_lat_start, float)
            ), 'new_lat_start not a float'
        self._lat_start = new_lat_start

    @property
    def lon_end(self):
        '''Ending Longitude of grid
        
        Ending longitude of cartesian grid. 
        Must be a :any:`float`.
        
        '''
        try:
            return self._lon_end
        except AttributeError:
            return 0
        
    @lon_end.setter
    def lon_end(self, new_lon_end):
        assert(
            isinstance(new_lon_end, float)
            ), 'new_lon_end not a float'
        self._lon_end = new_lon_end
    
    @property
    def lon_start(self):
        '''Starting Longitude of grid
        
        Starting longitude of cartesian grid. 
        Must be a :any:`float`.
        
        '''
        try:
            return self._lon_start
        except AttributeError:
            return 0
        
    @lon_start.setter
    def lon_start(self, new_lon_start):
        assert(
            isinstance(new_lon_start, float)
            ), 'new_lon_start not a float'
        self._lon_start = new_lon_start
