from zope.interface import implements
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import random
from time import gmtime, strftime
from Products.ImageEditor.interfaces.imageeditor import IImageEditorAdapter
from PIL import Image
from Products.CMFCore.utils import getToolByName

def _(s):
    """
    takes a string and returns the int that PIL likes
    """
    return int(float(s))

class Edit(BrowserView):

    template = ViewPageTemplateFile('imageeditor.pt')

    def __init__(self, *args, **kwargs):
        super(BrowserView, self).__init__(*args, **kwargs)
        
        self.imageeditor = IImageEditorAdapter(self.context)
        
        # always start with new image
        # not sure if this is desired or not 
        # this way, old edits are removed
        self.imageeditor.clearEdits()

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
        return str(self.imageeditor.getCurrentImage().format != "PNG")

    def getSize(self):
        return self.imageeditor.getCurrentImageInfo()['sizeformatted']

class ShowCurrentEdit(BrowserView):
    """
    Just a browser view to get latest edited image
    """
    def __init__(self, *args, **kwargs):
        super(BrowserView, self).__init__(*args, **kwargs)
        self.imageeditor = IImageEditorAdapter(self.context)

    def __call__(self):
        
        resp = self.request.response
        imagedata = self.imageeditor.getCurrentImageData()
        resp.setHeader('Content-Type', 'image/jpeg')
        resp.setHeader('Content-Length', len(imagedata))
        resp.setHeader('Last-Modified', strftime('%a, %d %b %Y %H:%M:%S +0000', gmtime()))
        resp.write(imagedata)
        return ''
    
class AJAX(BrowserView):
    
    def __init__(self, context, request):
        super(AJAX, self).__init__(context, request)
        
        self.imageeditor = IImageEditorAdapter(self.context)
    
    def getImageInfo(self):
        
        imageInfo = self.imageeditor.getCurrentImageInfo()
        
        return str({
            'url' : self.context.absolute_url() + "/currenteditedimage.jpg?" + str(random.randint(0, 1000000)),
            'canUndo' : str(int(self.imageeditor.unredo.canUndo())),
            'canRedo' : str(int(self.imageeditor.unredo.canRedo())),
            'canSave' : str(int(self.imageeditor.unredo.pos > 0)),
            'size' : imageInfo['sizeformatted'],
            'width' : str(imageInfo['width']),
            'height' : str(imageInfo['height'])
        })
    
    def saveImageEdit(self):          
        #force versioning to kick in
        portal_repository = getToolByName(self.context, 'portal_repository')
        if portal_repository.isVersionable(self.context):
            portal_repository.save(self.context, comment = "saved from image editor")
        
        self.imageeditor.saveEdit()
        self.context.reindexObject() #stop image caching on browser
        
        return self.getImageInfo()
    
    def cancelImageEdit(self):
        self.imageeditor.clearEdits()
        return self.getImageInfo()
        
    def redoImageEdit(self):
        self.imageeditor.redo()
        return self.getImageInfo()

    def undoImageEdit(self):
        self.imageeditor.undo()
        return self.getImageInfo()

    def rotateImageLeft(self):
        self.imageeditor.rotateLeft()
        return self.getImageInfo()
        
    def rotateImageRight(self):
        self.imageeditor.rotateRight()
        return self.getImageInfo()

    def imageFlipOnVerticalAxis(self):
        self.imageeditor.flipOnVerticalAxis()
        return self.getImageInfo()
        
    def blur(self, amount):
        self.imageeditor.blur(_(amount))
        return self.getImageInfo()
        
    def compress(self, amount):
        self.imageeditor.compress(_(amount))
        return self.getImageInfo()
        
    def contrast(self, amount):
        self.imageeditor.contrast(float("." + amount)*2.0)
        return self.getImageInfo()
        
    def brightness(self, amount):
        self.imageeditor.brightness(float("." + amount)*2.0)
        return self.getImageInfo()

    def sharpen(self, amount):
        self.imageeditor.sharpen(float(amount))
        return self.getImageInfo()
        
    def imageFlipOnHorizontalAxis(self):
        self.imageeditor.flipOnHorizontalAxis()
        return self.getImageInfo()

    def imageResizeSave(self, width, height):
        self.imageeditor.resize(_(width), _(height))
        return self.getImageInfo()
        
    def imageCropSave(self, x1, y1, x2, y2):
        self.imageeditor.crop(_(x1), _(y1), _(x2), _(y2))
        return self.getImageInfo()
        
    def cropAndResize(self, x1, y1, x2, y2, width, height):
        self.imageeditor.resize(_(width), _(height))
        self.imageeditor.crop(_(x1), _(y1), _(x2), _(y2))
        return self.getImageInfo()
        
    def addDropShadow(self):
        self.imageeditor.dropshadow()
        return self.getImageInfo()