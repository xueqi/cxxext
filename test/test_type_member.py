'''
Created on Feb 16, 2018

@author: xueqi
'''
import unittest
from type_member import TypeMember
from type_class import TypeClass
PART = True
class TestTypeMember(unittest.TestCase):

    def assertCodeEqual(self, desired, actual):
        desired = desired.split("\n")
        actual = actual.split("\n")
        #self.assertEqual(len(desired), len(actual))
        for i in range(len(desired)):
            self.assertEqual(desired[i], actual[i])
    
    def testInit(self):
        tm = TypeMember("testname", "int")
    
    def test_convert_to_python(self):
        tm = TypeMember("testmem", "int")
        code = 'Py_BuildValue("i", testmem)'
        self.assertEqual(tm.convert_to_python(), code, tm.convert_to_python())
        
        tm = TypeMember("testmem1", "unsigned long")
        code = 'Py_BuildValue("k", testmem1)'
        self.assertEqual(tm.convert_to_python(), code, tm.convert_to_python())

    

    @unittest.skipIf(not PART, "PART TEST")    
    def test_create_setter(self):
        tc = TypeClass("myclass")
        member = TypeMember("mem1", "int", cls=tc)
        setter_code = """static int
myclass_set_mem1(PyObject *self, PyObject *value, void *closure) {
    reinterpret_cast<myclassObject *>(self)->cxxobj->mem1 = myclass_to_myclassObject(value);
    // set the cxxobj value
}

"""
        self.assertCodeEqual(tc.create_setter(member), setter_code)
    

    @unittest.skipIf(not PART, "PART TEST")    
    def test_create_getter(self):
        tc = TypeClass("myclass")
        member = TypeMember("mem1", "int", cls=tc)
        getter_code = """static PyObject *
myclass_get_mem1(PyObject *self, void *closure) {
    PyObject * py_mem1 = Py_BuildValue("i", reinterpret_cast<myclassObject *>(self)->cxxobj->mem1);
    // increase refcount
    Py_XINCREF(py_mem1);
    return py_mem1;
}

"""
        self.assertCodeEqual(tc.create_getter(member), getter_code)

        tc = TypeClass("myclass")
        member = TypeMember("mem1", "short int", cls=tc)
        getter_code = """static PyObject *
myclass_get_mem1(PyObject *self, void *closure) {
    PyObject * py_mem1 = Py_BuildValue("h", reinterpret_cast<myclassObject *>(self)->cxxobj->mem1);
    // increase refcount
    Py_XINCREF(py_mem1);
    return py_mem1;
}

"""
        self.assertCodeEqual(tc.create_getter(member), getter_code)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testINit']
    unittest.main()