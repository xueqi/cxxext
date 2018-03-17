'''
Created on Mar 12, 2018

@author: xueqi
'''
FMT_PY_TO_CXX = {"unsigned char" : "b",
             "short int" : "h",
             "unsigned short int" : "H",
             "unsigned short" : "H",
             "long" : "l",
             "int" : "i",
             "unsigned int" : "I",
             "long int" : "l",
             "unsigned long" : "k",
             "long long": "L",
             "unsigned long long" : "K",
             "Py_ssize_t": "n",
             "char" : "b",
             "float" : 'f',
             "double" : "d",
             "short" : "h"
    }
convert_func_py_to_cxx = {
    "str" : "PyString_As"
    }
FMT_CXX_TO_PY = FMT_PY_TO_CXX

CONVERT_FUNC = {"pointer" : "convert_pointer_to_py",
                "object" : "convert_object_to_py"
    }

class CXXType(object):
    """ CXX type object.
    """
    def __init__(self, cxx_type, py_type=None, is_template=False,
                 is_pointer=False):
        """
        """
        self.cxx_type = cxx_type
        self.py_type = py_type
        self.is_template = is_template
        self.is_pointer = is_pointer
        
    def convert_to_python(self, name):
        if self.cxx_type in FMT_PY_TO_CXX:
            return 'Py_BuildValue("{fmt}", {pointer}{name})'.format(
                fmt=FMT_CXX_TO_PY[self.cxx_type], name=name,
                pointer="*" if self.is_pointer else ""
                )
        else:
            return 'Py_BuildValue("O&", {convert_func}, {pointer}{name})'.format(
                convert_func=CONVERT_FUNC['pointer'],
                name=name,
                pointer="" if self.is_pointer else "&"
                )
    
    def get_convert_function(self):
        """ convert_function return None if it is primitive type
            This is used in parse python argument to cxx arguments.
        """
        if self.cxx_type in FMT_CXX_TO_PY:
            return FMT_CXX_TO_PY[self.cxx_type], None
        if self.is_pointer:
            return CONVERT_FUNC["pointer"]
        else:
            return CONVERT_FUNC["object"]
    
    def convert_from_python(self, name):
        """ Convert 
        """
        if self.cxx_type in convert_func_py_to_cxx:
            return convert_func_py_to_cxx[self.cxx_type]
        if self.py_type is None:
            self.py_type = "%sObject" % self.cxx_type
        return self.py_type.convert_to_cxx()[0]