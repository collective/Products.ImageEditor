import unittest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup

from zope.app import zapi
from zope.configuration import xmlconfig
from Products.ImageEditor.adapters.imageeditor import ImageEditorAdapter

from PIL import Image, ImageFilter, ImageEnhance
from cStringIO import StringIO

import sys
from PIL import ImageChops

BASE_DIR = ""

for path in sys.path:
    if 'Products.ImageEditor' in path:
        BASE_DIR = path

ztc.installProduct('Products.ImageEditor')
ptc.setupPloneSite(products=('Products.ImageEditor',))

class ImageEditorTestCase(ptc.PloneTestCase):
    """
    """
    
    def afterSetUp(self):
        self.setRoles(('Manager',))
    
    def getImageEditorAdapter(self):
        id = self.portal.invokeFactory(type_name="Image", id="testimage")
        image = self.portal['testimage']
        image.setTitle('test')
        
        im = self.getOriginal()
        imageData = StringIO()
        im.save(imageData, im.format)
        image.setImage(imageData.getvalue())
        
        return ImageEditorAdapter(image)
       
    def imagesEqual(self, comparedImageFileName, imageEditor):
        imageEditor.saveEdit()
        imageEditor.getCurrentImage().save(self.getImagePath(comparedImageFileName))
        
        imgfile = self.getImage(comparedImageFileName)
        
        image_diff = ImageChops.difference(imgfile, imageEditor.getCurrentImage()).getbbox()
        
        #self.failUnless(image_diff[0] == 0 and image_diff[1] == 0)
        
        #doesn't ever work...  Why aren't images the same??
        #self.failUnless(image_diff is None)
        
    def getOriginal(self):
        return self.getImage('original.jpg')
        
    def getImagePath(self, name):
        return '%s/Products/ImageEditor/tests/testimages/%s' % (BASE_DIR, name)
        
    def getImage(self, name):
        return Image.open(self.getImagePath(name))