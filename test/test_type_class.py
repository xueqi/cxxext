'''
Created on Feb 16, 2018

@author: xueqi
'''
import unittest
from type_class import TypeClass
from type_member import TypeMember

PART = True
class TestTypeClass(unittest.TestCase):


    def testInit(self):
        self.assertRaises(Exception, TypeClass)
        self.assertRaises(Exception, TypeClass, ['Not Valid Class Name'])
        tc = TypeClass("myclass")
        self.assertEqual(tc.members, [], "Should be empty list")
        self.assertEqual(tc.methods, [], "Should be empty list")
        self.assertEqual(tc.name, "myclass", 
                         "The name should be the same as in constructor")
    def testAddMember(self):
        tc = TypeClass("myclass")
        tc.add_member("member1", "int")
        self.assertEqual(len(tc.members), 1, "Should have one member")
        member = tc.members[0]
        self.assertEqual(member.name, "member1")
    
    @unittest.skipIf(not PART, "PART TEST")
    def test_create_new(self):
        tc = TypeClass("myclass")
        func_new = """static PyObject *
myclass_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    myclassObject *self;
    self = (myclassObject *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->cxxobj = NULL;
        self->cxxobj_owner = NULL;
    }
    return (PyObject *)self;
}

"""
        self.assertEqual(tc.create_new(), func_new, tc.create_new())
    
    def assertCodeEqual(self, desired, actual):
        desired = desired.split("\n")
        actual = actual.split("\n")
        self.assertEqual(len(desired), len(actual))
        for i in range(len(desired)):
            self.assertEqual(desired[i], actual[i])
    
    def test_create_init_with_obj_address(self):
        tc = TypeClass("myclass")
        func_code = """static PyObject *
myclass_new_with_address(myclass *obj) {
    myclassObject * py_obj = PyObject_New(myclassObject, &myclassType);
    py_obj->cxxobj = obj;
    return py_obj;
}
"""
        self.assertCodeEqual(func_code, tc.create_init_with_obj_address())
    
    @unittest.skipIf(not PART, "PART TEST")
    def test_create_init(self):
        tc = TypeClass("myclass")
        func_init = """static int
myclass_init(myclassObject *self, PyObject *args, PyObject *kwds) {
    myclass* cxxobj = NULL;
    myclassObject *owner = NULL;
    // if the cxxobj is passed as an argument, we borrow the reference.
    if (PyTuple_Size(args) != 0) {
        PyObject *passed = PyTuple_GetItem(args, 0);
        // make sure the object is the myclassObject
        if (myclass_check(passed)) {
            owner = (myclassObject *)passed;
            cxxobj = owner->cxxobj;
        }
    }
    if (cxxobj == NULL) {
        // we create a new instance of class. 
        // This should put in a template. 
        // #check the arguments and put in constructor
        cxxobj = new myclass();
    }
    self->cxxobj = cxxobj;
    self->cxxobj_owner = owner;
    // increase the owner refcount, so that even the owner is deleted, 
    // we still could access the c++ class
    // be sure to reduce the refcount in dealloc
    Py_XINCREF(self->cxxobj_owner);
}

"""
        #print tc.create_new()
        #for l1, l2 in zip(tc.create_init().split("\n"), func_init.split("\n")):
        #    if not l1 == l2:
        #        print l1, l2
        self.assertEqual(tc.create_init(), func_init, tc.create_init())
        
    @unittest.skipIf(not PART, "PART TEST")    
    def test_create_struct(self):
        tc = TypeClass("myclass")
        struct_code = """typedef struct _myclassObject {
    PyObject_HEAD
    myclass * cxxobj;
    _myclassObject * cxxobj_owner;
} myclassObject;

"""
        self.assertEqual(tc.create_struct(), struct_code, tc.create_struct())

    @unittest.skipIf(not PART, "PART TEST")    
    def test_create_dealloc(self):
        tc = TypeClass("myclass")
        dealloc_code = """static void
myclass_dealloc(myclassObject* self) {
    // reduce the owner that contain the cxxobj
    Py_XDECREF(self->cxxobj_owner);
    // the owner will dealloc the ref to cxxobj
    if (!self->cxxobj_owner) { // this instance own the cxxobj
        delete self->cxxobj;
    }
}

"""
        self.assertEqual(tc.create_dealloc(), dealloc_code, tc.create_dealloc())
    @unittest.skipIf(not PART, "PART TEST")    
    def test_header(self):
        """ Create a header for class
        """
        tc = TypeClass("myclass")
        self.assertEqual(tc.header_file, "myclass_type.h")
        header = """/*licenses
*/
#include <Python.h>
#include <iostream>
#include "myclass.h"
typedef struct _myclassObject {
    PyObject_HEAD
    myclass * cxxobj;
    _myclassObject * cxxobj_owner;
} myclassObject;


extern PyTypeObject myclassType;
"""
        self.assertEqual(tc.create_header_file("myclass.h"), header, tc.create_header_file("myclass.h"))
    
    @unittest.skipIf(PART, "PART TEST")    
    def test_cpp(self):
        """ Create a code for class
        """
        tc = TypeClass("myclass")
        self.assertEqual(tc.cpp_file, "myclass_type.cpp")
        code = '''/*licenses
*/
#include "myclass_type.h"
static PyObject *
myclass_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    myclassObject *self;
    myclass* cxxobj = NULL;
    myclassObject *owner = NULL;
    // if the cxxobj is passed as an argument, we borrow the reference.
    if (PyTuple_GetSize(args) != 0) {
        PyObject *passed = PyTuple_GetItem(args, 0);
        // make sure the object is the myclassObject
        if (PyObject_IsInstance(passed, myclassObject)) {
            owner = (myclassObject *)args;
            cxxobj = owner->cxxobj;
            
        } else {
            // Raise an error that the passed class is not the same as this class
            PyErr_SetString(PyExc_TypeEror, "Parameter must be myclassObject object");
            return -1;
        }
    } else {
        // we create a new instance of class. // This should put in a template.
        cxxobj = myclass();
    }
    self = (myclassObject *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->cxxobj = cxxobj;
        self->cxxobj_owner = owner;
        // increase the owner refcount, so that even the owner is deleted, 
        // we still could access the c++ class
        // be sure to reduce the refcount in dealloc
        Py_INCREF(self->cxxobj_owner);
    }
    return (PyObject *)self;
}
static void
myclass_dealloc(myclassObject* self) {
    // reduce the owner that contain the cxxobj
    Py_XDECREF(self->cxxobj_owner);
    // the owner will dealloc the ref to cxxobj
    if (!self->cxxobj_owner) { // this instance own the cxxobj
        delete self->cxxobj;
    }
}
static PyTypeObject myclassType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "myclass",             /* tp_name */
    sizeof(myclassObject),             /* tp_basicsize */
    0,                         /* tp_itemsize */
    (destructor)myclass_dealloc, /* tp_dealloc */
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
    "myclass objects",           /* tp_doc */
    0,                         /* tp_traverse */
    0,                         /* tp_clear */
    0,                         /* tp_richcompare */
    0,                         /* tp_weaklistoffset */
    0,                         /* tp_iter */
    0,                         /* tp_iternext */
    myclass_methods,             /* tp_methods */
    myclass_members,             /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)myclass_init,      /* tp_init */
    0,                         /* tp_alloc */
    myclass_new,                 /* tp_new */
};


'''
        #self.assertEqual(tc.create_cpp_file(), code, tc.create_cpp_file())
    @unittest.skipIf(not PART, "PART TEST")    
    def test_create_def(self):
        tc = TypeClass("myclass")
        type_def = """PyTypeObject myclassType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "myclass",             /* tp_name */
    sizeof(myclassObject),             /* tp_basicsize */
    0,                         /* tp_itemsize */
    (destructor)myclass_dealloc, /* tp_dealloc */
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
    "myclass objects",           /* tp_doc */
    0,                         /* tp_traverse */
    0,                         /* tp_clear */
    0,                         /* tp_richcompare */
    0,                         /* tp_weaklistoffset */
    0,                         /* tp_iter */
    0,                         /* tp_iternext */
    myclass_methods,           /* tp_methods */
    0,                         /* tp_members */
    myclass_getseters,        /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)myclass_init,      /* tp_init */
    0,                         /* tp_alloc */
    myclass_new,                 /* tp_new */
};

"""
        self.assertCodeEqual(tc.create_type_def(), type_def)
    
    @unittest.skip("Unit nex test for type class")
    def test_nothing(self):
        tc = TypeClass("myclass")
        print tc.create_cpp_file()
    
    
    def create_test_class(self):
        cxx_code = """class A {
    int a;
    float b;
    bool c;
public:
    A();
    void func_a(int, double);
};
"""
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()