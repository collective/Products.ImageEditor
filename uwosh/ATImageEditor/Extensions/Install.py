from Products.CMFCore.utils import getToolByName
from StringIO import StringIO

def beforeUninstall(self, cascade, product, reinstall):
    out = StringIO()
    
    return out.getvalue(), cascade

def afterInstall(self, reinstall=False, **kwargs):
    out = StringIO()
    
    pt = self.portal_types
    imct = pt.Image

    editorAction = [action for action in imct.listActions() if action.id == 'editor']
    if len(editorAction) == 0:
        imct.addAction(
            id = 'editor',
            name = 'Visual Transform',
            action = "string:${object_url}/editor",
            permission = "Modify portal content",
            category = "object",
            condition = "object/hasPIL"
        )
    
    transform_action = [action for action in imct._actions if action.id == 'transform'][0]
    transform_action.visible = False

    return out.getvalue()