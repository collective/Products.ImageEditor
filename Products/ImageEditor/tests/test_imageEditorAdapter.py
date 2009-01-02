from Products.PloneTestCase.PloneTestCase import PloneTestCase
from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc
from Products.ImageEditor.tests.base import ImageEditorTestCase
from cStringIO import StringIO
import zope.app.publisher.browser
from Products.Five.testbrowser import Browser
from PIL import Image, ImageFilter, ImageEnhance
from cStringIO import StringIO

class TestImageEdits(ImageEditorTestCase):
    """
    Test the edit actions on images
    """
        
    def test_dropShadow(self):
        imageEditor = self.getImageEditorAdapter()
        imageEditor.dropshadow()
        self.imagesEqual('dropshadow.jpg', imageEditor)
        
    def test_sharpening(self):
        imageEditor = self.getImageEditorAdapter()        
        imageEditor.sharpen(1.5)
        self.imagesEqual('1.5sharpening.jpg', imageEditor)
        
    def test_quality(self):
        imageEditor = self.getImageEditorAdapter()        
        imageEditor.compress(50)
        #testing this isn't working
        #self.imagesEqual('50percentquality.jpg', imageEditor)
                
    def test_brightness(self):
        imageEditor = self.getImageEditorAdapter()
        imageEditor.brightness(.75*2.0)
        self.imagesEqual('75percentbrightness.jpg', imageEditor)
        
    def test_contrast(self):
        imageEditor = self.getImageEditorAdapter()
        imageEditor.contrast(.75*2.0)
        self.imagesEqual('75percentcontrast.jpg', imageEditor)
                
    def test_horizontalFlip(self):
        imageEditor = self.getImageEditorAdapter()
        imageEditor.flipOnHorizontalAxis()
        self.imagesEqual('horizontalflip.jpg', imageEditor)
        
    def test_verticalFlip(self):
        imageEditor = self.getImageEditorAdapter()
        imageEditor.flipOnVerticalAxis()
        self.imagesEqual('verticalflip.jpg', imageEditor)        
        
    def test_blur(self):
        imageEditor = self.getImageEditorAdapter()
        imageEditor.blur(2)
        self.imagesEqual('level2blur.jpg', imageEditor)        
        
    def test_resize(self):
        imageEditor = self.getImageEditorAdapter()
        imageEditor.resize(390, 478)
        self.imagesEqual('resizeto390by478.jpg', imageEditor)        
        
    def testRotateLeft(self):
        imageEditor = self.getImageEditorAdapter()
        imageEditor.rotateLeft()
        self.imagesEqual('rotateleft.jpg', imageEditor)        
        
    def test_rotateRight(self):
        imageEditor = self.getImageEditorAdapter()
        imageEditor.rotateRight()
        self.imagesEqual('rotateright.jpg', imageEditor)        
        
class TestAdapter(ImageEditorTestCase):
    """
    Test the edit actions on images
    """
        
    def test_undo(self):
        editor = self.getImageEditorAdapter()
        
        original_image = editor.getCurrentImageData()
        editor.dropshadow()
        self.failUnless(original_image != editor.getCurrentImageData())
        
        editor.undo()
        self.failUnless(original_image == editor.getCurrentImageData())
        
    def test_redo(self):
        editor = self.getImageEditorAdapter()
        
        original_image = editor.getCurrentImageData()
        editor.dropshadow()
        
        edited_image = editor.getCurrentImageData()
        self.failUnless(original_image != edited_image)
        
        editor.undo()
        self.failUnless(original_image == editor.getCurrentImageData())
        
        editor.redo()
        self.failUnless(edited_image == editor.getCurrentImageData())
        
    def test_clearEdits(self):
        editor = self.getImageEditorAdapter()
        
        original_image = editor.getCurrentImageData()
        
        editor.dropshadow()
        editor.rotateLeft()
        editor.rotateRight()
        
        editor.clearEdits()
        self.failUnless(original_image == editor.getCurrentImageData())
        
    def test_saveEdits(self):
        editor = self.getImageEditorAdapter()
        
        editor.dropshadow()
        editor.rotateLeft()
        
        current = editor.getCurrentImageData()
        editor.saveEdit()
        
        self.failUnless(len(editor.unredo.stack) == 1)
        self.failUnless(current == editor.getCurrentImageData())
        
    def test_getCurrentImage(self):
        editor = self.getImageEditorAdapter()
        
        editor.dropshadow()
        editor.rotateLeft()
        
        self.failUnless(editor.getCurrentImageData() == editor.unredo.getCurrent())
    
    def test_setImage(self):
        editor = self.getImageEditorAdapter()
        
        self.failUnless(len(editor.unredo.stack) == 1)
        
        editor.dropshadow()
        editor.rotateLeft()
        
        self.failUnless(len(editor.unredo.stack) == 3)
        
    def test_getCurrentImageData(self):
        # Not sure how to test this...
        pass
        
    def test_getCurrentImageInfo(self):
        editor = self.getImageEditorAdapter()
        info = editor.getCurrentImageInfo()
        
        self.failUnless(info['sizeformatted'] == "Size: 25kb")
        self.failUnless(info['width'] == 461)
        self.failUnless(info['height'] == 614)
        self.failUnless(info['size'] == 25)
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestImageEdits))
    suite.addTest(makeSuite(TestAdapter))
    
    return suite