from distutils.core import setup, Extension

module = Extension("myModule", sources=["color_math.c"])

setup(name="ColorMath",
      version=1.0,
      description="For color math",
      ext_modules=[module])
