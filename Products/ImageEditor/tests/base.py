import unittest
import sys
from cStringIO import StringIO

from PIL import Image
from PIL import ImageChops
from PIL import ImageEnhance

from Products.ImageEditor.adapters.imageeditor import ImageEditorAdapter

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup
from Products.CMFCore.utils import getToolByName

from zope.app import zapi
from zope.configuration import xmlconfig

BASE_DIR = ""

for path in sys.path:
    if 'Products.ImageEditor' in path:
        BASE_DIR = path

import Products.ImageEditor, collective.js.jqueryui, collective.js.jquery

@onsetup
def setUp():
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', Products.ImageEditor)
    zcml.load_config('configure.zcml', collective.js.jquery)
    zcml.load_config('configure.zcml', collective.js.jqueryui)
    fiveconfigure.debug_mode = False
    ztc.installProduct('ImageEditor')
    ztc.installPackage('collective.js.jquery')
    ztc.installPackage('collective.js.jqueryui')

setUp()

ptc.setupPloneSite(extension_profiles=('Products.ImageEditor:default',))

class ImageEditorTestCase(ptc.PloneTestCase):
    """
    """
    def afterSetUp(self):
        self.setRoles(('Manager',))
        
    def getImageContentType(self):
        try:
            id = self.portal.invokeFactory(type_name="Image", id="testimage")
        except Exception:
            id = 'testimage'
        image = self.portal[id]
        image.setTitle('test')
        #(Pdb) p context.getField('image').get(context)
        #<Image at /plone/bug-mantis-01.png/image>
        #(Pdb) p context.getField('image').get(context).data
        #<OFS.Image.Pdata object at 0xb277db6c>
        #(Pdb) p context.getField('image').get(context).data.data
        #'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x04N\x00\x00...
        #...
        #
        #In testcase:
        #(Pdb) image.getField('image').get(image)                                                                         
        #<Image at /plone/testimage/image>                                                                                
        #(Pdb) image.getField('image').get(image).data                                                                    
        #'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\...
        im = self.getOriginal()
        imageData = StringIO()
        im.save(imageData, im.format)
        image.setImage(imageData)
        return image
    
    def uninstall(self):
        setup_tool = getToolByName(self.portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-Products.ImageEditor:uninstall')
    
    def getEditor(self, context):
        return ImageEditorAdapter(context)
    
    def getImageEditorAdapter(self):
        image = self.getImageContentType()
        return ImageEditorAdapter(image)
               
    def getOriginal(self):
        return self.getImage('original.jpg')
        
    def getImagePath(self, name):
        return '%s/Products/ImageEditor/tests/testimages/%s' % (BASE_DIR, name)
        
    def getImage(self, name):
        return Image.open(self.getImagePath(name))
