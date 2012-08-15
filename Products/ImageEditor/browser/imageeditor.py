from Products.ATContentTypes.interface.image import IImageContent
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.ImageEditor.interfaces import IImageEditorAdapter
from Products.ImageEditor.interfaces import IImageEditorUtility
from Products.ImageEditor.meta.zcml import get_action_class
from Products.ImageEditor.utils import json
from Products.ImageEditor.utils import get_image_information
from plone.memoize.view import memoize
from time import gmtime, strftime
from zope.interface import implements


class ShowCurrentEdit(BrowserView):
    """
    Just a browser view to get latest edited image
    """
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.imageeditor = IImageEditorAdapter(context)
        self.imageeditor.set_field(request.get('field', ''))

    def __call__(self):
        resp = self.request.response
        imagedata = self.imageeditor.get_current_image_data()
        resp.setHeader('Content-Type', 'image/jpeg')
        resp.setHeader('Content-Length', len(imagedata))
        resp.setHeader('Last-Modified',
            strftime('%a, %d %b %Y %H:%M:%S +0000', gmtime()))
        resp.write(imagedata)
        return ''


class ImageEditorActionExecute(BrowserView):

    def get_args_from_request(self, action):
        args = {}

        for key in self.request.keys():
            if key.startswith(action + "."):
                args[key.split('.')[1]] = self.request.get(key)

        return args

    def __call__(self, action_name):
        #get action instance
        action = get_action_class(action_name)(self.context)
        #call instance with params
        result = action(**self.get_args_from_request(action_name)) or {}

        result.update(get_image_information(action.editor))
        result['previous_action'] = action_name

        resp = self.request.response
        resp.setHeader('Cache-Control', 'no-cache')
        resp.setHeader('Pragma', 'no-cache')
        return json(result)


class ImageEditorUtility(BrowserView):
    """Traversable utility for image editor
    """
    implements(IImageEditorUtility)

    @memoize
    def editable(self):
        pm = getToolByName(self.context, 'portal_membership')

        return IImageContent.providedBy(self.context) and not \
                pm.isAnonymousUser()

    @memoize
    def should_include(self, request):
        pm = getToolByName(self.context, 'portal_membership')

        return IImageContent.providedBy(self.context) and \
                not pm.isAnonymousUser() and \
                '/@@imageeditor.' in request.get('ACTUAL_URL')
