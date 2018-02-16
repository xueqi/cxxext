/*licenses
*/
#include "A_type.h"
bool A_check(PyObject*);;
static PyObject *
A_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    AObject *self;
    self = (AObject *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->cxxobj = NULL;
        self->cxxobj_owner = NULL;
    }
    return (PyObject *)self;
}
static void
A_dealloc(AObject* self) {
    // reduce the owner that contain the cxxobj
    Py_XDECREF(self->cxxobj_owner);
    // the owner will dealloc the ref to cxxobj
    if (!self->cxxobj_owner) { // this instance own the cxxobj
        delete self->cxxobj;
    }
}
static int
A_init(AObject *self, PyObject *args, PyObject *kwds) {
    A* cxxobj = NULL;
    AObject *owner = NULL;
    // if the cxxobj is passed as an argument, we borrow the reference.
    if (PyTuple_Size(args) != 0) {
        PyObject *passed = PyTuple_GetItem(args, 0);
        // make sure the object is the AObject
        if (A_check(passed)) {
            owner = (AObject *)passed;
            cxxobj = owner->cxxobj;
        }
    }
    if (cxxobj == NULL) {
        // we create a new instance of class. 
        // This should put in a template. 
        // #check the arguments and put in constructor
        cxxobj = new A();
    }
    self->cxxobj = cxxobj;
    self->cxxobj_owner = owner;
    // increase the owner refcount, so that even the owner is deleted, 
    // we still could access the c++ class
    // be sure to reduce the refcount in dealloc
    Py_INCREF(self->cxxobj_owner);
}
static PyObject *
A_get_imem(AObject *self, void *closure)
{
    PyObject * py_imem = int_to_py(self->cxxobj->imem);
    // increase refcount
    Py_XINCREF(py_imem);
    return py_imem;
}
static PyObject *
A_get_imem(AObject *self, PyObject *value, void *closure)
{
    self->cxxobject->imem = py_to_int(value);
    // set the cxxobj value
}
static PyObject *
A_get_fmem(AObject *self, void *closure)
{
    PyObject * py_fmem = float_to_py(self->cxxobj->fmem);
    // increase refcount
    Py_XINCREF(py_fmem);
    return py_fmem;
}
static PyObject *
A_get_fmem(AObject *self, PyObject *value, void *closure)
{
    self->cxxobject->fmem = py_to_float(value);
    // set the cxxobj value
}
static PyGetSetDef A_getseters[] = {
    {"A", A_get_imem, A_set_imem, NULL},
{"A", A_get_fmem, A_set_fmem, NULL},
{NULL}/* Sentinel */
};
static PyMethodDef A_methods[] = {
    {NULL}/* Sentinel */
};
static PyTypeObject AType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "A",             /* tp_name */
    sizeof(AObject),             /* tp_basicsize */
    0,                         /* tp_itemsize */
    (destructor)A_dealloc, /* tp_dealloc */
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
    "A objects",           /* tp_doc */
    0,                         /* tp_traverse */
    0,                         /* tp_clear */
    0,                         /* tp_richcompare */
    0,                         /* tp_weaklistoffset */
    0,                         /* tp_iter */
    0,                         /* tp_iternext */
    A_methods,           /* tp_methods */
    0,                         /* tp_members */
    A_getseters,        /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)A_init,      /* tp_init */
    0,                         /* tp_alloc */
    A_new,                 /* tp_new */
};
bool
A_check(PyObject *obj) {
    return PyObject_IsInstance(obj, (PyObject*)&AType);
}

