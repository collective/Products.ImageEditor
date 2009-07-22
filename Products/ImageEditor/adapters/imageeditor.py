from zope.interface import implements
from zope.component import adapts
from Products.ATContentTypes.interface.image import IImageContent
from Products.ImageEditor.interfaces import IImageEditorAdapter
from PIL import Image, ImageFilter, ImageEnhance
from cStringIO import StringIO

class ImageEditorAdapter(object):
    """context.getField('image').get(context) -> Field Image
    Field Image.data -> OFS Image
    OFSImage.data    -> str
    
    stack = [str, ...]
    """
    implements(IImageEditorAdapter)
    adapts(IImageContent)
    
    def __init__(self, context):
        self.context = context

        if not hasattr(context, 'stack_pos'):
            self.pos = 0
        if not hasattr(context, 'unredostack'):
            self.stack = [self.get_image_data()]

    def get_image_data(self):
        data = self.context.getField('image').get(self.context).data
        if type(data) == str:
            return data
        else:
            return data.data

    #UNDO REDO STUFF
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

    def undo(self):
        if self.can_undo():
            self.pos = self.pos - 1

    def can_undo(self):
        return self.pos > 0

    def redo(self):
        if self.can_redo():
            self.pos = self.pos + 1

    def can_redo(self):
        return self.pos + 1 < len(self.stack)

    def clear_edits(self, bottom=None):
        if hasattr(self.context, 'stack_pos'):
            delattr(self.context, 'stack_pos')

        if hasattr(self.context, 'unredostack'):
            delattr(self.context, 'unredostack')

        self.pos = 0

        if bottom is None:
            bottom = self.get_image_data()

        self.stack = [bottom]


    def do(self, value):
        if self.can_redo():
            for item in self.stack[(self.pos+1):len(self.stack)]:
                self.stack.remove(item)

        self.stack.append(value)
        self.pos = self.pos + 1

    def save_edit(self):
        image_data = self.get_current_image_data()
        
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
        self.clear_edits(image_data)

    def get_current_image(self):
        return Image.open(StringIO(self.get_current_image_data()))

    def get_current_image_data(self):
        return self.stack[self.pos]

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
            'sizeformatted': "Size: %.2f%s" % (bsize, size_descriptor)
        }


    def set_image(self, image, format="JPEG", quality=None):
        image_data = StringIO()
        
        if quality:
            image.save(image_data, format, quality=quality)
        else:
            image.save(image_data, format)
        
        self.do(image_data.getvalue())


