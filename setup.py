from setuptools import setup, find_packages
import os
from xml.dom import minidom

dependencies = [
    'setuptools'
]

#now get plone dependencies
dependencies.extend([d.strip('\n').strip() for d in open(os.path.join('Products', 'ImageEditor', 'dependencies.txt')).readlines() ])

setup(name='Products.ImageEditor',
      version=open(os.path.join("Products", "ImageEditor", "version.txt")).read(),
      description="A product that adds an editor tab to ATImage and News Item so you can rotate, flip, blur, compress, contrast, brightness, sharpen, add drop shadows, crop, resize an image.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='atimage plone image rotate flip blur compress contrast brightness sharpen drop shadows crop resize',
      author='Nathan Van Gheem',
      author_email='vangheem@gmail.com',
      url='http://plone.org/products/atimageeditor',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=dependencies,
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
