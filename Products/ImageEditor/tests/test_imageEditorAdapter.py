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

class TestAdapter(ImageEditorTestCase):
    """
    Test the edit actions on images
    """
        
    def test_undo(self):
        editor = self.getImageEditorAdapter()
        
        original_image = editor.get_current_image_data()
#        editor.dropshadow()
        self.failUnless(original_image != editor.get_current_image_data())
        
        editor.undo()
        self.failUnless(original_image == editor.get_current_image_data())
        
    def test_redo(self):
        editor = self.getImageEditorAdapter()
        
        original_image = editor.get_current_image_data()
#        editor.dropshadow()
        
        edited_image = editor.get_current_image_data()
        self.failUnless(original_image != edited_image)
        
        editor.undo()
        self.failUnless(original_image == editor.get_current_image_data())
        
        editor.redo()
        self.failUnless(edited_image == editor.get_current_image_data())
        
    def test_clear_edits(self):
        editor = self.getImageEditorAdapter()
        
        original_image = editor.get_current_image_data()
        
#        editor.dropshadow()
#        editor.rotateLeft()
#        editor.rotateRight()
        
        editor.clear_edits()
        self.failUnless(original_image == editor.get_current_image_data())
        
    def test_save_edits(self):
        editor = self.getImageEditorAdapter()
        
#        editor.dropshadow()
#        editor.rotateLeft()
        
        current = editor.get_current_image_data()
        editor.save_edit()
        
        self.failUnless(len(editor.stack) == 1)
        self.failUnless(current == editor.get_current_image_data())
        
    def test_get_current_image(self):
        editor = self.getImageEditorAdapter()
        
#        editor.dropshadow()
#        editor.rotateLeft()
#        
#        self.failUnless(editor.get_current_image_data() == editor.get_current())
    
    def test_setImage(self):
        editor = self.getImageEditorAdapter()
        
        self.failUnless(len(editor.stack) == 1)
        
#        editor.dropshadow()
#        editor.rotateLeft()
#        
        self.failUnless(len(editor.stack) == 3)
        
    def test_get_current_image_data(self):
        # Not sure how to test this...
        pass
        
    def test_get_current_image_info(self):
        editor = self.getImageEditorAdapter()
        info = editor.get_current_image_info()
        
        self.failUnless(info['sizeformatted'] == "Size: 25kb")
        self.failUnless(info['width'] == 461)
        self.failUnless(info['height'] == 614)
        self.failUnless(info['size'] == 25)
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestAdapter))
    
    return suite