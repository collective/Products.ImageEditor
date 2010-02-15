from setuptools import setup, find_packages
import os

setup(name='Products.ImageEditor',
      version='1.2',
      description="A product that adds an image editor tab to ATImage and News Item "
                  "so you can rotate, flip, blur, compress, contrast, brightness, "
                  "sharpen, add drop shadows, crop, resize an image, save as, and apply sepia.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone image editor rotate flip blur compress contrast brightness '
               'sharpen drop shadows crop resize save as sepia',
      author='Nathan Van Gheem',
      author_email='vangheem@gmail.com',
      url='http://www.plone.org/products/products-imageeditor',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'collective.js.jquery',
        'collective.js.jqueryui'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
