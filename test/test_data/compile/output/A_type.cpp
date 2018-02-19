/*licenses
*/
#include "A_type.h"
#include "type_convert.h"
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
A_get_cmem(PyObject *self, void *closure)
{
    PyObject * py_cmem = int_to_py(reinterpret_cast<AObject *>(self)->cxxobj->cmem);
    // increase refcount
    Py_XINCREF(py_cmem);
    return py_cmem;
}

static int
A_set_cmem(PyObject *self, PyObject *value, void *closure)
{
    reinterpret_cast<AObject *>(self)->cxxobj->cmem = py_to_int(value);
    // set the cxxobj value
}

static PyObject *
A_get_ucmem(PyObject *self, void *closure)
{
    PyObject * py_ucmem = uint_to_py(reinterpret_cast<AObject *>(self)->cxxobj->ucmem);
    // increase refcount
    Py_XINCREF(py_ucmem);
    return py_ucmem;
}

static int
A_set_ucmem(PyObject *self, PyObject *value, void *closure)
{
    reinterpret_cast<AObject *>(self)->cxxobj->ucmem = py_to_uint(value);
    // set the cxxobj value
}

static PyObject *
A_get_shmem(PyObject *self, void *closure)
{
    PyObject * py_shmem = int_to_py(reinterpret_cast<AObject *>(self)->cxxobj->shmem);
    // increase refcount
    Py_XINCREF(py_shmem);
    return py_shmem;
}

static int
A_set_shmem(PyObject *self, PyObject *value, void *closure)
{
    reinterpret_cast<AObject *>(self)->cxxobj->shmem = py_to_int(value);
    // set the cxxobj value
}

static PyObject *
A_get_usmem(PyObject *self, void *closure)
{
    PyObject * py_usmem = uint_to_py(reinterpret_cast<AObject *>(self)->cxxobj->usmem);
    // increase refcount
    Py_XINCREF(py_usmem);
    return py_usmem;
}

static int
A_set_usmem(PyObject *self, PyObject *value, void *closure)
{
    reinterpret_cast<AObject *>(self)->cxxobj->usmem = py_to_uint(value);
    // set the cxxobj value
}

static PyObject *
A_get_imem(PyObject *self, void *closure)
{
    PyObject * py_imem = int_to_py(reinterpret_cast<AObject *>(self)->cxxobj->imem);
    // increase refcount
    Py_XINCREF(py_imem);
    return py_imem;
}

static int
A_set_imem(PyObject *self, PyObject *value, void *closure)
{
    reinterpret_cast<AObject *>(self)->cxxobj->imem = py_to_int(value);
    // set the cxxobj value
}

static PyObject *
A_get_uimem(PyObject *self, void *closure)
{
    PyObject * py_uimem = uint_to_py(reinterpret_cast<AObject *>(self)->cxxobj->uimem);
    // increase refcount
    Py_XINCREF(py_uimem);
    return py_uimem;
}

static int
A_set_uimem(PyObject *self, PyObject *value, void *closure)
{
    reinterpret_cast<AObject *>(self)->cxxobj->uimem = py_to_uint(value);
    // set the cxxobj value
}

static PyObject *
A_get_llmem(PyObject *self, void *closure)
{
    PyObject * py_llmem = longlong_to_py(reinterpret_cast<AObject *>(self)->cxxobj->llmem);
    // increase refcount
    Py_XINCREF(py_llmem);
    return py_llmem;
}

static int
A_set_llmem(PyObject *self, PyObject *value, void *closure)
{
    reinterpret_cast<AObject *>(self)->cxxobj->llmem = py_to_longlong(value);
    // set the cxxobj value
}

static PyObject *
A_get_limem(PyObject *self, void *closure)
{
    PyObject * py_limem = int_to_py(reinterpret_cast<AObject *>(self)->cxxobj->limem);
    // increase refcount
    Py_XINCREF(py_limem);
    return py_limem;
}

static int
A_set_limem(PyObject *self, PyObject *value, void *closure)
{
    reinterpret_cast<AObject *>(self)->cxxobj->limem = py_to_int(value);
    // set the cxxobj value
}

static PyObject *
A_get_umem(PyObject *self, void *closure)
{
    PyObject * py_umem = uint_to_py(reinterpret_cast<AObject *>(self)->cxxobj->umem);
    // increase refcount
    Py_XINCREF(py_umem);
    return py_umem;
}

static int
A_set_umem(PyObject *self, PyObject *value, void *closure)
{
    reinterpret_cast<AObject *>(self)->cxxobj->umem = py_to_uint(value);
    // set the cxxobj value
}

