from zope.interface import implements
from uwosh.ATImageEditor.interfaces import IUnredoStack
from zope.component import adapts
from Products.ATContentTypes.interface.image import IATImage

class UnredoStack(object):
    """
    see interfaces.py for info
    """
    implements(IUnredoStack)
    adapts(IATImage)

    def __init__(self, context):
        self.context = context
        
        if not hasattr(context, 'stack_pos'):
            self.pos = 0
        if not hasattr(context, 'unredostack'):
            self.stack = [self.context.data]
        
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
        
    def clearStack(self):
        UnredoStack.__init__(self, self.context)