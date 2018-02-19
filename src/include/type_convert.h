#ifndef TYPE_CONVERT_H
#define TYPE_CONVERT_H

#include <Python.h>
#include <string>
using namespace std;
// Convert to python object.
PyObject * int_to_py(int);
PyObject * uint_to_py(int);
PyObject * longlong_to_py(long long);
PyObject * ulonglong_to_py(unsigned long long);
PyObject * double_to_py(double);
PyObject * float_to_py(float);
PyObject * bool_to_py(bool);
PyObject * string_to_py(string&);
PyObject * cstring_to_py(const char *);

// convert from PyObject
int py_to_int(PyObject *);
unsigned int py_to_uint(PyObject *);
unsigned long long py_to_ulonglong(PyObject *);
long long py_to_longlong(PyObject *);
double py_to_double(PyObject *);
float  py_to_float(PyObject *);
bool py_to_bool(PyObject *);
string py_to_string(PyObject *);
char * py_to_cstring(PyObject *);

#endif