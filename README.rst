Introduction
============

.. image:: https://secure.travis-ci.org/collective/Products.ImageEditor.png?branch=master
    :alt: Travis CI badge
    :target: http://travis-ci.org/collective/Products.ImageEditor

.. image:: https://coveralls.io/repos/collective/Products.ImageEditor/badge.png?branch=master
    :alt: Coveralls badge
    :target: https://coveralls.io/r/collective/Products.ImageEditor

Once installed this product adds a "Image Editor" link near the image widget. 
It also provides an Image Editor Button.

Features
--------

* rotate
* flip
* blur
* compress
* contrast
* brightness
* sharpen
* add drop shadows
* crop
* resize
* sepia
* save as another content type.

Dependencies
------------

* collective.js.jqueryui


Installation
------------

*WARNING*

Products.ImageEditor depends on collective.js.jqueryui. The 
collective.js.jqueryui package changes quite often and those
changes frequently break Products.ImageEditor. Please read
the documentation on collective.js.jqueryui to make sure you're
installing the correct version for the plone you're running.
Depending on your setup, you might have to install collective.js.jqueryui
version 1.7, 1.8, 1.9 or 1.10. And depending on those choices,
you might also have to upgrade plone.app.jquery.

Don't blame me for this...


Editor Storage
--------------

By default, ImageEditor uses sessions to store the image data.
Since 2.0, it has support for beaker storage. 

To use beaker storage, add beaker to your eggs in buildout::

    [eggs]
    ...
    beaker
    ...

Then, add environment variables to set the beaker settings::

    BEAKER_CACHE_TYPE file
    BEAKER_CACHE_DATA_DIR /path/to/data
    BEAKER_CAHCE_LOCK_DIR /path/to/lock

The environment variables can be set using the `environment-vars`
option in plone.recipe.zope2instance buildout configuration.

Diazo
-----

The following rule in rules.xml will be useful, most likely::

    <!-- ImageEditor -->
    <notheme css:if-content="#image-editor-controls" />


Contributors
------------
* Andreas Zeidler
* Jean-Michel FRANCOIS
* Davi Lima
* Sylvain Boureliou
* Jeff Kunce
* Hector Velarde
