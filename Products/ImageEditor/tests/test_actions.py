import unittest
from Products.ImageEditor.tests import base
from Products.ImageEditor.actions.actions import *

class TestActions(base.ImageEditorTestCase):
    """Test Actions"""
    def afterSetUp(self):
        super(TestActions, self).afterSetUp()
        self.image = self.getImageContentType()
        
    def beforeTearDown(self):
        parent = self.image.getParentNode()
        parent.manage_delObjects([self.image.getId()])

    def test_crop(self):
        action = CropAction(self.image)
        x1, y1, x2, y2 = 0, 0, 10, 10
        action(x1, y1, x2, y2)

    def test_rotateLeft(self):
        RotateLeftAction(self.image)()
    
    def test_blur(self):
        action = BlurAction(self.image)
        amount = 2 # min=0,max=8,
        action(amount)

    def test_save(self):
        SaveImageEditAction(self.image)()

    def test_cancel(self):
        CancelImageEditAction(self.image)()

    def test_redo(self):
        RedoAction(self.image)()

    def test_undo(self):
        UndoAction(self.image)()

    def test_rotateRight(self):
        RotateRightAction(self.image)()

    def test_flipVertical(self):
        FlipOnVerticalAxisAction(self.image)()

    def test_compress(self):
        action = CompressAction(self.image)
        amount = 60.0
        action(amount)

    def test_contrast(self):
        action = ContrastAction(self.image)
        amount = 50.0
        action(amount)

    def test_bright(self):
        action = BrightnessAction(self.image)
        amount = 50.0
        action(amount)
        
    def test_sharpen(self):
        action = SharpenAction(self.image)
        amount = 1.5
        action(amount)
        
    def test_flipHorizontal(self):
        FlipOnHorizontalAxisAction(self.image)()
        
    def test_resize(self):
        action = ResizeAction(self.image)
        width, height = 150, 150
        action(width, height)
        
    def test_dropShadow(self):
        action = DropShadowAction(self.image)
        offset_x = 5
        offset_y = 5
        background_color = u"ffffff"
        shadow_color = u"444444"
        border = 8
        iterations = 3
        action(offset_x, offset_y, background_color, shadow_color, border, iterations)
        
    def test_save_as_image(self):
        parent = self.image.getParentNode()
        action = SaveAsImageEditAction(self.image)
        title = "foobar"
        _type = "Image"
        res = action(_type, title)
        
        self.failUnless(title in parent.objectIds())
        self.failUnless(res['new_type_location'] == "%s/%s/edit" % (parent.absolute_url(), title))
        self.failUnless(parent['foobar'].portal_type == "Image")
    
    def test_save_as_news_item(self):
        parent = self.image.getParentNode()
        action = SaveAsImageEditAction(self.image)
        title = "foobar"
        _type = "News Item"
        res = action(_type, title)

        self.failUnless(title in parent.objectIds())
        self.failUnless(res['new_type_location'] == "%s/%s/edit" % (parent.absolute_url(), title))
        self.failUnless(parent['foobar'].portal_type == "News Item")

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestActions))
    return suite
