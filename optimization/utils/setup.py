from distutils.core import setup, Extension

module = Extension("myModule", sources=["utils.c"])

setup(name="DistanceMath",
      version=1.0,
      description="For distance math",
      ext_modules=[module])
