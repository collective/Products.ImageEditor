from Products.ImageEditor.interfaces.unredostack import IUnredoStack
from zope.interface import implements
from zope.component import adapts
from Products.ATContentTypes.interface.image import IATImage
from PIL import Image
from cStringIO import StringIO

class UnredoStack(object):
    """
    see interfaces.py for info
    """
    implements(IUnredoStack)
    adapts(IATImage)

    def __init__(self, image):
        self.image = image
        
        if not hasattr(image, 'stack_pos'):
            self.pos = 0
        if not hasattr(image, 'unredostack'):
            self.stack = [image.data]
        
    def get_pos(self):
        return self.image.stack_pos
    def set_pos(self, value):
        self.image.stack_pos = value
    pos = property(get_pos, set_pos)

    def get_stack(self):
        return self.image.unredostack
    def set_stack(self, value):
        self.image.unredostack = value
    stack = property(get_stack, set_stack)

    def do(self, value):
        if self.canRedo():
            #clear top
            for item in self.stack[(self.pos+1):len(self.stack)]:
                self.stack.remove(item)

        self.stack.append(value)
        self.pos = self.pos + 1

    def getCurrent(self):
        return self.stack[self.pos]

    def undo(self):
        self.pos = self.pos - 1

    def canUndo(self):
        return self.pos > 0

    def redo(self):
        self.pos = self.pos + 1

    def canRedo(self):
        return self.pos + 1 < len(self.stack)
        
    def clearStack(self, bottom=None):
        
        if hasattr(self.image, 'stack_pos'):
            delattr(self.image, 'stack_pos')
            
        if hasattr(self.image, 'unredostack'):
            delattr(self.image, 'unredostack')
            
        self.pos = 0

        if bottom is None:
            bottom = self.image.data

        self.stack = [bottom]