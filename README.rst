Introduction
============
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


Contributors
------------
* Andreas Zeidler
* Jean-Michel FRANCOIS
* Davi Lima
* Sylvain Boureliou
* Jeff Kunce
* Hector Velarde
