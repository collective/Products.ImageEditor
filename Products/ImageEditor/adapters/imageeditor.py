from persistent.dict import PersistentDict
from persistent.list import PersistentList
from zope.interface import implements
from zope.component import adapts
from Products.ATContentTypes.interface.image import IImageContent
from Products.ImageEditor.interfaces import IImageEditorAdapter
from PIL import Image
from cStringIO import StringIO
from Acquisition import aq_inner


ListStorage = PersistentList


try:
    from beaker.cache import CacheManager
    from beaker.util import parse_cache_config_options
    import os
    options = {}
    for key in os.environ.keys():
        if key.startswith('BEAKER_CACHE_'):
            bkey = 'cache.' + key.lstrip('BEAKER_CACHE_').lower()
            options[bkey] = os.environ[key].strip()

    if not options:
        raise ImportError

    cache_manager = CacheManager(**parse_cache_config_options(options))

    class Cache(object):
        def __init__(self, name, expire):
            self.store = cache_manager.get_cache(name, expire=expire)

        def get(self, key, default=None):
            try:
                return self.store.get_value(key)
            except KeyError:
                return default

        def put(self, key, value):
            self.store.set_value(key, value)
    beaker_cache = Cache('imageeditor', 86400)
    BEAKER_ENABLED = True
    ListStorage = list
except ImportError:
    BEAKER_ENABLED = False


class BeakerStorage(object):

    def __init__(self, uid):
        self.uid = uid
        self.data = beaker_cache.get(uid, {})

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        rtn = self.data[key] = value
        beaker_cache.put(self.uid, self.data)
        return rtn

    def setdefault(self, key, value):
        rtn = self.data.setdefault(key, value)
        beaker_cache.put(self.uid, self.data)
        return rtn

    def get(self, key, default=None):
        return self.data.get(key, default)


def _getBeakerStorage(context):
    return BeakerStorage(context.UID())


def _getSessionStorage(context):
    session = context.REQUEST.SESSION  # evil! :)
    if not session.has_key('imageeditor'):
        session['imageeditor'] = PersistentDict()
    return session['imageeditor'].setdefault(
        context.UID(), PersistentDict())


def getStorage(context):
    if BEAKER_ENABLED:
        return _getBeakerStorage(context)
    else:
        return _getSessionStorage(context)


class ImageEditorAdapter(object):
    """context.getField('image').get(context) -> Field Image
    Field Image.data -> OFS Image
    OFSImage.data    -> str

    stack = [str, ...]
    """
    implements(IImageEditorAdapter)
    adapts(IImageContent)

    def __init__(self, context, fieldname=''):
        self.context = aq_inner(context)
        self.fieldname = fieldname
        if fieldname == '':
            # always set a fieldname so we get keys right
            field = self.field
            self.fieldname = field.__name__
        self.storage = getStorage(self.context)

    @property
    def field(self):
        if self.fieldname:
            return self.context.getField(self.fieldname)
        else:
            return self.context.getField('image') or \
                self.context.getPrimaryField()

    def set_field(self, name):
        if name != '':
            self.fieldname = name

    def get_image_data(self):
        return str(self.field.get(self.context).data)

    # UNDO REDO STUFF
    def get_pos(self):
        return self.storage.setdefault('position%s' % self.fieldname, 0)

    def set_pos(self, value):
        self.storage['position%s' % self.fieldname] = value
    pos = property(get_pos, set_pos)

    @property
    def stackkey(self):
        return 'unredostack%s' % self.fieldname

    def store_stack(self, stack):
        self.storage[self.stackkey] = stack

    @property
    def stack(self):
        stack = self.storage.setdefault(self.stackkey, ListStorage())
        if not stack:
            stack.append(self.get_image_data())
            self.store_stack(stack)
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
        self.store_stack(stack)
        self.pos = 0
        self.storage['clearkey' + self.fieldname] = False

    def do(self, value):
        stack = self.stack
        if self.can_redo():
            for item in self.stack[(self.pos + 1):len(self.stack)]:
                stack.remove(item)

        stack.append(value)
        self.store_stack(stack)
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
        # should I clear???  Maybe you should still be able to undo...
        self.clear_edits(image_data)

    def get_current_image(self):
        return Image.open(StringIO(self.get_current_image_data()))

    def get_current_image_data(self):
        return self.stack[self.pos]

    def get_current_image_info(self):
        data = self.get_current_image_data()
        bsize = len(data)
        bsize = bsize / 1024

        size_descriptor = 'kb'
        if bsize > 1024:
            bsize = bsize / 1024.0
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
