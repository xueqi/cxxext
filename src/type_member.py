""" Type member class
"""
TO_PY = 0
FROM_PY = 1
from cxx_type import CXXType

class TypeMember(object):
    
    def __init__(self, name, cxx_type,
                 getter=True, setter=True,
                 is_public=False,
                 cls=None):
        self.name = name
        self.type = CXXType(cxx_type)
        # self.py_type = py_type
        self.getter = getter
        self.setter = setter
        self.cls = cls
        self.is_public = is_public
    def convert_to_python(self):
        """ convertion code from cxx type to python type
        """
        return self.type.convert_to_python(self.name)
    
    def get_setter_code(self):
        """ Generate setter code for this member in class
        """
        setter_code = """static int
{cls_name}_set_{name}(PyObject *self, PyObject *value, void *closure) {{
    reinterpret_cast<{cls_name}Object *>(self)->cxxobj->{name} = {setter_clause};
    // set the cxxobj value
}}
""".format(name=self.name, cls_name=self.cls.name,
           setter_clause=self.type.convert_from_python("value"))
  
        return setter_code
    
    def get_getter_code(self):
        """ Generate getter code for this member in class
        """
        getter_code = """static PyObject *
{cls_name}_get_{name}(PyObject *self, void *closure) {{
    PyObject * py_{name} = {convert_clause};
    // increase refcount
    Py_XINCREF(py_{name});
    return py_{name};
}}
""".format(name=self.name, convert_clause=self.type.convert_to_cxx()[0],
           cls_name=self.cls.name)
        return getter_code
        