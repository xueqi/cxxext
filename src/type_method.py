'''
Created on Feb 19, 2018

@author: xueqi
'''
# https://docs.python.org/3/c-api/arg.html
FMT_PY_TO_CXX = {"unsigned char" : "b",
             "short int" : "h",
             "unsigned short int" : "H",
             "int" : "i",
             "unsigned int" : "I",
             "long int" : "l",
             "unsigned long" : "k",
             "long long": "L",
             "unsigned long long" : "K",
             "Py_ssize_t": "n",
             "char" : "b",
             "float" : 'f',
             "double" : "d"
    }

FMT_CXX_TO_PY = {"unsigned char" : "b",
             "short int" : "h",
             "unsigned short int" : "H",
             "int" : "i",
             "unsigned int" : "I",
             "long int" : "l",
             "unsigned long" : "k",
             "long long": "L",
             "unsigned long long" : "K",
             "Py_ssize_t": "n",
             "char" : "b",
             "float" : 'f',
             "double" : "d"
    }

class Variable(object):
    """ A variable is a struct that store the information needed to convert between cxx and python
    if cxx_type is a primitive variable, fmt is the corresponding value in FMT_CXX_TO_PY
    if cxx_type is a class, fmt is "O&", which uses converter function
    """
    def __init__(self, cxx_type, py_type):
        self.cxx_type = cxx_type
        self.py_type = py_type
        if self.cxx_type in FMT_PY_TO_CXX:
            self.fmt = FMT_PY_TO_CXX[self.cxx_type]
        else:
            self.fmt = "O&"
            self.converter_name = "convert_%s_%s" % (cxx_type, py_type) 
    def converter_cxx_to_py(self):
        """ Converter function for buildValue
        status = converter(object, address)
        template <class T>
        PyObject * converter(void * address) {
            T * cxxobj = static_cast<T*>address;
            
        }
        """

class Argument(object):
    def __init__(self, c_type, py_type, fmt):
        self.c_type = c_type
        self.py_type = py_type
        self.fmt = fmt
        self.py2cxx = None
        self.cxx2py = None
        
    def get_format(self):
        return self.fmt
    
    def get_cxx2py_code(self, cxxname):
        """ Get convert code from cxxname
        """
        if self.cxx2py is None:
            return 'Py_BuildValue("{fmt}", {cxxname})'.format(
                fmt=self.fmt, cxxname=cxxname)
        else:
            return 'Py_BuildValue("O&", {converter}, {cxxname})'.format(
                converter = self.cxx2py,
                cxxname=cxxname)
    
int_argument = Argument('int', int, 'i')
float_argument = Argument('float', float, 'f')

class TypeMethod(object):
    '''
    method class
    '''
    def __init__(self, func_name, rtn_type, args, kwargs, cls=None):
        '''
        :param func_name: The function name
        :param func_type: The signature of the function
        
        '''
        self.name = func_name
        self.rtn_type = rtn_type
        self.cls = cls
        self.args = args
        self.kwargs = kwargs
        #self.rtn_type, self.args, self.kwargs = self.parse_func_type(func_type)

    
    def get_method_def(self):
        """ Return the method define in _methods[] structure
        """
        flags = []
        if self.args:
            flags.append("METH_VARARGS")
        if self.kwargs:
            flags.append("METH_KEYWORDS")
        if not flags:
            flags = ["METH_NOARGS"]
        func_name = self.get_func_name()
        return '{"%s", (PyCFunction)%s, %s, ""}' % (
            self.name,
            self.get_func_name(),
            " | ".join(flags),
            )
    
    def get_code(self):
        """ take python function
            call the c++ function, 
            return python type
            
        """
        code = "PyObject *\n"
        code += self.get_func_def_py()
        code += " {\n"
        arg_list = []
        fmt_type = ""
        # define local variable
        for arg_name, arg_type in self.args:
            arg_define = "    %s %s = %s;" % (arg_type, arg_name, 0)
            code += arg_define + "\n"
            if arg_type in FMT_CXX_TO_PY:
                fmt_type += FMT_CXX_TO_PY[arg_type]
            else:
                arg_type += "?"
            arg_list.append(arg_name)
        arg_list_str = ", ".join(arg_list)
        # convert python argument to c++ argument
        convert_code = '''    if (!PyArg_ParseTuple(args, "{fmt}", {args})) {{
        return NULL;
    }}
'''.format(fmt=fmt_type, args=", ".join(["&%s" % _ for _ in arg_list]))
        code += convert_code
        func_code = "self->cxxobj->{func_name}({arg_list});".format(
            func_name=self.name, arg_list=arg_list_str)
        if self.rtn_type != "void":
            func_code = "{rtn_type} result = ".format(rtn_type=self.rtn_type) + func_code
        code += "    %s\n" % func_code
        # get return value
        code += "    %s\n" % self.build_result()
        code += "}\n"
        return code
    
    def build_result(self, result_name="result"):
        """ Build return clause
        """
        if self.rtn_type == "void":
            return "Py_RETURN_NONE;"
        # for builtin type
        return self.build_result_for_return_type("result", "py_result",
                                                self.rtn_type);
    
    def build_result_for_return_type(self, c_result_name, py_result_name,
                                     return_type=None):
        """ Build result for return type
        PyObject * py_result = Py_BuildValue(fmt, &result);
        return py_result;
        """
        rtn_type = return_type
        if rtn_type in FMT_PY_TO_CXX:
            fmt = FMT_PY_TO_CXX[rtn_type]
        else:
            fmt = "O"
        return """PyObject * py_result = Py_BuildValue("{fmt}", result);
    return py_result;""".format(fmt=fmt)
    
    def get_func_def_py(self):
        """ Get function definition
        """ 
        func_def = "%s(%sObject *self" % (self.get_func_name(), self.cls.name)
        if self.args or self.kwargs:
            func_def += ", PyObject *args"
        if self.kwargs:
            func_def += ", PyObject *kwargs"
        func_def += ")"
        return func_def
    
    def get_func_name(self):
        if self.cls:
            return "%s_%s" % (self.cls.name, self.name)
        else:
            return self.name