'''
Created on Feb 16, 2018

@author: xueqi
'''
import unittest
from type_member import TypeMember

class TestTypeMember(unittest.TestCase):


    def testInit(self):
        tm = TypeMember("testname", "int")
    
    def test_convert_to_python(self):
        tm = TypeMember("testmem", "int")
        code = "int_to_py"
        self.assertEqual(tm.convert_to_python(), code, tm.convert_to_python())
        
        tm = TypeMember("testmem1", "ulong", "ultopy", "pytoul")
        code = "ultopy"
        self.assertEqual(tm.convert_to_python(), code, tm.convert_to_python())
    
    def test_convert_to_cxx(self):
        tm = TypeMember("testmem", "int")
        code = "py_to_int"
        self.assertEqual(tm.convert_to_cxx(), code, tm.convert_to_cxx())
        
        tm = TypeMember("testmem1", "ulong", "ultopy", "pytoul")
        code = "pytoul"
        self.assertEqual(tm.convert_to_cxx(), code, tm.convert_to_cxx())


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testINit']
    unittest.main()