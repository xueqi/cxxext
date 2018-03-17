import sys
sys.path.append("/home/xueqi/Documents/LiClipse Workspace/cxxext/src")
import os
relion_src = "/home/src/relion"
# basic class to build
cls_build = [("MyOptimiser", 'MlOptimiser', "src/ml_optimiser.h")]
from class_builder import ClassBuilder

builder = ClassBuilder()
builder.add_include_dir(relion_src)
builder.add_include_dir(os.path.join(relion_src, "external", "fftw", "include"))
output_dir = "py_relion"
try:
    os.mkdir(output_dir)
except OSError as err:
    if err.errno == 17:
        pass
for py_cls, cxx_cls, header_file in cls_build:
    h_file_name = builder.convert_cxx_to_python(os.path.join(relion_src, header_file), cxx_cls, output_dir)
