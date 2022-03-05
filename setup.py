from distutils.core import setup, Extension
from Cython.Build import cythonize
from numpy import get_include


ext = Extension("badapple_convert", sources=["badapple_convert.pyx"], include_dirs=['.', get_include()])
setup(name="badapple_convert", ext_modules=cythonize([ext]))