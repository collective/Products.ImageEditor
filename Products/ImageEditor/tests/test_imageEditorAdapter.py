from Products.ImageEditor.tests.base import ImageEditorTestCase
from Products.ImageEditor.actions import *

class TestAdapter(ImageEditorTestCase):
    """
    Test the edit actions on images
    """
        
    def test_undo(self):
        editor = self.getImageEditorAdapter()
        
        original_image = editor.get_current_image_data()
        RotateRightAction(editor.context)()
        self.failUnless(original_image != editor.get_current_image_data())
        
        editor.undo()
        self.failUnless(original_image == editor.get_current_image_data())
        
    def test_redo(self):
        editor = self.getImageEditorAdapter()
        
        original_image = editor.get_current_image_data()

        RotateRightAction(editor.context)()
        edited_image = editor.get_current_image_data()
        self.failUnless(original_image != edited_image)
        
        editor.undo()
        self.failUnless(original_image == editor.get_current_image_data())
        
        editor.redo()
        self.failUnless(edited_image == editor.get_current_image_data())
        
    def test_clear_edits(self):
        editor = self.getImageEditorAdapter()
        
        original_image = editor.get_current_image_data()
        
        RotateRightAction(editor.context)()
        RotateRightAction(editor.context)()
        RotateRightAction(editor.context)()
        
        editor.clear_edits()
        self.failUnless(original_image == editor.get_current_image_data())
        
    def test_save_edits(self):
        editor = self.getImageEditorAdapter()
        
        RotateRightAction(editor.context)()
        RotateRightAction(editor.context)()
        
        current = editor.get_current_image_data()
        editor.save_edit()
        
        self.failUnless(len(editor.stack) == 1)
        self.failUnless(current == editor.get_current_image_data())
        
    def test_get_current_image_info(self):
        editor = self.getImageEditorAdapter()
        info = editor.get_current_image_info()

        self.failUnless(info['sizeformatted'] == "Size: 25.00kb")
        self.failUnless(info['width'] == 461)
        self.failUnless(info['height'] == 614)
        self.failUnless(info['size'] == 25)
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestAdapter))
    
    return suite