'''
Created on Feb 16, 2018

@author: xueqi
'''
import os
import glob
import unittest
from class_builder import ClassBuilder

class TestCompile(unittest.TestCase):

    def testCompile(self):
        test_dir = os.path.join(os.path.dirname(__file__), "test_data", "compile")
        cwd = os.getcwd()
        os.chdir(test_dir)
        # create the builder
        builder = ClassBuilder()
        builder.add_include_dir(os.getcwd())
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        # compile the code
        import distutils.ccompiler as ccc
        import sysconfig
        c = ccc.new_compiler()
        # add include dir
        c.add_include_dir(sysconfig.get_paths()['include'])
        c.add_include_dir(os.getcwd())
        for fname in glob.glob("*.h"):
            classname = os.path.basename(os.path.splitext(fname)[0]).upper()
            # create 
            builder.convert_cxx_to_python(fname, classname, output_dir)
            os.chdir(output_dir)
            c.compile(["%s_type.cpp" % classname])
            os.chdir("..")
        os.chdir(cwd)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()