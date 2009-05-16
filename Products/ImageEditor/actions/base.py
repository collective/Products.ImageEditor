from Products.ImageEditor.interfaces.actions import IImageEditorAction
from Products.ImageEditor.interfaces.imageeditor import IImageEditorAdapter
from zope.interface import implements
from zope.component import adapts

class BaseImageEditorAction:
    adapts(IImageEditorAdapter)
    implements(IImageEditorAction)
    
    name = ""
    description = ""
    skip_apply = False
    options = None
    icon = None
    
    def __init__(self, image):
        self.editor = IImageEditorAdapter(image)
        
    def action_parameters(self):
        return False
    
    def on_setup(self):
        return False
    
    def __call__(self):
        raise Exception("Not Implemented")