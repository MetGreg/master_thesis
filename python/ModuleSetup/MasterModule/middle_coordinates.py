'''Class for saving coordinates of grid box middle pixels'''

# python modules
import numpy as np


class MiddleCoordinates(object):
    '''Saves coordinates of grid box middle pixels'''
    
    def __init__(self):
        '''Initialization of object
        
        Does nothing so far.
        
        '''
        pass
       
    @property
    def azi(self):
        '''Azimuth coordinates
        
        Azimuth coordinates of grid box mids. 
        Must be a :any:`numpy.ndarray`.
        
        '''
        try:
            return self._azi
        except AttributeError:
            return 0
    
    @azi.setter
    def azi(self, new_azi):
        assert(
            isinstance(new_azi, np.ndarray)
            ), 'new_azi not a numpy.ndarray'
        self._azi = new_azi
    
    @property
    def range_(self):
        '''Range coordinates
        
        Range coordinates of grid box mids. 
        Must be a :any:`numpy.ndarray`.
        
        '''
        try:
            return self._range_
        except AttributeError:
            return 0
    
    @range_.setter
    def range_(self, new_range_):
        assert(
            isinstance(new_range_, np.ndarray)
            ), 'new_range_ not a numpy.ndarray'
        self._range_ = new_range_
    
