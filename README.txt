Introduction
============
Once installed this product adds a "Image Editor" tab for the image content type and News Item content type.

Features
========

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

Roadmap / Proposal
==================

* Categorize actions (effects, transformations, colors)

Dependencies
============

* collective.js.jquery
* collective.js.jqueryui

Suggestions
===========

This product depends on collective.js.jqueryui which is great, but not always required on every page load. If you'd like to speed up the page loads of other pages that do not need the extra javascript, you can add this condition, `here.restrictedTraverse('@@image-editor-utility').should_include(request)`, to the jqueryui js entry in portal_javascripts.

Contributors
============
* Andreas Zeidler
* Jean-Michel FRANCOIS
* Davi Lima
* Sylvain Boureliou
* Jeff Kunce
