from zope.interface import implements
from zope.component import adapts
from Products.ATContentTypes.interface.image import IATImage
from Products.ImageEditor.interfaces.imageeditor import IImageEditorAdapter
from Products.ImageEditor.interfaces.unredostack import IUnredoStack
from PIL import Image, ImageFilter, ImageEnhance
from cStringIO import StringIO

class ImageEditorAdapter(object):
    implements(IImageEditorAdapter)
    adapts(IATImage)
    
    def __init__(self, image):
        self.image = image
        #adapter to handle redo and undo
        self.unredo = IUnredoStack(image)
        
    def undo(self):
        self.unredo.undo()
        
    def redo(self):
        self.unredo.redo()
        
    def clearEdits(self):
        self.unredo.clearStack()

    def saveEdit(self):
        image_data = self.unredo.getCurrent()
        
        field = self.image.getField('image')
        mimetype = field.getContentType(self.image)
        filename = field.getFilename(self.image)
        
        # because AT tries to get mimetype and filename from a file like
        # object by attribute access I'm passing a string along
        self.image.setImage(
            image_data, 
            mimetype=mimetype,
            filename=filename, 
            refresh_exif=False
        )
        
        #should I clear???  Maybe you should still be able to undo...              
        self.unredo.clearStack(image_data)
        
    def getOriginalImage(self):
        return Image.open(StringIO(self.unredo.stack[0]))
        
    def getCurrentImage(self):
        return Image.open(StringIO(self.unredo.getCurrent()))
       
    def setImage(self, image, format="JPEG", quality=None):
        """
        Setting the image just adds to the unredo stack...
        """
        image_data = StringIO()
        
        if quality:
            image.save(image_data, format, quality=quality)
        else:
            image.save(image_data, format)
        
        self.unredo.do(image_data.getvalue())
       
    def getCurrentImageData(self):
        return self.unredo.getCurrent()
       
    def getCurrentImageInfo(self):
        data = self.getCurrentImageData()
        bsize = len(data)
        bsize = bsize/1024

        size_descriptor = 'kb'
        if bsize > 1024:
            bsize = bsize/1024.0
            size_descriptor = 'mb'

        size = self.getCurrentImage().size

        width = size[0]
        height = size[1]

        return {
            'size': bsize,
            'width': width,
            'height': height,
            'sizeformatted': "Size: %s%s" % (str(bsize)[:4], size_descriptor)
        }
       
    def rotateLeft(self):
        original = self.getCurrentImage()
        image = original.rotate(90)

        self.setImage(image, original.format)
        
    def rotateRight(self):
        original = self.getCurrentImage()
        image = original.rotate(270)

        self.setImage(image, original.format)
        
    def flipOnVerticalAxis(self):
        original = self.getCurrentImage()
        image = original.transpose(Image.FLIP_TOP_BOTTOM)

        self.setImage(image, original.format)
        
    def flipOnHorizontalAxis(self):
        original = self.getCurrentImage()
        image = original.transpose(Image.FLIP_LEFT_RIGHT)

        self.setImage(image, original.format)
        
    def blur(self, amount):
        image = self.getCurrentImage()
        fmt = image.format
        for x in range(0, amount):
            image = image.filter(ImageFilter.BLUR)
            
        self.setImage(image, fmt)
        
    def compress(self, amount):
        image = self.getCurrentImage().convert('RGB') # if it is a png, convert it...
        self.setImage(image, quality=amount)
        
    def contrast(self, amount):
        image = self.getCurrentImage()
        enhancer = ImageEnhance.Contrast(image)
        newImage = enhancer.enhance(amount)

        self.setImage(newImage, image.format)
        
    def brightness(self, amount):
        """
        amount should be between 0.0 and 2.0
        1.0 being the original image
        """
        image = self.getCurrentImage()
        enhancer = ImageEnhance.Brightness(image)
        #can enhance from 0.0-2.0, 1.0 being original image
        newImage = enhancer.enhance(amount)

        self.setImage(newImage, image.format)
        
    def sharpen(self, amount):
        image = self.getCurrentImage()
        enhancer = ImageEnhance.Sharpness(image)
        newImage = enhancer.enhance(amount)

        self.setImage(newImage, image.format)
    
    def resize(self, width, height):
        image = self.getCurrentImage()
        format = image.format
        size=(width, height)
        new_image = image.resize(size, Image.ANTIALIAS)
        
        self.setImage(new_image, image.format)
        
    def crop(self, tlx, tly, brx, bry):
        image = self.getCurrentImage()
        format = image.format
        box = (tlx, tly, brx, bry)
        new_image = image.crop(box=box)
        new_image.load()
        
        self.setImage(new_image, image.format)
        
    def dropshadow(self):
        """
        Code taken from http://code.activestate.com/recipes/474116/
        """
        image = self.getCurrentImage()
        offset = (5,5)
        background=0xffffff
        shadow=0x444444
        border=8
        iterations=3
        format = image.format
        
        # Create the backdrop image -- a box in the background colour with a 
        # shadow on it.
        totalWidth = image.size[0] + abs(offset[0]) + 2*border
        totalHeight = image.size[1] + abs(offset[1]) + 2*border
        back = Image.new(image.mode, (totalWidth, totalHeight), background)

        # Place the shadow, taking into account the offset from the image
        shadowLeft = border + max(offset[0], 0)
        shadowTop = border + max(offset[1], 0)
        back.paste(shadow, [shadowLeft, shadowTop, shadowLeft + image.size[0], 
        shadowTop + image.size[1]] )

        # Apply the filter to blur the edges of the shadow.  Since a small kernel
        # is used, the filter must be applied repeatedly to get a decent blur.
        n = 0
        while n < iterations:
            back = back.filter(ImageFilter.BLUR)
            n += 1

        # Paste the input image onto the shadow backdrop  
        imageLeft = border - min(offset[0], 0)
        imageTop = border - min(offset[1], 0)
        back.paste(image, (imageLeft, imageTop))
        
        self.setImage(back, format)
        
        