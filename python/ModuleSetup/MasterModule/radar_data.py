'''Class for general radar data properties'''

# Python modules
import numpy as np
from datetime import datetime


class RadarData(object):
    '''Class to save radar data properties
    
    This class is used to define general, for different radars identical 
    radar data properties. 
    
    '''
    
    def __init__(self):
        '''Initializiation of object
        
        Does nothing so far.
        
        '''
        pass
    
    @property
    def azi_rays(self):
        '''Number of azimuth rays
        
        Number of azimuth rays of the radar, which usually is 360. 
        Must be an :any:`int`.
        
        '''
        try:
            return self._azi_rays
        except AttributeError:
            return 0    
        
    @azi_rays.setter
    def azi_rays(self, new_azi_rays):
        assert(
            isinstance(new_azi_rays, np.int64) 
            or isinstance(new_azi_rays, int)
            ), 'new azi_rays not an integer' 
        self._azi_rays = new_azi_rays
    
    @property
    def azi_start(self):
        '''Starting azimuth
        
        Starting value of azimuth angle. 
        Must be a :any:`float`.
        
        '''
        try:
            return self._azi_start
        except AttributeError:
            return 0

    @azi_start.setter
    def azi_start(self, new_azi_start):
        assert isinstance(new_azi_start, float), 'azi_start not a float'
        self._azi_start = new_azi_start

    @property
    def azi_steps(self):
        '''Azimuth steps
        
        Steps between two measurements in azimuth angle. 
        Must be a :any:`float`.
        
        '''
        try:
            return self._azi_steps
        except AttributeError:
            return 0

    @azi_steps.setter
    def azi_steps(self, new_azi_steps):
        assert isinstance(new_azi_steps, float), 'azi_steps not a float'
        self._azi_steps = new_azi_steps
        
    @property
    def ele(self):
        '''Elevation
        
        Elevation of radar beam in degrees. 
        Must be a :any:`numpy.ndarray` or a :any:`float`.
        
        '''
        try:
            return self._ele
        except AttributeError:
            return 0

    @ele.setter
    def ele(self, new_ele):
        assert(
            isinstance(new_ele, np.ndarray) 
            or isinstance(new_ele, np.float64)
            or isinstance(new_ele, np.float32)
            ), 'new_ele not a float'
        self._ele = new_ele
        
    @property
    def lat_site(self):
        '''Latitude coordinate
        
        Latitude coordinate of radar location. 
        Must be a :any:`float` or a :any:`numpy.ndarray`.
        
        '''
        try:
            return self._lat_site
        except AttributeError:
            return 0
    
    @lat_site.setter
    def lat_site(self, new_lat_site):
        assert(
            isinstance(new_lat_site, np.ndarray) 
            or isinstance(new_lat_site, np.float64)
            or isinstance(new_lat_site, float)
            ), 'new_lat_site not a float'
        self._lat_site = new_lat_site
    
    @property
    def lon_site(self):
        '''Longitde coordinate
        
        Longitude coordinate of radar location. 
        Must be a :any:`float` or a :any:`numpy.ndarray`.
        
        '''
        try:
            return self._lon_site
        except AttributeError:
            return 0
        
    @lon_site.setter
    def lon_site(self, new_lon_site):
        assert(
            isinstance(new_lon_site, np.ndarray) 
            or isinstance(new_lon_site, np.float64)
            or isinstance(new_lon_site, float)
            ), 'new_lon_site not a float'
        self._lon_site = new_lon_site
        
    @property
    def r_bins(self):
        '''Number of range bins
        
        Number of range bins of the radar. 
        Must be an :any:`int`.
        
        '''
        try:
            return self._r_bins
        except AttributeError:
            return 0
        
    @r_bins.setter
    def r_bins(self, new_r_bins):
        assert(
            isinstance(new_r_bins, np.int64)
            or isinstance(new_r_bins, int)
            ), 'new r_bins not an integer' 
        self._r_bins = new_r_bins

    @property
    def r_start(self):
        '''Starting range
        
        Starting value of range. 
        Must be a :any:`float`.
        
        '''
        try:
            return self._r_start
        except AttributeError:
            return 0

    @r_start.setter
    def r_start(self, new_r_start):
        assert(
            isinstance(new_r_start, np.float32)
            or isinstance(new_r_start, np.float64)
            or isinstance(new_r_start, float)
            ), 'r_start not a float'
        self._r_start = new_r_start

    @property
    def r_steps(self):
        '''Range steps
        
        Steps in range between two measurements. 
        Must be a :any:`float`.
        
        '''
        try:
            return self._r_steps
        except AttributeError:
            return 0

    @r_steps.setter
    def r_steps(self, new_r_steps):
        assert(
            isinstance(new_r_steps, np.float32)
            or isinstance(new_r_steps, np.float64)
            ), 'r_steps not a float'
        self._r_steps = new_r_steps

    @property
    def refl(self):
        '''Reflectivity
        
        Reflectivity measured by the radar. 
        Must be a 2D :any:`numpy.ndarray`.
        
        '''
        try:
            return self._refl
        except AttributeError:
            return 0
        
    @refl.setter
    def refl(self, new_refl):
        assert(
            isinstance(new_refl, np.ndarray)
            ), 'new refl is no numpy array'
        assert(
            len(new_refl.shape) == 2
            ), 'new refl is not 2-dimensional'
        self._refl = new_refl
