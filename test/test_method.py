'''
Created on Feb 19, 2018

@author: xueqi
'''
import unittest
from type_class import TypeClass
from type_method import TypeMethod

class TestArgument(unittest.TestCase):
    
    def test_types(self):
        pass

class TestMethod(unittest.TestCase):

    def setUp(self):
        super(TestMethod, self).setUp()
        self.cls = TypeClass("myclass")
        self.funcname = "funcname"
        self.func_type = "void (int, double)"
        self.argname = ["", "arg1"]
    def tearDown(self):
        super(TestMethod, self).tearDown()


    def test_parse_func_type(self):
        tm = TypeMethod(self.funcname, "void", [("arg1", "int"), ("arg2", "double")], {}, self.cls)
        rtype, args, kwargs = tm.rtn_type, tm.args, tm.kwargs
        self.assertEqual(rtype, "void")
        self.assertEqual(args, [("arg1", "int"), ("arg2", "double")])
        self.assertEqual(kwargs, {})
    
    def test_get_func_def_py(self):
        tm = TypeMethod(self.funcname, "void", [], {}, self.cls)
        self.assertEqual("myclass_funcname(myclassObject *self)", tm.get_func_def_py())
        tm = TypeMethod(self.funcname, "void", [("","int")], {}, self.cls)
        self.assertEqual("myclass_funcname(myclassObject *self, PyObject *args)", tm.get_func_def_py())
    
    def test_get_result(self):
        tm = TypeMethod(self.funcname, "void", [("arg1", "int")], {}, self.cls)
        r_d = "Py_RETURN_NONE;"
        self.assertEqual(r_d, tm.build_result("result_name"))
        tm = TypeMethod(self.funcname, "int", [("arg1", "int")], {}, self.cls)
        r_d = """PyObject * py_result = Py_BuildValue("i", result);
    return py_result;"""
        self.assertEqual(r_d, tm.build_result("result_name")) 
               
        tm = TypeMethod(self.funcname, "double", [("arg1", "int")], {}, self.cls)
        r_d = """PyObject * py_result = Py_BuildValue("d", result);
    return py_result;"""
        self.assertEqual(r_d, tm.build_result("result_name"))
        
        tm = TypeMethod(self.funcname, "MyModel", [("arg1", "MyModel")], {}, self.cls)
        r_d = """PyObject * py_result = Py_BuildValue("O", result);
    return py_result;"""
        self.assertEqual(r_d, tm.build_result("result_name"))
        
    def test_get_method_def(self):
        func_name = "funcname"
        tm = TypeMethod(func_name, "void", [("arg1", "int")], {}, self.cls)
        
        f_d = """PyObject *
myclass_funcname(myclassObject *self, PyObject *args) {
    int arg1 = 0;
    if (!PyArg_ParseTuple(args, "i", &arg1)) {
        return NULL;
    }
    self->cxxobj->funcname(arg1);
    Py_RETURN_NONE;
}
"""
        self.assertEqual(tm.get_code(), f_d, tm.get_code())
        
        tm = TypeMethod(func_name, "int", [("arg1", "int")], {}, self.cls)
        f_d = """PyObject *
myclass_funcname(myclassObject *self, PyObject *args) {
    int arg1 = 0;
    if (!PyArg_ParseTuple(args, "i", &arg1)) {
        return NULL;
    }
    int result = self->cxxobj->funcname(arg1);
    PyObject * py_result = Py_BuildValue("i", result);
    return py_result;
}
"""
        self.assertEqual(tm.get_code(), f_d, tm.get_code())
        
        tm = TypeMethod(func_name, "int", [("arg1", "int"), ("arg2", "float")], {}, self.cls)
        f_d = """PyObject *
myclass_funcname(myclassObject *self, PyObject *args) {
    int arg1 = 0;
    float arg2 = 0;
    if (!PyArg_ParseTuple(args, "if", &arg1, &arg2)) {
        return NULL;
    }
    int result = self->cxxobj->funcname(arg1, arg2);
    PyObject * py_result = Py_BuildValue("i", result);
    return py_result;
}
"""
        self.assertEqual(tm.get_code(), f_d, tm.get_code())
    
    @unittest.skip("pointer not implemented")
    def test_get_method_def_pointer(self):
    
        tm = TypeMethod(func_name, "int *", [("arg1", "int")], {}, self.cls)
        f_d = """PyObject *
myclass_funcname(myclassObject *self, PyObject *args)) {
    int arg1 = 0;
    if (!PyArg_ParseTuple(args, "i", &arg1) {
        return NULL;
    }
    int * result = self->cxxobj->funcname(arg1);
    return result;
}
"""
        self.assertEqual(tm.get_code(), f_d, tm.get_code())
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()