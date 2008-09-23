from zope.interface import implements

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.kss.interfaces import IPloneKSSView
from plone.app.kss.plonekssview import PloneKSSView
from kss.core import kssaction
from PIL import Image, ImageFilter, ImageEnhance
from cStringIO import StringIO
import random
from Products.ATContentTypes.content.image import ATImage
from time import gmtime, strftime
from uwosh.ATImageEditor.interfaces import IUnredoStack

def _(s):
    """
    takes a string and returns the int that PIL likes
    """
    return int(float(s))

class Edit(BrowserView):

    template = ViewPageTemplateFile('imageeditor.pt')

    def __init__(self, *args, **kwargs):
        BrowserView.__init__(self, *args, **kwargs)
        
        self.unredo = IUnredoStack(self.context)
        
        # always start with new image
        # not sure if this is desired or not 
        # this way old edits are removed
        self.unredo.clearStack()

    def __call__(self):        
        #reset on each visit to page
        return self.template()
        
    def image_url(self):
        """
        This is used because sometimes browsers cache images that may have been edited
        """
        return self.context.absolute_url() + "?" + str(random.randint(0, 1000000))

    def canCompress(self):
        #cannot compress png files
        return str(Image.open(StringIO(self.unredo.getCurrent())).format != "PNG")

    def getSize(self):
        return GetImageInfo(self.unredo.getCurrent())['size']
        

class ShowCurrentEdit(BrowserView):

    def __init__(self, *args, **kwargs):
        BrowserView.__init__(self, *args, **kwargs)
        self.unredo = IUnredoStack(self.context)

    def __call__(self):
        
        resp = self.request.response
        
        resp.setHeader('Content-Type', 'image/jpeg')
        resp.setHeader('Content-Length', len(self.unredo.getCurrent()))
        resp.setHeader('Last-Modified', strftime('%a, %d %b %Y %H:%M:%S +0000', gmtime()))
        resp.write(self.unredo.getCurrent())
        return ''

