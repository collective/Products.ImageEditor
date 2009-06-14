from zope.interface import Interface, Attribute

class IImageEditorAdapter(Interface):

    pos = Attribute("""Position of the stack""")
    stack = Attribute("""Actual stack...""")

    def do(self, value):
        """performing the action.
        value: str image data
        """

    def can_undo(self):
        """
        Returns boolean if they can undo
        """

    def undo():
        """
        undo last edit
        """

    def can_redo(self):
        """
        Returns boolean if they can redo
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
       
    def set_image(image, format="JPEG", quality=None):
        """ Set new image on stack
        image: PIL.image
        format: str represent the format
        quality: float for quality if supported by format
        """
       
    def get_current_image():
        """ return the currently edited image
          -> PIL.Image
        """
        
    def get_current_image_data():
       """ get currently edited image data
         -> str
       """
       
    def get_current_image_info():
        """ Return a dict of info about the image
         -> {'size': , 
             'width':,
             'height': ,
             'sizeformatted': "Size: %s%s"
            }
        
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