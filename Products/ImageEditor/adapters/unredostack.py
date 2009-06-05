from Products.ImageEditor.interfaces.unredostack import IUnredoStack
from zope.interface import implements
from zope.component import adapts
from Products.ATContentTypes.interface.image import IImageContent
from PIL import Image

class UnredoStack(object):
    """
    see interfaces.py for info
    """
    implements(IUnredoStack)
    adapts(IImageContent)

    def __init__(self, context):
        self.context = context
        
        if not hasattr(context, 'stack_pos'):
            self.pos = 0
        if not hasattr(context, 'unredostack'):
            self.stack = [context.getField('image').get(context).data]
        
    def get_pos(self):
        return self.context.stack_pos
    def set_pos(self, value):
        self.context.stack_pos = value
    pos = property(get_pos, set_pos)

    def get_stack(self):
        return self.context.unredostack
    def set_stack(self, value):
        self.context.unredostack = value
    stack = property(get_stack, set_stack)

    def do(self, value):
        if self.can_redo():
            #clear top
            for item in self.stack[(self.pos+1):len(self.stack)]:
                self.stack.remove(item)

        self.stack.append(value)
        self.pos = self.pos + 1

    def get_current(self):
        self.context.plone_log(self.pos)
        self.context.plone_log(self.stack)
        #TypeError: expected read buffer, ImplicitAcquirerWrapper found
        return self.stack[self.pos]

    def undo(self):
        self.pos = self.pos - 1

    def can_undo(self):
        return self.pos > 0

    def redo(self):
        self.pos = self.pos + 1

    def can_redo(self):
        return self.pos + 1 < len(self.stack)
        
    def clear_stack(self, bottom=None):
        
        if hasattr(self.context, 'stack_pos'):
            delattr(self.context, 'stack_pos')
            
        if hasattr(self.context, 'unredostack'):
            delattr(self.context, 'unredostack')
            
        self.pos = 0

        if bottom is None:
            bottom = self.context.getField('image').get(self.context).data

        self.stack = [bottom]