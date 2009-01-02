from Products.CMFCore.utils import getToolByName
from StringIO import StringIO

def beforeUninstall(self, cascade, product, reinstall):
    out = StringIO()
    
    return out.getvalue(), cascade

def afterInstall(self, reinstall=False, **kwargs):
    out = StringIO()
    
    #done with generic setup -- the way it should be done...
    
    return out.getvalue()