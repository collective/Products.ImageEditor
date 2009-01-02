import unittest
from Products.ImageEditor.tests.base import ImageEditorTestCase
from Products.CMFCore.utils import getToolByName
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from zope.component import getUtility
from Products.ImageEditor.adapters.unredostack import UnredoStack
from cStringIO import StringIO

class TestUnredoStack(ImageEditorTestCase):
    """
    
    """
    
    def getUnredoAdapter(self):
        id = self.portal.invokeFactory(type_name="Image", id="testimage")
        image = self.portal['testimage']
        image.setTitle('test')
        
        im = self.getOriginal()
        imageData = StringIO()
        im.save(imageData, im.format)
        image.setImage(imageData.getvalue())
        
        return UnredoStack(image)
        
    def test_should_get_current_item_on_stack(self):
        unredo = self.getUnredoAdapter()
        
        self.failUnless(unredo.getCurrent() == unredo.image.data)
        
    def test_should_add_to_stack(self):
        editor = self.getImageEditorAdapter()
        
        editor.dropshadow()
        
        #starts from pos 0
        self.failUnless(editor.unredo.pos == 1)
        
    def test_should_be_able_to_undo(self):
        editor = self.getImageEditorAdapter()
        
        editor.dropshadow()
        
        self.failUnless(editor.unredo.canUndo())
        
    def test_should_not_be_able_undo(self):
        editor = self.getImageEditorAdapter()
        
        self.failUnless(not editor.unredo.canUndo())
        
    def test_undo_should_go_back_to_previous_edit(self):
        editor = self.getImageEditorAdapter()
        editor.dropshadow()
        editor.unredo.undo()
        self.failUnless(editor.unredo.getCurrent() == editor.image.data)
        
    def test_should_redo(self):
        editor = self.getImageEditorAdapter()
        editor.dropshadow()
        current_data = editor.unredo.getCurrent()
        editor.unredo.undo()
        editor.unredo.redo()
        self.failUnless(editor.unredo.getCurrent() == current_data)
        
    def test_canRedo_evaluates_correctly(self):
        editor = self.getImageEditorAdapter()
        editor.dropshadow()
        current_data = editor.unredo.getCurrent()
        editor.unredo.undo()
        self.failUnless(editor.unredo.canRedo())
        
    def test_canRedo_should_not_work(self):
        editor = self.getImageEditorAdapter()
        editor.dropshadow()
        current_data = editor.unredo.getCurrent()
        self.failUnless(not editor.unredo.canRedo())
        
    def test_clearStack_should_go_back_to_original_image(self):
        editor = self.getImageEditorAdapter()
        editor.dropshadow()
        editor.dropshadow()
        editor.dropshadow()
        editor.dropshadow()
        editor.unredo.clearStack()
        self.failUnless(editor.unredo.getCurrent() == editor.image.data)
        
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestUnredoStack))
    return suite