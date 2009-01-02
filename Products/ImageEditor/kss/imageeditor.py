from plone.app.kss.interfaces import IPloneKSSView
from plone.app.kss.plonekssview import PloneKSSView
from kss.core import kssaction
from zope.interface import implements
from Products.ImageEditor.interfaces.imageeditor import IImageEditorAdapter
import random
from Products.CMFCore.utils import getToolByName

def _(s):
    """
    takes a string and returns the int that PIL likes
    """
    return int(float(s))


class ImageEditorKSS(PloneKSSView):
    implements(IPloneKSSView)

    def __init__(self, *args, **kwargs):
        super(PloneKSSView, self).__init__(*args, **kwargs)
        
        self.imageeditor = IImageEditorAdapter(self.context)

    def callSetImageCommand(self):
        """
        
        """
        imageCommands = self.getCommandSet('imageeditor')
        ksscore = self.getCommandSet('core')
        
        imageInfo = self.imageeditor.getCurrentImageInfo()
        
        imageCommands.setImage(
            ksscore.getSameNodeSelector(), 
            self.context.absolute_url() + "/currenteditedimage.jpg?" + str(random.randint(0, 1000000)),
            str(int(self.imageeditor.unredo.canUndo())),
            str(int(self.imageeditor.unredo.canRedo())),
            str(int(self.imageeditor.unredo.pos > 0)),
            imageInfo['sizeformatted'],
            str(imageInfo['width']),
            str(imageInfo['height'])
        )
        
    @kssaction
    def saveImageEdit(self):          
        #force versioning to kick in
        portal_repository = getToolByName(self.context, 'portal_repository')
        if portal_repository.isVersionable(self.context):
            portal_repository.save(self.context, comment = "saved from image editor")
        
        self.imageeditor.saveEdit()
        self.context.reindexObject() #stop image caching on browser
        
        self.callSetImageCommand()
    
    @kssaction 
    def cancelImageEdit(self):
        self.imageeditor.clearEdits()
        self.callSetImageCommand()
        
    @kssaction
    def redoImageEdit(self):
        self.imageeditor.redo()
        self.callSetImageCommand()

    @kssaction 
    def undoImageEdit(self):
        self.imageeditor.undo()
        self.callSetImageCommand()

    @kssaction
    def rotateImageLeft(self):
        self.imageeditor.rotateLeft()
        self.callSetImageCommand()
        
    @kssaction
    def rotateImageRight(self):
        self.imageeditor.rotateRight()
        self.callSetImageCommand()

    @kssaction
    def imageFlipOnVerticalAxis(self):
        self.imageeditor.flipOnVerticalAxis()
        self.callSetImageCommand()
        
    @kssaction
    def blur(self, amount):
        self.imageeditor.blur(_(amount))
        self.callSetImageCommand()
        
    @kssaction
    def compress(self, amount):
        self.imageeditor.compress(_(amount))
        self.callSetImageCommand()
        
    @kssaction
    def contrast(self, amount):
        self.imageeditor.contrast(float("." + amount)*2.0)
        self.callSetImageCommand()
        
    @kssaction
    def brightness(self, amount):
        self.imageeditor.brightness(float("." + amount)*2.0)
        self.callSetImageCommand()

    @kssaction
    def sharpen(self, amount):
        self.imageeditor.sharpen(float(amount))
        self.callSetImageCommand()
        
    @kssaction
    def imageFlipOnHorizontalAxis(self):
        self.imageeditor.flipOnHorizontalAxis()
        self.callSetImageCommand()

    @kssaction
    def imageResizeSave(self, width, height):
        self.imageeditor.resize(_(width), _(height))
        self.callSetImageCommand()
        
    @kssaction
    def imageCropSave(self, topLeftX, topLeftY, bottomRightX, bottomRightY):
        self.imageeditor.crop(_(topLeftX), _(topLeftY), _(bottomRightX), _(bottomRightY))
        self.callSetImageCommand()
        
    @kssaction
    def cropAndResize(self, topLeftX, topLeftY, bottomRightX, bottomRightY, width, height):
        self.imageeditor.resize(_(width), _(height))
        self.imageeditor.crop(_(topLeftX), _(topLeftY), _(bottomRightX), _(bottomRightY))
        self.callSetImageCommand()
        
    @kssaction
    def addDropShadow(self):
        self.imageeditor.dropshadow()
        self.callSetImageCommand()