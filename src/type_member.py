""" Type member class
"""
from string import Template
TO_PY = 0
FROM_PY = 1

CONVERT_FUNCS = {
    "int" : ["int_to_py", "py_to_int"],
    "unsigned int" : ["uint_to_py", "py_to_uint"],
    "char" : ["int_to_py", "py_to_int"],
    "unsigned char" : ["uint_to_py", "py_to_uint"],
    "short" : ["int_to_py", "py_to_int"],
    "unsigned short" : ["uint_to_py", "py_to_uint"],
    "long" : ["int_to_py", "py_to_int"],
    "unsigned long" : ["uint_to_py", "py_to_uint"],
    "long long" : ["longlong_to_py", "py_to_longlong"],
    "unsigned long long":["ulonglong_to_py", "py_to_ulonglong"],
    "double" : ["double_to_py", "py_to_double"],
    "char *" : ["cstring_to_py", "py_to_cstring"],
    "const char *" : ["cstring_to_py", "py_to_cstring"],
    "string" : ["string_to_py", "py_to_string"]
    }

class CXXType(object):
    """ CXX type object.
    """
    def __init__(self, type_name):
        """
        """
        self.type_name = type_name.strip()
        self.master_type = type_name.split("<")[0]
        if "<" in type_name:
            # remote the outmost pair of <
            idx = type_name.index("<")
            tmp = type_name[idx+1:-1]
            # get the template types:
            

class TypeMember(object):
    
    def __init__(self, name, mem_type, convert_function_to_py=None,
                 convert_function_from_py=None,
                 getter=True, setter=True):
        self.name = name
        self.type = mem_type
        self.getter = getter
        self.setter = setter
        self.convert_function_to_py = convert_function_to_py
        self.convert_function_from_py = convert_function_from_py
        # check if the type is template: TODO
        
    def convert_to_python(self):
        """ convertion code from cxx type to python type
        """
        tpl = "${convert_func}"
        d = {"name": self.name, 
             "convert_func": self.get_convert_function(TO_PY)
             }
        return Template(tpl).substitute(d)
    
    def convert_to_cxx(self):
        """ Convertion code from python type to cxx
        """
        return self.get_convert_function(FROM_PY)
    
    def get_convert_function(self, direction):
        if self.type in CONVERT_FUNCS:
            return CONVERT_FUNCS[self.type][direction]
        if direction == TO_PY:
            if self.convert_function_to_py:
                return self.convert_function_to_py
            
            return "%s_to_py" % self.type
        if direction == FROM_PY:
            if self.convert_function_from_py:
                return self.convert_function_from_py
            return "py_to_%s" % self.type
