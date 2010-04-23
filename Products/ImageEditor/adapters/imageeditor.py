from persistent.dict import PersistentDict
from persistent.list import PersistentList
from zope.interface import implements
from zope.component import adapts
from Products.ATContentTypes.interface.image import IImageContent
from Products.ImageEditor.interfaces import IImageEditorAdapter
from PIL import Image
from cStringIO import StringIO
from Acquisition import aq_inner


class ImageEditorAdapter(object):
    """context.getField('image').get(context) -> Field Image
    Field Image.data -> OFS Image
    OFSImage.data    -> str
    
    stack = [str, ...]
    """
    implements(IImageEditorAdapter)
    adapts(IImageContent)
    
    def __init__(self, context):
        self.context = aq_inner(context)

    @property
    def storage(self):
        session = self.context.REQUEST.SESSION      # evil! :)
        if not session.has_key('imageeditor'):
            session['imageeditor'] = PersistentDict()
        
        editordata = session['imageeditor']
        uid = self.context.UID()
        
        if not editordata.has_key(uid):
            editordata[uid] = PersistentDict()
        
        return editordata[uid]

    @property
    def field(self):
        storage = self.storage
        fieldname = storage.get('fieldname')
        if fieldname:
            return self.context.getField(fieldname)
        else:
            return self.context.getField('image') or \
                self.context.getPrimaryField()

    def set_field(self, name):
        storage = self.storage
        if not name == storage.get('fieldname'):
            storage['fieldname'] = name     # set name before clear
            self.clear_edits()

    def get_image_data(self):
        return str(self.field.get(self.context).data)

    # UNDO REDO STUFF
    def get_pos(self):
        return self.storage.setdefault('position', 0)
    def set_pos(self, value):
        self.storage['position'] = value
    pos = property(get_pos, set_pos)

    @property
    def stack(self):
        stack = self.storage.setdefault('unredostack', PersistentList())
        if not stack:
            stack.append(self.get_image_data())
        return stack

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
        if bottom is None:
            bottom = self.get_image_data()
        stack = self.stack
        stack[:] = [bottom]
        self.pos = 0

    def do(self, value):
        if self.can_redo():
            for item in self.stack[(self.pos+1):len(self.stack)]:
                self.stack.remove(item)

        self.stack.append(value)
        self.pos = self.pos + 1

    def save_edit(self):
        image_data = self.get_current_image_data()
        
        field = self.field
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


