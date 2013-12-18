# -*- coding:utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '3.1.0.dev0'
long_description = (
    open('README.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(name='Products.ImageEditor',
      version=version,
      description='adds a "Image Editor" link near the image widget '
        ' allowing the user to rotate, flip, '
        'blur, compress, change contrast & brightness, sharpen, add drop '
        'shadows, crop, resize an image, save as, and apply sepia.',
      long_description=long_description,
      classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Plone :: 4.0",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='plone image editor rotate flip blur compress contrast '
        'brightness sharpen drop shadows crop resize save as sepia',
      author='Nathan Van Gheem',
      author_email='vangheem@gmail.com',
      url='http://www.plone.org/products/products-imageeditor',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'collective.js.jqueryui',
          'plone.i18n',
          'plone.memoize',
          'plone.registry',
          'Products.Archetypes',
          'Products.ATContentTypes',
          'Products.CMFCore',
          'Products.GenericSetup',
          'setuptools',
          'zope.component',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.schema',
      ],
      extras_require={'test': [
          'collective.testcaselayer',
          'plone.api',
          'plone.app.testing',
          'plone.browserlayer',
          'plone.testing',
          'Products.PloneTestCase',
          'Testing.ZopeTestCase',
          'unittest2',
      ]},
      entry_points='''
        [z3c.autoinclude.plugin]
        target = plone
      ''',
)
