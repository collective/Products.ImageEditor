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

def _(s):
    """
    takes a string and returns the int that PIL likes
    """
    return int(float(s))

class Edit(BrowserView):

    template = ViewPageTemplateFile('imageeditor.pt')

    def __call__(self):        
        #reset on each visit to page
        self.context.unredo = UnredoStack(self.context.data)
        return self.template()
        
    def image_url(self):
        """
        This is used because sometimes browsers cache images that may have been edited
        """
        return self.context.absolute_url() + "?" + str(random.randint(0, 1000000))

    def canCompress(self):
        #cannot compress png files
        return str(Image.open(StringIO(self.context.data)).format != "PNG")

    def getSize(self):
        return GetImageInfo(self.context.unredo.getCurrent())['size']
        

class ShowCurrentEdit(BrowserView):

    def __call__(self):
        
        resp = self.request.response
        
        resp.setHeader('Content-Type', 'image/jpeg')
        resp.setHeader('Content-Length', len(self.context.unredo.getCurrent()))
        resp.setHeader('Last-Modified', strftime('%a, %d %b %Y %H:%M:%S +0000', gmtime()))
        resp.write(self.context.unredo.getCurrent())
        return ''

class ImageEditorKSS(PloneKSSView):
    implements(IPloneKSSView)

    def getImageData(self):
        return Image.open(StringIO(self.context.unredo.getCurrent()))

    def callSetImageCommand(self):
        """
        
        """
        imageCommands = self.getCommandSet('imageeditor')
        ksscore = self.getCommandSet('core')
        
        imageInfo = GetImageInfo(self.context.unredo.getCurrent())
        
        imageCommands.setImage(
            ksscore.getSameNodeSelector(), 
            self.context.absolute_url() + "/showcurrentedit?" + str(random.randint(0, 1000000)),
            str(int(self.context.unredo.canUndo())),
            str(int(self.context.unredo.canRedo())),
            str(int(self.context.unredo.pos > 0)),
            imageInfo['size'],
            imageInfo['width'],
            imageInfo['height']
        )
        
    def setImage(self, value):
        value.seek(0)
        self.context.unredo.do(value.read())
        
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

        current = self.context.unredo.getCurrent()
        self.context.setImage(current)
        self.context.unredo = UnredoStack(current)
        
        self.context.reindexObject() #stop image caching on browser
        
        self.callSetImageCommand()
    
    @kssaction 
    def cancelImageEdit(self):
        """
        Just create a new UnredoStack and remove all edits
        """
        self.context.unredo = UnredoStack(self.context.data)
        self.callSetImageCommand()
        
    @kssaction
    def redoImageEdit(self):
        """
        ...
        """
        self.context.unredo.redo()
        self.callSetImageCommand()

    @kssaction 
    def undoImageEdit(self):
        self.context.unredo.undo()
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
        #image = new_image
        cropped_output = StringIO()
        format = format and format or default_format
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
        
class UnredoStack:
    """
    stack that handles undo and redo for image data
    """

    def __init__(self, bottom):
        """
        @param bottom: first element on the stack
        """
        self.pos = 0
        self.stack = [bottom]

    def do(self, value):
        """
        performing an action
        @param value: image data
        """
        if self.canRedo():
            #clear top
            for item in self.stack[(self.pos+1):len(self.stack)]:
                self.stack.remove(item)

        self.stack.append(value)
        self.pos = self.pos + 1

    def getCurrent(self):
        """
        gets the current element in the undo/redo stack
        """
        return self.stack[self.pos]

    def undo(self):
        self.pos = self.pos - 1

    def canUndo(self):
        return self.pos > 0

    def redo(self):
        self.pos = self.pos + 1

    def canRedo(self):
        return self.pos + 1 < len(self.stack)
        
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
    