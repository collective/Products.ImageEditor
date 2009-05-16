from zope.interface import Interface, Attribute

class IUnredoStack(Interface):
    
    pos = Attribute("""Position of the stack""")
    stack = Attribute("""Actual stack...""")
    
    def do(self, value):
        """
        performing the action
        """
        
    def get_current(self):
        """
        Returns the current element in stack
        """
        
    def undo(self):
        """
        Undo action
        """
        
    def can_undo(self):
        """
        Returns boolean if they can undo
        """
        
    def redo(self):
        """
        redo last action
        """
        
    def can_redo(self):
        """
        Returns boolean if they can redo
        """
        
    def clear_stack(self):
        """
        Clears the stack and resets all image edits
        """
    
