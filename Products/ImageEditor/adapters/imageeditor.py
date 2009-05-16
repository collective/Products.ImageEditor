from zope.interface import implements
from zope.component import adapts
from Products.ATContentTypes.interface.image import IImageContent
from Products.ImageEditor.interfaces.imageeditor import IImageEditorAdapter
from Products.ImageEditor.interfaces.unredostack import IUnredoStack
from PIL import Image, ImageFilter, ImageEnhance
from cStringIO import StringIO

class ImageEditorAdapter(object):
    implements(IImageEditorAdapter)
    adapts(IImageContent)
    
    def __init__(self, context):
        self.context = context
        #adapter to handle redo and undo
        self.unredo = IUnredoStack(context)
        
    def undo(self):
        self.unredo.undo()
        
    def redo(self):
        self.unredo.redo()
        
    def clear_edits(self):
        self.unredo.clear_stack()

    def save_edit(self):
        image_data = self.unredo.get_current()
        
        field = self.context.getField('image')
        mimetype = field.getContentType(self.context)
        filename = field.getFilename(self.context)
        
        # because AT tries to get mimetype and filename from a file like
        # object by attribute access I'm passing a string along
        field.set(
            self.context,
            image_data, 
            mimetype=mimetype,
            filename=filename, 
            refresh_exif=False
        )
        
        #should I clear???  Maybe you should still be able to undo...              
        #self.unredo.clear_stack(image_data)
        
    def get_current_image(self):
        return Image.open(StringIO(self.unredo.get_current()))
       
    def set_image(self, image, format="JPEG", quality=None):
        """
        Setting the image just adds to the unredo stack...
        """
        image_data = StringIO()
        
        if quality:
            image.save(image_data, format, quality=quality)
        else:
            image.save(image_data, format)
        
        self.unredo.do(image_data.getvalue())
       
    def get_current_image_data(self):
        return self.unredo.get_current()
       
    def get_current_image_info(self):
        data = self.get_current_image_data()
        bsize = len(data)
        bsize = bsize/1024

        size_descriptor = 'kb'
        if bsize > 1024:
            bsize = bsize/1024.0
            size_descriptor = 'mb'

        size = self.get_current_image().size

        width = size[0]
        height = size[1]

        return {
            'size': bsize,
            'width': width,
            'height': height,
            'sizeformatted': "Size: %s%s" % (str(bsize)[:4], size_descriptor)
        }
        
