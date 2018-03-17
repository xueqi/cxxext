'''
Created on Feb 16, 2018

@author: xueqi
'''
import os
from type_class import TypeClass
from type_method import TypeMethod
from ctypes import *
from wrapper import *
from clang.cindex import TypeKind
TYPES = {"int" : c_int,
         "long" : c_int,
         "char **": LP_LP_c_char,
         "char *": LP_c_char,
         "double" : c_double,
         "bool" : c_bool,
         "char" : c_char,
         "float" : c_float,
         "long" : c_long,
         "unsigned int": c_uint,
         "short" : c_short,
         "unsigned long long" : c_ulonglong,
         "long long" : c_longlong,
         "unsigned long" : c_ulong}

class ClassBuilder(object):
    """ Build cpp files for extensions of a class
    """
    def __init__(self):
        self.index = None
        self.include_dirs = []
        self.add_include_dir(os.path.join(os.path.dirname(__file__), "include"))

    def add_include_dir(self, d):
        if not os.path.exists(d): return
        self.include_dirs.append(d)
    
    def parse(self, cxxfile):
        if self.index is None:
            from clang.cindex import Index
            self.index = Index.create()        
        args = ['-xc++-header', '-std=c++11']
        for inc_dir in self.include_dirs:
            args.append("-I%s" % inc_dir)
        tu = self.index.parse(cxxfile, args)
        return tu
    
    def convert_cxx_to_python(self, fname, classname, output_dir):
        # convert a cxx class to python
        if self.index is None:
            from clang.cindex import Index
            self.index = Index.create()
        args = ['-xc++-header', '-std=c++11']
        for inc_dir in self.include_dirs:
            args.append("-I%s" % inc_dir)
        tu = self.index.parse(fname, args)
        # get all classes
        classes = self.get_all_classes(tu.cursor)
        
        if not classname in classes:
            raise Exception("No class built")
        tc = classes[classname]
        cpp_file_name = os.path.join(output_dir, tc.cpp_file)
        h_file_name = os.path.join(output_dir, tc.header_file)
        open(cpp_file_name, 'w').write(tc.create_cpp_file())
        open(h_file_name, 'w').write(tc.create_header_file(fname))
        return h_file_name
    
    def get_all_classes(self, start):
        """ Get all classes from tu, and return a dict containing the classes
        """
        from clang.cindex import CursorKind as CK
        all_classes = {}
        for cu in start.get_children():
            if cu.kind == CK.CLASS_DECL:
                cls_name = cu.spelling
                cls = self.get_class(cu)
                if not cls_name in all_classes:
                    all_classes[cls_name] = cls
                else:
                    if sizeof(all_classes[cls_name]) < sizeof(cls):
                        all_classes[cls_name] = cls
        print all_classes.keys()
        print TYPES.keys()
        return all_classes

    
    def get_type(self, clang_type, type_name=None):
        """ Return ctype, construct with type_name
        """
        if type_name is None:
            type_name = clang_type.spelling
        if type_name in TYPES:
            return TYPES[type_name]
        if clang_type.kind == TypeKind.ELABORATED:
            return self.get_type(clang_type.get_named_type(), type_name)
        if clang_type.kind == TypeKind.TYPEDEF:
            return self.get_type(clang_type.get_declaration().underlying_typedef_type)

        if clang_type.kind == TypeKind.UNEXPOSED or clang_type.kind == TypeKind.RECORD:
            tp = self.get_class(clang_type.get_declaration(), cls_name=type_name)
            TYPES[type_name] = tp
            return tp
        if clang_type.kind == TypeKind.POINTER:
            # TODO: Do we need the derefed type?
            return c_void_p 
        if clang_type.kind == TypeKind.ENUM:
            return c_int
        
        elif clang_type.kind == TypeKind.CONSTANTARRAY:
            base_type = clang_type.element_type
            base_count = clang_type.element_count
            if base_type.spelling in TYPES:
                tp = TYPES[base_type.spelling] * base_count
                TYPES[type_name] = tp
                return tp
        print clang_type.spelling, clang_type.kind, type_name
        raise
    
    def get_class(self, cls_cu, cls_name=None):
        """ parse the class, return as subclass of ctypes.Structure
        """
        from clang.cindex import CursorKind as CK
        if cls_name == None:
            cls_name = cls_cu.spelling
        print "Parsing class %s" % cls_name
        cls = new_struct(cls_name)
        _fields_ = []
        for child in cls_cu.get_children():
            if child.kind == CK.FIELD_DECL:
                sz = child.type.get_size()
                cld_type = self.get_type(child.type)
                cld_name = child.spelling
                _fields_.append((cld_name, cld_type))
            elif child.kind == CK.CXX_METHOD:
                #print child.spelling, child.type.spelling
                # parse methods.
                #method = self.get_method(child)
                #result.methods.append(method)
                pass
            else:
                print child.kind, child.type.spelling
        cls._fields_ = _fields_
        print cls, sizeof(cls)
        return cls
    
    def get_method(self, method_cu, cls=None):
        """ Parse the method cursor and return a type method
        :param method_cu: The cursor for a method
        :param cls: The class that the method belongs to
        """
        rtn_type = method_cu.result_type.spelling
        func_name = method_cu.spelling

        args = []
        for child in method_cu.get_children():
            if child.type.spelling:
                args.append((child.spelling, child.type.spelling))
        
        kwargs = {}
        type_meth = TypeMethod(func_name, rtn_type, args, kwargs, cls=cls)
        return type_meth

# Test
if __name__ == "__main__":
    builder = ClassBuilder()
    builder.add_include_dir("/home/src/relion")
    builder.add_include_dir("/home/src/relion/external/fftw/include")
    start = builder.parse("/home/src/relion/src/ml_optimiser.h")
    from pprint import pprint
    builder.get_all_classes(start.cursor)
    #pprint([vars(_) for _ in builder.get_all_classes(start.cursor)['MlOptimiser'].members])
    