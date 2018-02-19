'''
Created on Feb 16, 2018

@author: xueqi
'''
import os
from type_class import TypeClass

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
        
    def convert_cxx_to_python(self, fname, classname, output_dir):
        # convert a cxx class to python
        if self.index is None:
            from clang.cindex import Index
            self.index = Index.create()
        args = ['-x', 'c++-header', '-std=c++11']
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
                    all_classes[cls_name].update(cls)
        return all_classes
    
    def get_class(self, cu, cls=None):
        """ parse the class, get all members and methods
        """
        from clang.cindex import CursorKind as CK, AccessSpecifier as AS
        from type_member import TypeMember
        result = cls
        if result is None:
            result = TypeClass(cu.spelling)
        for child in cu.get_children():
            if child.kind == CK.FIELD_DECL:
                if not child.access_specifier == AS.PUBLIC:
                    print child.access_specifier, child.type.spelling, child.spelling
                    continue
                # skip all template for now.:TODO: put it back
                if "<" in child.type.spelling:
                    print("Template not supported yet", child.type.spelling, child.spelling)
                    continue
                # and remove all namespace for now
                if len(child.type.spelling.split("::")) > 1:
                    print("namespace not support yet. Use basetype.", child.type.spelling)
                tp = child.type.spelling.split("::")[-1]
                result.members.append(
                    TypeMember(child.spelling, tp)
                    )
        return result
        