'''
Created on Feb 16, 2018

@author: xueqi
'''
import os
import glob
import unittest
from class_builder import ClassBuilder

class TestCompile(unittest.TestCase):
    
    def test_compile_type_convert(self):
        test_dir = os.path.join(os.path.dirname(__file__), "test_data", "compile")
        cwd = os.getcwd()
        src_dir = os.path.join(test_dir, "..", "..", "..", "src/cxx_src")
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
        for path in builder.include_dirs:
            c.add_include_dir(path)
        for fname in [os.path.join(src_dir, 'type_convert.cpp')]:
            # create 
            os.chdir(output_dir)
            # supress the const char* to char* warning. This is ok in c, but not c++
            ext_args = ['-fPIC', '-Wno-write-strings', '-o%s.o' % os.path.basename(os.path.splitext(fname)[0])]
            c.compile([fname], output_dir=test_dir, extra_preargs=ext_args, extra_postargs=ext_args)
            os.chdir("..")
        # test the functions
        
        os.chdir(cwd)
    
    def make_lib(self, srcs, libname):
        pass
    
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
        c = ccc.new_compiler(verbose=2, force=1)
        # add include dir
        c.add_include_dir(sysconfig.get_paths()['include'])
        c.add_include_dir(os.getcwd())
        for path in builder.include_dirs:
            c.add_include_dir(path)
        clses = []
        headers = []
        objs = []
        for fname in glob.glob("*.h"):
            classname = os.path.basename(os.path.splitext(fname)[0]).upper()
            if len(classname) > 1:
                classname = "MlOptimiser"
                #continue
            clses.append(classname)
            # create 
            h_file_name = builder.convert_cxx_to_python(fname, classname, output_dir)
            headers.append(h_file_name)
            os.chdir(output_dir)
            # supress the const char* to char* warning. This is ok in c, but not c++
            ext_args = ['-Wno-write-strings', '-fPIC']
            c.compile(["%s_type.cpp" % classname], extra_preargs=ext_args, extra_postargs=ext_args)
            objs.append("%s/%s_type.o" % (output_dir, classname))
            os.chdir("..")
            c.compile([fname.replace(".h", ".cpp")], extra_preargs=ext_args, extra_postargs=ext_args)
            objs.append(fname.replace(".h", ".o"))
        # make module ltest
        objs.append("output/type_convert.o")
        module_name = "ltest"
        with open("test_module.cpp", "w") as f:
            f.write("#include <Python.h>\n#include <iostream>\n")
            # add all types
            for header in headers:
                f.write('#include "%s"\n' % header)
            # add the init function
            f.write("""PyMODINIT_FUNC
initltest(void) {
    PyObject *m;
    m = Py_InitModule3("ltest", NULL, "ltest module");
    if (m == NULL) return;
    // add all types
""")
            # add all types
            for cls in clses:
                f.write("""    if (PyType_Ready(&{cls}Type) < 0) {{
        std::cerr << "Could not import {cls}Type" << std::endl;
    }}
    Py_INCREF(&{cls}Type);
    PyModule_AddObject(m, "{cls}", (PyObject *)&{cls}Type);
""".format(cls=cls))
            f.write("}\n")
        
        # compile the module
        c.compile(["test_module.cpp"], extra_preargs=ext_args, extra_postargs=ext_args)
        objs.append("test_module.o")
        # link to a python lib
        print objs
        c.link_shared_object(objs,
                            "ltest.so",
                            libraries = ["stdc++"]  )
        print os.getcwd()
        import sys
        sys.path.append(".")
        import ltest
        print ltest.A
        a = ltest.A()
        print dir(a)
        print ["func test", a.func_b(1, 3.2)]
        os.chdir(cwd)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()