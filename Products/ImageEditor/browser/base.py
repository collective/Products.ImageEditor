from plone.memoize.view import memoize
from Products.Five.browser import BrowserView
from Products.ImageEditor.interfaces.imageeditor import IImageEditorAdapter
from Products.ImageEditor.meta.zcml import get_actions
from Products.ImageEditor.utils import generate_random_url
from Products.ImageEditor.utils import get_image_information
from Products.ImageEditor.utils import json
from zope.formlib import form
from Products.CMFCore.utils import getToolByName
import zope.i18n
from Products.ImageEditor import translationstrings as ts


class ImageEditor(BrowserView):
    """Redirect based on the user preferences"""
    def __call__(self, *args, **kwargs):
        pm = getToolByName(self.context, 'portal_membership')
        member = pm.getAuthenticatedMember()
        pref = 'alagimp'
        if member is not None:
            pref = member.getProperty('image_editor', 'alagimp')
        self.request.response.redirect('@@imageeditor.%s' % pref)
        return ''


class Base(BrowserView):
    """Basic view for image editor"""

    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.editor = IImageEditorAdapter(self.context)
        self.editor.set_field(request.get('field', ''))
        self.actions = [(name, action.class_(self.context)) \
                                for name, action in get_actions()]

    @memoize
    @property
    def jqueryui_installed(self):
        """
        if collective.js.jqueryui is installed we don't have to manually
        include the javascript/css
        """
        qi = getToolByName(self.context, 'portal_quickinstaller')
        return qi.productInstalled('collective.js.jqueryui')

    def get_buttons(self):
        buttons = []
        for name, action in self.actions:
            info = {
                'id': name + '-button',
                'value': zope.i18n.translate(action.name),
                'name': zope.i18n.translate(name),
                'alt': zope.i18n.translate(action.description),
            }
            if action.icon:
                info['style'] = "background-image: url(%s)" % action.icon
            buttons.append(info)
        return buttons

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
                    zope.i18n.translate(widget.context.title),
                    zope.i18n.translate(widget.context.description),
                    widget()
                )

            if not action.skip_apply:
                html += """
<input type="button" id="%(name)s-apply-button"
       class="image-edit-apply-button" name="%(name)s"
       value="%(apply)s"
/>
                """ % {'name': name, 'apply': zope.i18n.translate(ts.Apply)}

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
        This is used because sometimes browsers cache
        images that may have been edited
        """
        return generate_random_url(self.context)
