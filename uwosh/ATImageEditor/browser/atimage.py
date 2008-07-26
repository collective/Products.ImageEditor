from zope.interface import implements

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.kss.interfaces import IPloneKSSView
from plone.app.kss.plonekssview import PloneKSSView
from kss.core import kssaction
from PIL import Image
from cStringIO import StringIO
import random

class Edit(BrowserView):

    template = ViewPageTemplateFile('atimage_edit.pt')

    def __call__(self):
        return self.template()
        
    def image_url(self):
        """
        This is used because sometimes browsers cache images that may have been edited
        """
        return self.context.absolute_url() + "?" + str(random.randint(0, 1000))
        
        
class ATImageKSS(PloneKSSView):
    implements(IPloneKSSView)

    def getImageData(self):
        return self.context.getImage().getImageAsFile()

    def reloadImage(self):
        atimageCommands = self.getCommandSet('atimage')
        ksscore = self.getCommandSet('core')
        atimageCommands.reloadImage(ksscore.getSameNodeSelector())

    @kssaction
    def rotateImageLeft(self):
        original = Image.open(self.getImageData())
        image = original.rotate(90)
        
        output = StringIO()
        image.save(output, original.format)
        
        self.context.setImage(output)
        
        self.reloadImage()
        
    @kssaction
    def rotateImageRight(self):
        original = Image.open(self.getImageData())
        image = original.rotate(270)
        
        output = StringIO()
        image.save(output, original.format)
        
        self.context.setImage(output)
        self.reloadImage()

    @kssaction
    def imageFlipOnVerticalAxis(self):
        original = Image.open(self.getImageData())
        image = original.transpose(Image.FLIP_TOP_BOTTOM)
        
        output = StringIO()
        image.save(output, original.format)
        
        self.context.setImage(output)
        self.reloadImage()
        
    @kssaction
    def imageFlipOnHorizontalAxis(self):
        original = Image.open(self.getImageData())
        image = original.transpose(Image.FLIP_LEFT_RIGHT)
        
        output = StringIO()
        image.save(output, original.format)
        
        self.context.setImage(output)
        self.reloadImage()

    @kssaction
    def imageResizeSave(self, width, height):
        image = Image.open(self.getImageData())
        format = image.format
        size=( int(width), int(height) )
        image = image.resize(size, Image.ANTIALIAS)
        data = StringIO()
        image.save(data, format)
        data.seek(0)
        
        self.context.setImage(data)
        self.reloadImage()
    
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
        
        self.context.setImage(cropped_output)
        self.reloadImage()
        
    @kssaction
    def cropAndResize(self, topLeftX, topLeftY, bottomRightX, bottomRightY, width, height):
        #resize
        image = Image.open(self.getImageData())
        format = image.format
        size=( int(width), int(height) )
        image = image.resize(size,Image.ANTIALIAS)
        data = StringIO()
        image.save(data, format)

        data.seek(0)
        
        self.context.setImage(data)
        
        #crop
        image = Image.open(self.getImageData())
        format = image.format
        box = (int(topLeftX), int(topLeftY), int(bottomRightX), int(bottomRightY))
        new_image = image.crop(box=box)
        new_image.load()
        cropped_output = StringIO()
        format = format and format or default_format
        new_image.save(cropped_output, format)
        cropped_output.seek(0)
        
        self.context.setImage(cropped_output)
        self.reloadImage()