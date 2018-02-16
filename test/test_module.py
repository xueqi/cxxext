'''
Created on Feb 16, 2018

@author: xueqi
'''
import unittest


class TestImport(unittest.TestCase):

    def testImport(self):
        from clang.cindex import Index
        a = Index.create()
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'TestImport.testImport']
    unittest.main()