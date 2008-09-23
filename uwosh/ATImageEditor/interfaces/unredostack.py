from zope.interface import Interface, Attribute

class IUnredoStack(Interface):
    
    pos = Attribute("""Position of the stack""")
    stack = Attribute("""Actual stack...""")
    
    def do(self, value):
        """
        performing the action
        """
        
    def getCurrent(self):
        """
        Returns the current element in stack
        """
        
    def undo(self):
        """
        Undo action
        """
        
    def canUndo(self):
        """
        Returns boolean if they can undo
        """
        
    def redo(self):
        """
        redo last action
        """
        
    def canRedo(self):
        """
        Returns boolean if they can redo
        """
        
    def clearStack(self):
        """
        Clears the stack
        """
    
