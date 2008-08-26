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

    def getSize(self):
        return GetSize(self.context.unredo.getCurrent())
        

class ShowCurrentEdit(BrowserView):

    def __call__(self):
        
        RESPONSE = self.request.response
        REQUEST = self.request
        RESPONSE.setHeader('Content-Type', 'image/jpeg')
        RESPONSE.setHeader('Content-Length', len(self.context.unredo.getCurrent()))
        RESPONSE.setHeader('Last-Modified', strftime('%a, %d %b %Y %H:%M:%S +0000', gmtime()))
        RESPONSE.write(self.context.unredo.getCurrent())
        return ''
        
class ImageEditorKSS(PloneKSSView):
    implements(IPloneKSSView)

    def getImageData(self):
        return StringIO(self.context.unredo.getCurrent())

    def callSetImageCommand(self):
        imageCommands = self.getCommandSet('imageeditor')
        ksscore = self.getCommandSet('core')
        imageCommands.setImage(
            ksscore.getSameNodeSelector(), 
            self.context.absolute_url() + "/showcurrentedit?" + str(random.randint(0, 1000000)),
            str(int(self.context.unredo.canUndo())),
            str(int(self.context.unredo.canRedo())),
            str(int(self.context.unredo.pos > 0)),
            GetSize(self.context.unredo.getCurrent())            
        )
        
    def setImage(self, value):
        value.seek(0)
        self.context.unredo.do(value.read())
        
        self.callSetImageCommand()

    @kssaction
    def saveImageEdit(self):
        current = self.context.unredo.getCurrent()
        self.context.setImage(current)
        self.context.unredo = UnredoStack(current)
        self.callSetImageCommand()
    
    @kssaction 
    def cancelImageEdit(self):
        self.context.unredo = UnredoStack(self.context.data)
        self.callSetImageCommand()
        
    @kssaction
    def redoImageEdit(self):
        self.context.unredo.redo()
        self.callSetImageCommand()

    @kssaction 
    def undoImageEdit(self):
        self.context.unredo.undo()
        self.callSetImageCommand()

    @kssaction
    def rotateImageLeft(self):
        original = Image.open(self.getImageData())
        image = original.rotate(90)
        
        output = StringIO()
        image.save(output, original.format)
        
        self.setImage(output)
        
    @kssaction
    def rotateImageRight(self):
        original = Image.open(self.getImageData())
        image = original.rotate(270)
        
        output = StringIO()
        image.save(output, original.format)
        
        self.setImage(output)

    @kssaction
    def imageFlipOnVerticalAxis(self):
        original = Image.open(self.getImageData())
        image = original.transpose(Image.FLIP_TOP_BOTTOM)
        
        output = StringIO()
        image.save(output, original.format)
        
        self.setImage(output)
        
    @kssaction
    def blur(self, amount):
        image = Image.open(self.getImageData())
        fmt = image.format
        for x in range(0, int(amount)):
            image = image.filter(ImageFilter.BLUR)
            
        output = StringIO()
        image.save(output, fmt)
        self.setImage(output)
        
    @kssaction
    def compress(self, amount):
        image = Image.open(self.getImageData())

        output = StringIO()
        image.save(output, image.format, quality=int(amount))
        self.setImage(output)
        
    @kssaction
    def contrast(self, amount):
        image = Image.open(self.getImageData())
        enhancer = ImageEnhance.Contrast(image)
        newImage = enhancer.enhance(float(amount)/100.0)

        output = StringIO()
        newImage.save(output, image.format)
        self.setImage(output)

    @kssaction
    def brightness(self, amount):
        image = Image.open(self.getImageData())
        enhancer = ImageEnhance.Brightness(image)
        newImage = enhancer.enhance(float(amount)/100.0)

        output = StringIO()
        newImage.save(output, image.format)
        self.setImage(output)

    @kssaction
    def sharpen(self, amount):
        image = Image.open(self.getImageData())
        enhancer = ImageEnhance.Sharpness(image)
        newImage = enhancer.enhance(float(amount))

        output = StringIO()
        newImage.save(output, image.format)
        self.setImage(output)

    @kssaction
    def imageFlipOnHorizontalAxis(self):
        original = Image.open(self.getImageData())
        image = original.transpose(Image.FLIP_LEFT_RIGHT)
        
        output = StringIO()
        image.save(output, original.format)
        self.setImage(output)

    @kssaction
    def imageResizeSave(self, width, height):
        image = Image.open(self.getImageData())
        format = image.format
        size=( int(width), int(height) )
        image = image.resize(size, Image.ANTIALIAS)
        data = StringIO()
        image.save(data, format)
        data.seek(0)
        
        self.setImage(data)
    
    @kssaction
    def imageCropSave(self, topLeftX, topLeftY, bottomRightX, bottomRightY):
        image = Image.open(self.getImageData())
        format = image.format
        box = (int(topLeftX), int(topLeftY), int(bottomRightX), int(bottomRightY))
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
        image = Image.open(self.getImageData())
        format = image.format
        size=( int(width), int(height) )
        image = image.resize(size, Image.ANTIALIAS)
        data = StringIO()
        image.save(data, format)

        data.seek(0)
        
        #crop
        image = Image.open(StringIO(data.read()))
        format = image.format
        box = (int(topLeftX), int(topLeftY), int(bottomRightX), int(bottomRightY))
        new_image = image.crop(box=box)
        new_image.load()
        cropped_output = StringIO()
        format = format and format or default_format
        new_image.save(cropped_output, format)
        cropped_output.seek(0)
        
        self.setImage(cropped_output)
        
class UnredoStack:

    def __init__(self, bottom):
        self.pos = 0
        self.stack = [bottom]

    def do(self, value):
        if self.canRedo():
            #clear top
            for item in self.stack[(self.pos+1):len(self.stack)]:
                self.stack.remove(item)

        self.stack.append(value)
        self.pos = self.pos + 1

    def getCurrent(self):
        return self.stack[self.pos]

    def undo(self):
        self.pos = self.pos - 1

    def canUndo(self):
        return self.pos > 0

    def redo(self):
        self.pos = self.pos + 1

    def canRedo(self):
        return self.pos + 1 < len(self.stack)
        
def GetSize(data):
    size = len(data)

    size = size/1024

    if size > 1024:
        return str(size/1024)[0:4] + 'mb'
    else:
        return "Size: " + str(size)[0:4] + 'kb'