static PyObject *
A_get_ullmem(PyObject *self, void *closure)
{
    PyObject * py_ullmem = ulonglong_to_py(reinterpret_cast<AObject *>(self)->cxxobj->ullmem);
    // increase refcount
    Py_XINCREF(py_ullmem);
    return py_ullmem;
}

static int
A_set_ullmem(PyObject *self, PyObject *value, void *closure)
{
    reinterpret_cast<AObject *>(self)->cxxobj->ullmem = py_to_ulonglong(value);
    // set the cxxobj value
}

static PyObject *
A_get_ulimem(PyObject *self, void *closure)
{
    PyObject * py_ulimem = uint_to_py(reinterpret_cast<AObject *>(self)->cxxobj->ulimem);
    // increase refcount
    Py_XINCREF(py_ulimem);
    return py_ulimem;
}

static int
A_set_ulimem(PyObject *self, PyObject *value, void *closure)
{
    reinterpret_cast<AObject *>(self)->cxxobj->ulimem = py_to_uint(value);
    // set the cxxobj value
}

static PyObject *
A_get_fmem(PyObject *self, void *closure)
{
    PyObject * py_fmem = float_to_py(reinterpret_cast<AObject *>(self)->cxxobj->fmem);
    // increase refcount
    Py_XINCREF(py_fmem);
    return py_fmem;
}

static int
A_set_fmem(PyObject *self, PyObject *value, void *closure)
{
    reinterpret_cast<AObject *>(self)->cxxobj->fmem = py_to_float(value);
    // set the cxxobj value
}

static PyObject *
A_get_dmem(PyObject *self, void *closure)
{
    PyObject * py_dmem = double_to_py(reinterpret_cast<AObject *>(self)->cxxobj->dmem);
    // increase refcount
    Py_XINCREF(py_dmem);
    return py_dmem;
}

static int
A_set_dmem(PyObject *self, PyObject *value, void *closure)
{
    reinterpret_cast<AObject *>(self)->cxxobj->dmem = py_to_double(value);
    // set the cxxobj value
}

static PyObject *
A_get_smem(PyObject *self, void *closure)
{
    PyObject * py_smem = string_to_py(reinterpret_cast<AObject *>(self)->cxxobj->smem);
    // increase refcount
    Py_XINCREF(py_smem);
    return py_smem;
}

static int
A_set_smem(PyObject *self, PyObject *value, void *closure)
{
    reinterpret_cast<AObject *>(self)->cxxobj->smem = py_to_string(value);
    // set the cxxobj value
}

static PyObject *
A_get_cstrmem(PyObject *self, void *closure)
{
    PyObject * py_cstrmem = cstring_to_py(reinterpret_cast<AObject *>(self)->cxxobj->cstrmem);
    // increase refcount
    Py_XINCREF(py_cstrmem);
    return py_cstrmem;
}

static int
A_set_cstrmem(PyObject *self, PyObject *value, void *closure)
{
    reinterpret_cast<AObject *>(self)->cxxobj->cstrmem = py_to_cstring(value);
    // set the cxxobj value
}

static PyObject *
A_get_cxmem(PyObject *self, void *closure)
{
    PyObject * py_cxmem = cstring_to_py(reinterpret_cast<AObject *>(self)->cxxobj->cxmem);
    // increase refcount
    Py_XINCREF(py_cxmem);
    return py_cxmem;
}

static int
A_set_cxmem(PyObject *self, PyObject *value, void *closure)
{
    reinterpret_cast<AObject *>(self)->cxxobj->cxmem = py_to_cstring(value);
    // set the cxxobj value
}

static PyGetSetDef A_getseters[] = {
    {"cmem", A_get_cmem, A_set_cmem, NULL},
{"ucmem", A_get_ucmem, A_set_ucmem, NULL},
{"shmem", A_get_shmem, A_set_shmem, NULL},
{"usmem", A_get_usmem, A_set_usmem, NULL},
{"imem", A_get_imem, A_set_imem, NULL},
{"uimem", A_get_uimem, A_set_uimem, NULL},
{"llmem", A_get_llmem, A_set_llmem, NULL},
{"limem", A_get_limem, A_set_limem, NULL},
{"umem", A_get_umem, A_set_umem, NULL},
{"ullmem", A_get_ullmem, A_set_ullmem, NULL},
{"ulimem", A_get_ulimem, A_set_ulimem, NULL},
{"fmem", A_get_fmem, A_set_fmem, NULL},
{"dmem", A_get_dmem, A_set_dmem, NULL},
{"smem", A_get_smem, A_set_smem, NULL},
{"cstrmem", A_get_cstrmem, A_set_cstrmem, NULL},
{"cxmem", A_get_cxmem, A_set_cxmem, NULL},
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



