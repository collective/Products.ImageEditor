import unittest
from cStringIO import StringIO
from Products.ImageEditor.tests import base
from Products.ImageEditor.actions.actions import *

class TestActions(base.ImageEditorTestCase):
    """Test Actions"""
    def afterSetUp(self):
        self.setRoles(('Manager',))
        self.image = [self.getImageContentType()]
        
    def beforeTearDown(self):
        self.portal.manage_delObjects(['testimage'])

    def test_crop(self):
        image = self.image[0]
        action = CropAction(image)
        x1, y1, x2, y2 = 0, 0, 10, 10
        action(x1, y1, x2, y2)
        #TODO: how could i test assert on img ?

    def test_rotateLeft(self):
        image = self.image[0]
        action = RotateLeftAction(image)
        action()
    
    def test_blur(self):
        image = self.image[0]
        action = BlurAction(image)
        amount = 2 # min=0,max=8,
        action(amount)

    def test_save(self):
        image = self.image[0]
        action = SaveImageEditAction(image)
        action()
        

    def test_cancel(self):
        image = self.image[0]
        action = CancelImageEditAction(image)
        action()
        

    def test_redo(self):
        image = self.image[0]
        action = RedoAction(image)
        action()
        

    def test_undo(self):
        image = self.image[0]
        action = UndoAction(image)
        action()
        

    def test_rotateRight(self):
        image = self.image[0]
        action = RotateRightAction(image)
        action()
        

    def test_flipVertical(self):
        image = self.image[0]
        action = FlipOnVerticalAxisAction(image)
        action()
        

    def test_compress(self):
        image = self.image[0]
        action = CompressAction(image)
        amount = 60.0
        action(amount)
        

    def test_contrast(self):
        image = self.image[0]
        action = ContrastAction(image)
        amount = 50.0
        action(amount)
        

    def test_bright(self):
        image = self.image[0]
        action = BrightnessAction(image)
        amount = 50.0
        action(amount)
        

    def test_sharpen(self):
        image = self.image[0]
        action = SharpenAction(image)
        amount = 2
        action(amount)
        

    def test_flipHorizontal(self):
        image = self.image[0]
        action = FlipOnHorizontalAxisAction(image)
        action()
        

    def test_resize(self):
        image = self.image[0]
        action = ResizeAction(image)
        width, height = 150, 150
        action(width, height)
        
        
    def test_dropShadow(self):
        image = self.image[0]
        action = DropShadowAction(image)
        offset_x = 5
        offset_y = 5
        background_color = u"ffffff"
        shadow_color = u"444444"
        border = 8
        iterations = 3
        action(offset_x, offset_y, background_color, shadow_color, border, iterations)
        editor = self.getEditor(image)
        self.imagesEqual('dropshadow.jpg', editor)
        



def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestActions))
    return suite
