from zope.interface import implements
from zope.component import adapts
from Products.ATContentTypes.interface.image import IATImage
from uwosh.ATImageEditor.interfaces.imageeditor import IImageEditorAdapter
from uwosh.ATImageEditor.interfaces.unredostack import IUnredoStack
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
        current = self.unredo.getCurrent()
        self.image.setImage(current)
        self.unredo.clearStack()
        
    def getCurrentImage(self):
        return Image.open(StringIO(self.getCurrentImageData()))
       
    def setImage(self, value):
        value.seek(0)
        self.unredo.do(value.read())
       
       
    def getCurrentImageData(self):
        return self.unredo.getCurrent()
       
    def getCurrentImageInfo(self):
        data = self.unredo.getCurrent()
        bsize = len(data)
        bsize = bsize/1024

        if bsize > 1024:
            bsize = "Size: " + str(bsize/1024)[0:4] + 'mb'
        else:
            bsize = "Size: " + str(bsize)[0:4] + 'kb'

        size = Image.open(StringIO(data)).size

        width = size[0]
        height = size[1]

        return {
            'size': bsize,
            'width': str(width),
            'height': str(height)
        }
       
    def rotateLeft(self):
        original = self.getCurrentImage()
        image = original.rotate(90)
        
        output = StringIO()
        image.save(output, original.format)
        
        self.setImage(output)
        
    def rotateRight(self):
        original = self.getCurrentImage()
        image = original.rotate(270)
        
        output = StringIO()
        image.save(output, original.format)
        
        self.setImage(output)
        
    def flipOnVerticalAxis(self):
        original = self.getCurrentImage()
        image = original.transpose(Image.FLIP_TOP_BOTTOM)
        
        output = StringIO()
        image.save(output, original.format)
        
        self.setImage(output)
        
    def flipOnHorizontalAxis(self):
        original = self.getCurrentImage()
        image = original.transpose(Image.FLIP_LEFT_RIGHT)
        
        output = StringIO()
        image.save(output, original.format)
        self.setImage(output)
        
    def blur(self, amount):
        image = self.getCurrentImage()
        fmt = image.format
        for x in range(0, amount):
            image = image.filter(ImageFilter.BLUR)
            
        output = StringIO()
        image.save(output, fmt)
        self.setImage(output)
        
    def compress(self, amount):
        output = StringIO()
        self.getCurrentImage().convert('RGB').save(output, 'JPEG', quality=amount)
        self.setImage(output)
        
    def contrast(self, amount):
        image = self.getCurrentImage()
        enhancer = ImageEnhance.Contrast(image)
        #can enhance from 0.0-2.0, 1.0 being original image
        newImage = enhancer.enhance(amount)

        output = StringIO()
        newImage.save(output, image.format)
        self.setImage(output)
        
    def brightness(self, amount):
        image = self.getCurrentImage()
        enhancer = ImageEnhance.Brightness(image)
        #can enhance from 0.0-2.0, 1.0 being original image
        newImage = enhancer.enhance(amount)

        output = StringIO()
        newImage.save(output, image.format)
        self.setImage(output)
        
    def sharpen(self, amount):
        image = self.getCurrentImage()
        enhancer = ImageEnhance.Sharpness(image)
        newImage = enhancer.enhance(amount)

        output = StringIO()
        newImage.save(output, image.format)
        self.setImage(output)
    
    def resize(self, width, height):
        image = self.getCurrentImage()
        format = image.format
        size=(width, height)
        image = image.resize(size, Image.ANTIALIAS)
        data = StringIO()
        image.save(data, format)
        data.seek(0)
        
        self.setImage(data)
        
    def crop(self, tlx, tly, brx, bry):
        image = self.getCurrentImage()
        format = image.format
        box = (tlx, tly, brx, bry)
        new_image = image.crop(box=box)
        new_image.load()

        cropped_output = StringIO()
        new_image.save(cropped_output, format)
        cropped_output.seek(0)
        
        self.setImage(cropped_output)
        
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

        output = StringIO()
        back.save(output, format)
        output.seek(0)
        
        self.setImage(output)
        
        