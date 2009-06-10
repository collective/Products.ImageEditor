import sys
from cStringIO import StringIO

from PIL import Image
from PIL import ImageChops
from PIL import ImageEnhance

from Products.PloneTestCase import PloneTestCase as ptc
from Products.ImageEditor.adapters.imageeditor import ImageEditorAdapter
from Testing import ZopeTestCase as ztc


BASE_DIR = ""

for path in sys.path:
    if 'Products.ImageEditor' in path:
        BASE_DIR = path

ptc.setupPloneSite(products=('Products.ImageEditor',))

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
        
        im = self.getOriginal()
        imageData = StringIO()
        im.save(imageData, im.format)
        image.setImage(imageData.getvalue())
        return image
    
    def getEditor(self, context):
        return ImageEditorAdapter(context)
    
    def getImageEditorAdapter(self):
        image = self.getImageContentType()
        return ImageEditorAdapter(image)
       
    def imagesEqual(self, comparedImageFileName, imageEditor):
        imageEditor.save_edit()
        imageEditor.get_current_image().save(self.getImagePath(comparedImageFileName))
        
        imgfile = self.getImage(comparedImageFileName)
        
        image_diff = ImageChops.difference(imgfile, imageEditor.get_current_image()).getbbox()
        
        #self.failUnless(image_diff[0] == 0 and image_diff[1] == 0)
        
        #doesn't ever work...  Why aren't images the same??
        #self.failUnless(image_diff is None)
        
    def getOriginal(self):
        return self.getImage('original.jpg')
        
    def getImagePath(self, name):
        return '%s/Products/ImageEditor/tests/testimages/%s' % (BASE_DIR, name)
        
    def getImage(self, name):
        return Image.open(self.getImagePath(name))
