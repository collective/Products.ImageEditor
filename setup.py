from setuptools import setup, find_packages
import os

version = '1.0rc1'

setup(name='Products.ImageEditor',
      version=version,
      description="A product that adds an editor tab to ATImage so you can crop and resize an image",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='atimage image resize scrop rotate',
      author='Nathan Van Gheem',
      author_email='vangheem@gmail.com',
      url='http://plone.org/products/atimageeditor',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
