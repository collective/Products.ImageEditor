from zope.interface import Interface, Attribute

class IImageEditorAdapter(Interface):
        
    def undo():
        """
        undo last edit
        """
        
    def redo():
        """
        redo edit
        """
        
    def clear_edits():
        """
        clear all edits from undo/redo
        """

    def save_edit():
        """
        This method gets the current image in the unredo stack and saves it to the
        object.  It then saves the history of it and gets the version_message so
        the history has better info...
        """
       
    def set_image():
        """
        Set new image on stack
        """
       
    def get_current_image():
        """
        return the currently edited image
        """
        
    def get_current_image_data():
       """
       
       """
       
    def get_current_image_info():
        """
        
        """
       
class IImageEditorUtility(Interface):
    
    def should_include(context):
        """
        will check if css and js files should be included
        """
        
class IImageEditorLayer(Interface):
    """
    marker interface for image editor layer
    """
    
class IImageEditorContext(Interface):
    """
    Just a context for image editor actions so they can be traversed.
    """
    
class IImageEditorActionContext(Interface):
    """
    The actually traversable actions that allow ajax calls to be performed.
    """