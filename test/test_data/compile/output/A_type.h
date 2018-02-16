/*licenses
*/
#include <Python.h>
#include "a.h"
typedef struct _AObject {
    PyObject_HEAD
    A * cxxobj;
    _AObject * cxxobj_owner;
} AObject;
