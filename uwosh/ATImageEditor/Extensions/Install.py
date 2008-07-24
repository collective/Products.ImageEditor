from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
from collective.plonetruegallery.content.config import *

def beforeUninstall(self, cascade, product, reinstall):
    out = StringIO()
    
    return out.getvalue(), cascade

def afterInstall(self, reinstall=False, **kwargs):
    out = StringIO()
    
    pt = self.portal_types
    imct = pt['Image']    

    imct.addAction(
        id = 'editor',
        name = 'Visual Transform',
        action = "string:${object_url}/editor",
        permission = "Modify portal content",
        category = "object",
        condition = "object/hasPIL"
    )
            
    return out.getvalue()