'''
Created on Feb 16, 2018

@author: xueqi
'''
import re
from string import Template
from type_member import TypeMember
import code

class TypeClass(object):
    '''
    The high level type class that parsed from c++ header file
    '''

    def __init__(self, classname, mod=None):
        '''
        Constructor
        '''
        # check class name. If not valid c++ class Name, raises
        # template class should count as valid class, with specified type
        if not self.is_valid_class_name(classname):
            raise Exception("Invalid class name")
        self.name = classname
        self.mod = mod
        self.methods = []
        self.members = []
        self.export_functions = []
        self.foward_declares = []
    def add_member(self, name, type):
        self.members.append(TypeMember(name, type))
    
    def add_method(self, name, rtn_type, args):
        """ Add a method with return type rtn_type, and arguments args
        :param name: The method name. Should be 
        """
    
    def is_valid_class_name(self, classname):
        """ Check if the class name is valid. 
        Class name should start with _ or alphabet,
        and containing only _ , alphabet, digit 
        """
        if not re.match(r"[_A-Za-z][_\w]*", classname):
            return False
        return True
    
    def create_methods(self):
        """ 
        """
        all_method_defs = []
        for method in self.methods:
            code += self.create_method_function(method)
            all_method_defs.append(method.get_method_def())
        all_method_defs.append("{NULL}")
        # add the member def section
        tpl = """static PyMethodDef ${name}_methods[] = {
    ${all_method_defs}/* Sentinel */
};
"""
        d = {"name" : self.name, 
             "all_method_defs" : ",\n".join(all_method_defs)}
        getset_code = Template(tpl).substitute(d)
        return getset_code
    
    
    def create_members(self):
        """ Member is exposed as properties.
        """
        code = ""
        all_member_defs = []
        def_tpl = Template("{\"${name}\", ${getter}, ${setter}, NULL}")
        for member in self.members:
            code += self.create_member_function(member)
            
            d = { "name" : self.name, 
                 "getter" : "NULL",
                 "setter" : "NULL",
                 }
            if member.getter:
                d["getter"] = self.get_getter_name(member.name)
            if member.setter:
                d["setter"] = self.get_setter_name(member.name)
            all_member_defs.append(def_tpl.substitute(d))
        all_member_defs.append("{NULL}")
        # add the member def section
        tpl = """static PyGetSetDef ${name}_getseters[] = {
    ${all_member_defs}/* Sentinel */
};
"""
        d = {"name" : self.name, 
             "all_member_defs" : ",\n".join(all_member_defs)}
        getset_code = Template(tpl).substitute(d)
        return code + getset_code
    
    def get_getter_name(self, mem_name):
        return "%s_get_%s" % (self.name, mem_name)
    
    def get_setter_name(self, mem_name):
        return "%s_set_%s" % (self.name, mem_name)
    
    def create_member_function(self, member, getter=True, setter=True):
        """ Create member function getter and setter.
        """
        
        code = ""
        if getter:
            code += self.create_getter(member)
        if setter:
            code += self.create_setter(member)
        return code
    
    def create_setter(self, member):
        """ A typical setter is to unwrap the python type into cxx type, 
        and set the cxxobj->mem
        The convert function should be an attribute of member
        """
        tpl = """static PyObject *
${name}_get_${mem_name}(${name}Object *self, PyObject *value, void *closure)
{
    self->cxxobject->${mem_name} = ${convert_func}(value);
    // set the cxxobj value
}
"""
        d = {"name" : self.name, "mem_name": member.name,
             "convert_func" : member.convert_to_cxx()}
        getter_code = Template(tpl).substitute(d)
        return getter_code
    
    def create_getter(self, member):
        """ A typical getter is to wrap the cxx type into python type, 
        and return the wrapped value.
        The convert function should be an attribute of member
        """
        tpl = """static PyObject *
${name}_get_${mem_name}(${name}Object *self, void *closure)
{
    PyObject * py_${mem_name} = ${convert_func}(self->cxxobj->${mem_name});
    // increase refcount
    Py_XINCREF(py_${mem_name});
    return py_${mem_name};
}
"""
        d = {"name" : self.name, "mem_name": member.name,
             "convert_func" : member.convert_to_python()}
        getter_code = Template(tpl).substitute(d)
        return getter_code
        
    
    def create_init(self):
        """ Create the init function.
        Init function will replace the new function.
        """
        tpl = """static int
${name}_init(${name}Object *self, PyObject *args, PyObject *kwds) {
    ${name}* cxxobj = NULL;
    ${name}Object *owner = NULL;
    // if the cxxobj is passed as an argument, we borrow the reference.
    if (PyTuple_Size(args) != 0) {
        PyObject *passed = PyTuple_GetItem(args, 0);
        // make sure the object is the ${name}Object
        if (${name}_check(passed)) {
            owner = (${name}Object *)passed;
            cxxobj = owner->cxxobj;
        }
    }
    if (cxxobj == NULL) {
        // we create a new instance of class. 
        // This should put in a template. 
        // #check the arguments and put in constructor
        cxxobj = new ${name}();
    }
    self->cxxobj = cxxobj;
    self->cxxobj_owner = owner;
    // increase the owner refcount, so that even the owner is deleted, 
    // we still could access the c++ class
    // be sure to reduce the refcount in dealloc
    Py_INCREF(self->cxxobj_owner);
}
"""
        d = {"name":self.name}
        func_code = Template(tpl).substitute(d)
        return func_code
    
    def create_new(self):
        """ Create a new function statements. 
        If the c++ class is wrapped and passed to args, 
        the member is a reference to the passed argument.
        Otherwise create a new reference
        
        """
        tpl = """static PyObject *
${name}_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    ${name}Object *self;
    self = (${name}Object *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->cxxobj = NULL;
        self->cxxobj_owner = NULL;
    }
    return (PyObject *)self;
}
"""
        d = {"name":self.name}
        func_code = Template(tpl).substitute(d)
        return func_code
    
    def create_dealloc(self):
        tpl = """static void
${name}_dealloc(${name}Object* self) {
    // reduce the owner that contain the cxxobj
    Py_XDECREF(self->cxxobj_owner);
    // the owner will dealloc the ref to cxxobj
    if (!self->cxxobj_owner) { // this instance own the cxxobj
        delete self->cxxobj;
    }
}
"""
        d = {"name":self.name}
        dealloc_code = Template(tpl).substitute(d)
        return dealloc_code
    
    def create_struct(self):
        """ Create a struct of the class, which containing the c++ class instance
            This should goto header file
        """
        
        tpl = """typedef struct _${name}Object {
    PyObject_HEAD
    ${name} * cxxobj;
    _${name}Object * cxxobj_owner;
} ${name}Object;
"""
        d = {"name":self.name}
        struct_code = Template(tpl).substitute(d)
        return struct_code

    def create_cpp_file(self):
        tpl = """${license}#include "${name}_type.h"
${all_code}
"""
        d = {"license" : '/*%s*/\n' % self.get_license(), 
             "all_code" : self.get_all_code(),
             "name" : self.name}
        cpp_code = Template(tpl).substitute(d)
        return cpp_code
    
    def get_all_code(self):
        """ Combine all code
        """
        codes = ""
        codes += self.create_new()
        codes += self.create_dealloc()
        codes += self.create_init()
        codes += self.create_members()
        codes += self.create_methods()
        # others
        codes += self.create_type_def()
        # add the utility functions;
        # The typecheck
        codes += self.create_type_check()
        dec = ""
        for fd in self.foward_declares:
            dec += "%s;\n" % fd
        codes = dec + codes
        return codes
    
    def create_header_file(self, class_includes):
        tpl = """${license}#include <Python.h>
#include "${class_includes}"
${struct_code}"""
        d = {"license" : '/*%s*/\n' % self.get_license(), 
             "struct_code" : self.create_struct(),
             "class_includes": class_includes}
        header_code = Template(tpl).substitute(d)
        return header_code
    
    def create_type_check(self):
        tpl = """bool
${name}_check(PyObject *obj) {
    return PyObject_IsInstance(obj, (PyObject*)&${name}Type);
}
"""
        self.foward_declares.append("bool %s_check(PyObject*);" % self.name)
        d = {"name":self.name}
        check_code = Template(tpl).substitute(d)
        return check_code
    
    def create_type_def(self):
        """ Create the definition of the type.
        """
        tpl = """static PyTypeObject ${name}Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "${typename}",             /* tp_name */
    sizeof(${name}Object),             /* tp_basicsize */
    0,                         /* tp_itemsize */
    (destructor)${name}_dealloc, /* tp_dealloc */
    0,                         /* tp_print */
    0,                         /* tp_getattr */
    0,                         /* tp_setattr */
    0,                         /* tp_compare */
    0,                         /* tp_repr */
    0,                         /* tp_as_number */
    0,                         /* tp_as_sequence */
    0,                         /* tp_as_mapping */
    0,                         /* tp_hash */
    0,                         /* tp_call */
    0,                         /* tp_str */
    0,                         /* tp_getattro */
    0,                         /* tp_setattro */
    0,                         /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT |
        Py_TPFLAGS_BASETYPE,   /* tp_flags */
    "${name} objects",           /* tp_doc */
    0,                         /* tp_traverse */
    0,                         /* tp_clear */
    0,                         /* tp_richcompare */
    0,                         /* tp_weaklistoffset */
    0,                         /* tp_iter */
    0,                         /* tp_iternext */
    ${name}_methods,           /* tp_methods */
    0,                         /* tp_members */
    ${name}_getseters,        /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)${name}_init,      /* tp_init */
    0,                         /* tp_alloc */
    ${name}_new,                 /* tp_new */
};
"""
        d = {"name":self.name, "typename":self.type_name}
        def_code = Template(tpl).substitute(d)
        return def_code
    
    def get_license(self):
        return "licenses\n"
    
    @property
    def header_file(self):
        return "%s_type.h" % self.name
    @property
    def cpp_file(self):
        return "%s_type.cpp" % self.name
    @property
    def type_name(self):
        if self.mod:
            return "%s.%s" % (self.mod, self.name)
        else:
            return self.name
    