from setuptools import setup, find_packages
from os.path import join

version = open(join('Products', 'ImageEditor', 'version.txt')).read()
readme = open("README.txt").read()
history = open(join('docs', 'HISTORY.txt')).read()

setup(name = 'Products.ImageEditor',
      version = version,
      description = 'A product that adds an "image editor" link and tab to '
        '"Image" and "News Item" content allowing the user to rotate, flip, '
        'blur, compress, change contrast & brightness, sharpen, add drop '
        'shadows, crop, resize an image, save as, and apply sepia.',
      long_description = readme + '\n' + history,
      classifiers = [
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='plone image editor rotate flip blur compress contrast '
        'brightness sharpen drop shadows crop resize save as sepia',
      author = 'Nathan Van Gheem',
      author_email = 'vangheem@gmail.com',
      url = 'http://www.plone.org/products/products-imageeditor',
      license = 'GPL',
      packages = find_packages(exclude=['ez_setup']),
      namespace_packages = ['Products'],
      include_package_data = True,
      zip_safe = False,
      install_requires = [
        'setuptools',
        'collective.js.jquery',
        'collective.js.jqueryui',
      ],
      extras_require = { 'test': [
        'collective.testcaselayer',
      ]},
      entry_points = '''
        [z3c.autoinclude.plugin]
        target = plone
      ''',
)
