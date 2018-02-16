""" Type member class
"""
from string import Template
FROM_PY = 1
TO_PY = 2
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
        if direction == TO_PY:
            if self.convert_function_to_py:
                return self.convert_function_to_py
            return "%s_to_py" % self.type
        if direction == FROM_PY:
            if self.convert_function_from_py:
                return self.convert_function_from_py
            return "py_to_%s" % self.type