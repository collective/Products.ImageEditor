from zope.interface import implements
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import random
from time import gmtime, strftime
from Products.ImageEditor.interfaces.imageeditor import IImageEditorAdapter
from PIL import Image

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
    