class ImageEditorKSS(PloneKSSView):
    implements(IPloneKSSView)

    def __init__(self, *args, **kwargs):
        super(PloneKSSView, self).__init__(*args, **kwargs)
        
        self.unredo = IUnredoStack(self.context)

    def getImageData(self):
        return Image.open(StringIO(self.unredo.getCurrent()))

    def callSetImageCommand(self):
        """
        
        """
        imageCommands = self.getCommandSet('imageeditor')
        ksscore = self.getCommandSet('core')
        
        imageInfo = GetImageInfo(self.unredo.getCurrent())
        
        imageCommands.setImage(
            ksscore.getSameNodeSelector(), 
            self.context.absolute_url() + "/showcurrentedit?" + str(random.randint(0, 1000000)),
            str(int(self.unredo.canUndo())),
            str(int(self.unredo.canRedo())),
            str(int(self.unredo.pos > 0)),
            imageInfo['size'],
            imageInfo['width'],
            imageInfo['height']
        )
        
    def setImage(self, value):
        value.seek(0)
        self.unredo.do(value.read())
        
        self.callSetImageCommand()

    @kssaction
    def saveImageEdit(self):
        """
        This method gets the current image in the unredo stack and saves it to the
        object.  It then saves the history of it and gets the version_message so
        the history has better info...
        """
          
        #force versioning to kick in
        portal_repository = getToolByName(self.context, 'portal_repository')
        if portal_repository.isVersionable(self.context):
            portal_repository.save(self.context, comment = "")

        current = self.unredo.getCurrent()
        self.context.setImage(current)
        self.unredo.clearStack()
        
        self.context.reindexObject() #stop image caching on browser
        
        self.callSetImageCommand()
    
    @kssaction 
    def cancelImageEdit(self):
        """
        Just create a new UnredoStack and remove all edits
        """
        self.unredo.clearStack()
        self.callSetImageCommand()
        
    @kssaction
    def redoImageEdit(self):
        """
        ...
        """
        self.unredo.redo()
        self.callSetImageCommand()

    @kssaction 
    def undoImageEdit(self):
        self.unredo.undo()
        self.callSetImageCommand()

    @kssaction
    def rotateImageLeft(self):
        original = self.getImageData()
        image = original.rotate(90)
        
        output = StringIO()
        image.save(output, original.format)
        
        self.setImage(output)
        
    @kssaction
    def rotateImageRight(self):
        original = self.getImageData()
        image = original.rotate(270)
        
        output = StringIO()
        image.save(output, original.format)
        
        self.setImage(output)

    @kssaction
    def imageFlipOnVerticalAxis(self):
        original = self.getImageData()
        image = original.transpose(Image.FLIP_TOP_BOTTOM)
        
        output = StringIO()
        image.save(output, original.format)
        
        self.setImage(output)
        
    @kssaction
    def blur(self, amount):
        image = self.getImageData()
        fmt = image.format
        for x in range(0, _(amount)):
            image = image.filter(ImageFilter.BLUR)
            
        output = StringIO()
        image.save(output, fmt)
        self.setImage(output)
        
    @kssaction
    def compress(self, amount):
        output = StringIO()
        self.getImageData().convert('RGB').save(output, 'JPEG', quality=_(amount))
        self.setImage(output)
        
    @kssaction
    def contrast(self, amount):
        """
        @param amount: will be number between 0-100
        """
        image = self.getImageData()
        enhancer = ImageEnhance.Contrast(image)
        #can enhance from 0.0-2.0, 1.0 being original image
        newImage = enhancer.enhance(float("." + amount)*2.0)

        output = StringIO()
        newImage.save(output, image.format)
        self.setImage(output)

    @kssaction
    def brightness(self, amount):
        """
        @param amount: will be number between 0-100
        """
        image = self.getImageData()
        enhancer = ImageEnhance.Brightness(image)
        #can enhance from 0.0-2.0, 1.0 being original image
        newImage = enhancer.enhance(float("." + amount)*2.0)

        output = StringIO()
        newImage.save(output, image.format)
        self.setImage(output)

    @kssaction
    def sharpen(self, amount):
        image = self.getImageData()
        enhancer = ImageEnhance.Sharpness(image)
        newImage = enhancer.enhance(float(amount))

        output = StringIO()
        newImage.save(output, image.format)
        self.setImage(output)

    @kssaction
    def imageFlipOnHorizontalAxis(self):
        original = self.getImageData()
        image = original.transpose(Image.FLIP_LEFT_RIGHT)
        
        output = StringIO()
        image.save(output, original.format)
        self.setImage(output)

    @kssaction
    def imageResizeSave(self, width, height):
        image = self.getImageData()
        format = image.format
        size=( _(width), _(height) )
        image = image.resize(size, Image.ANTIALIAS)
        data = StringIO()
        image.save(data, format)
        data.seek(0)
        
        self.setImage(data)
    
    @kssaction
    def imageCropSave(self, topLeftX, topLeftY, bottomRightX, bottomRightY):
        image = self.getImageData()
        format = image.format
        box = (_(topLeftX), _(topLeftY), _(bottomRightX), _(bottomRightY))
        new_image = image.crop(box=box)
        new_image.load()

        cropped_output = StringIO()
        new_image.save(cropped_output, format)
        cropped_output.seek(0)
        
        self.setImage(cropped_output)
        
    @kssaction
    def cropAndResize(self, topLeftX, topLeftY, bottomRightX, bottomRightY, width, height):
        #resize
        image = self.getImageData()
        format = image.format
        size=( _(width), _(height) )
        image = image.resize(size, Image.ANTIALIAS)
        data = StringIO()
        image.save(data, format)

        data.seek(0)
        
        #crop
        image = Image.open(StringIO(data.read()))
        format = image.format
        box = (_(topLeftX), _(topLeftY), _(bottomRightX), _(bottomRightY))
        new_image = image.crop(box=box)
        new_image.load()
        cropped_output = StringIO()
        format = format and format or default_format
        new_image.save(cropped_output, format)
        cropped_output.seek(0)
        
        self.setImage(cropped_output)
        
    @kssaction
    def addDropShadow(self):
        """
        Code taken from http://code.activestate.com/recipes/474116/
        """
        image = self.getImageData()
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
        
def GetImageInfo(data):
    """
    returns information in the form of a string dict about the image
    uses strings only because that is what kss likes
    @param data: image data
    """
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
    