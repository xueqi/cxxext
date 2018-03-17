'''
python wrapper for c++ class
The wrapper class definition _fields_ depends on how the c++ file is compiled.
So the wrapper should be difference for each compilation
@author: xueqi
'''
from ctypes import *
FUNC_SIGNATURES = {}

LP_c_char = POINTER(c_char)
LP_LP_c_char = POINTER(LP_c_char)

def new_struct(struct_name, struct_size=None):
    new_s = type(struct_name, (Structure, ), {})
    if struct_size:
        new_s._fields_ = [("data", POINTER(c_char) * struct_size)]
    new_s.spelling = struct_name
    def update(other):
        new_s._fields_.extend(other._fields_)
    new_s.update = staticmethod(update)
    new_s.size = 0
    def __str__(self):
        return self.struct_name
    new_s.__str__ = __str__
    new_s.__repr__ = __str__
    return new_s

class Wrapper(Structure):
    '''
    A wrapper structure is a c++ class instance.
    '''
    def __init__(self, handle, instance=None, *args, **kwargs):
        '''
        Constructor
        '''
        self.handle = handle
        self.name = self.__class__.__name__
        super(Wrapper, self).__init__(*args, **kwargs)
    
    def get_func(self, func_name):
        real_func_name = "%s_%s" % (self.name, func_name)
        try:
            print real_func_name
            func = getattr(self.handle, real_func_name)
        except AttributeError:
            func = None
        return func

class B(Wrapper):
    _fields_ = [
        ("a", c_int),
        ("b", c_int)
        ]
    def __init__(self, *args, **kwargs):
        super(B, self).__init__(*args, **kwargs)
        
class A(Wrapper):
    _fields_ = [
        ("a", c_int),
        ("b", c_int),
        ("bbb", B),
        ("c", c_int),
        ("d", c_int)
        ]
    
    def __init__(self, *args, **kwargs):
        super(A, self).__init__(*args, **kwargs)
    