from zope.interface import Interface, Attribute

class IImageEditorAdapter(Interface):
     
    unredo = Attribute("""The unredo stack to handle undo and redo""")
        
    def undo(self):
        """
        undo last edit
        """
        
    def redo(self):
        """
        redo edit
        """
        
    def clearEdits(self):
        """
        clear all edits from undo/redo
        """

    def saveEdit(self):
        """
        This method gets the current image in the unredo stack and saves it to the
        object.  It then saves the history of it and gets the version_message so
        the history has better info...
        """
    def getOriginalImage(self):
        """
        
        """

    def getImageData(self):
        """
        get current image data from stack
        """
       
    def setImage(self, value):
       """
       Set new image on stack
       """
       
    def imageInfo(self):
        """
        return information on the current image
        """
       
    def rotateLeft(self):
        """
        rotate image left
        """
        
    def rotateRight(self):
        """
        rotate image right
        """
        
    def flipOnVerticalAxis(self):
        """
        """
        
    def flipOnHorizontalAxis(self):
        """
        """
        
    def blur(self, amount):
        """
        blur image by amount
        """
        
    def compress(self, amount):
        """
        compress the image and convert it to jpg if necessary
        """
        
    def contrast(self, amount):
        """
        set contrast on an image
        """
        
    def brightness(self, amount):
        """
        set brightness on an image
        """
        
    def sharpen(self, amount):
        """
        sharpen an image
        """
    
    def resize(self, width, height):
        """
        resize current image
        """
        
    def crop(self, tlx, tly, brx, bry):
        """
        crop current image
        """
        
    def dropshadow(self):
       """
       add drop shadow to current image
       """