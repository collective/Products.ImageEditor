from Products.ATContentTypes.interface.image import IImageContent
from OFS.SimpleItem import SimpleItem
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.interface import implements
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from time import gmtime, strftime
from Products.ImageEditor.interfaces.imageeditor import *
from Products.CMFCore.utils import getToolByName
from Products.ImageEditor.meta.zcml import get_actions, get_action_class
from zope.formlib import form
from plone.memoize.view import memoize
from Products.ImageEditor.utils import *

class NewEdit(BrowserView):
    
    template = ViewPageTemplateFile('imageeditor.pt')
    
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        
        self.editor = IImageEditorAdapter(self.context)
        self.actions = [(name, action.class_(self.context)) for name, action in get_actions()]
        
    def get_buttons(self):
        html = ''
        
        for name, action in self.actions:
            html += """
<input class="edit-button" 
       id="%(normal_name)s-button" 
       type="button" 
       name="%(normal_name)s"
       alt="%(title)s"
       style="background-image: url(%(icon)s);"
       value="%(name)s" 
/>
            """ % {
                'name' : action.name,
                'normal_name' : name,
                'icon' : action.icon,
                'title' : action.description
            }
            
        return html
    
    def get_options(self):
        html = ''
        
        for name, action in self.actions:
            html += '<div class="image-edit-action" id="%s-options">' % name
            widgets = form.setUpInputWidgets(
                action.options, 
                name,
                self.context,
                self.request,
                ignore_request=True
            )
            
            for widget in widgets:
                html += """
<div class="edit-option">
    <label class="formQuestion" for="%s.%s">%s</label>
    <div class="formHelp">%s</div>
    %s
</div>
                """ % (
                    name,
                    widget.name,
                    widget.context.title.default,
                    widget.context.description.default,
                    widget()
                )
            
            if not action.skip_apply:
                html += """
<input type="button" id="%(name)s-apply-button" 
       class="image-edit-apply-button" name="%(name)s" 
       value="Apply" 
/>
                """ % {'name': name}
            
            html += '</div>'
            
        return html
    
    def setup_js(self):
        setup_js = []
        
        for name, action in self.actions:
            js = action.on_setup()
            if js:
                setup_js.append(js)

        return """
var IMAGE_INFORMATION = %s;
(function($){
$(document).ready(function(){

%s

});
})(jQuery);
        """ % (json(get_image_information(self.editor)), '\n'.join(setup_js))
        
    def custom_action_parameters(self):
        params = []
        
        for name, action in self.actions:
            ap = action.action_parameters()
            if ap:
                params.append("ACTION_PARAMETERS['%s'] = %s;" % (name, ap))
        
        return """
var ACTION_PARAMETERS = {};
%s    
        """ % '\n'.join(params)
        
    @memoize
    def image_url(self):
        """
        This is used because sometimes browsers cache images that may have been edited
        """
        return generate_random_url(self.context)
    
    def __call__(self):
        return self.template()

class ShowCurrentEdit(BrowserView):
    """
    Just a browser view to get latest edited image
    """
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.imageeditor = IImageEditorAdapter(context)

    def __call__(self):
        
        resp = self.request.response
        imagedata = self.imageeditor.get_current_image_data()
        resp.setHeader('Content-Type', 'image/jpeg')
        resp.setHeader('Content-Length', len(imagedata))
        resp.setHeader('Last-Modified', strftime('%a, %d %b %Y %H:%M:%S +0000', gmtime()))
        resp.write(imagedata)
        return ''
    
    
class ImageEditorActionContext(SimpleItem):
    # Implementing IBrowserPublisher tells the Zope 2 publish traverser to pay attention
    # to the publishTraverse and browserDefault methods.
    implements(IImageEditorActionContext, IBrowserPublisher)
    
    def __init__(self, context, request, action_name):
        super(ImageEditorActionContext, self).__init__(context, request)
        self.context = context
        self.request = request
        self.action_name = action_name

    def browserDefault(self, request):
        """ always use the execute view of the action--there is no other.
        """
        return self, ('@@execute',)

    def absolute_url(self):
        return self.context.absolute_url() + "/image-editor/" + self.action_name
    
class ImageEditorContext(SimpleItem):
    # Implementing IBrowserPublisher tells the Zope 2 publish traverser to pay attention
    # to the publishTraverse and browserDefault methods.
    implements(IImageEditorContext, IBrowserPublisher)
        
    def publishTraverse(self, traverse, action_name):
        """ Look up the action name whose name matches the next URL and wrap it.
        """
        return ImageEditorActionContext(self.context, self.request, action_name).__of__(self)

    def browserDefault(self, request):
        """ Should never get here!
        """
        raise Exception("no action specified")

    def absolute_url(self):
        return self.context.absolute_url() + "/image-editor"
    
class ImageEditorActionExecute(BrowserView):
    
    def get_args_from_request(self):
        args = {}
        
        for key in self.request.keys():
            if key.startswith(self.context.action_name + "."):
                args[key.split('.')[1]] = self.request.get(key)
                
        return args
        
    
    def __call__(self):
        #get action instance
        action = get_action_class(self.context.action_name)(self.context.context)
        #call instance with params
        action(**self.get_args_from_request())
        
        return json(get_image_information(action.editor))

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
                request.get('ACTUAL_URL').endswith('@@editor')
