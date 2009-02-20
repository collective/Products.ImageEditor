from Products.CMFCore.utils import getToolByName

def install(portal, reinstall=False):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.ImageEditor:default')

def uninstall(portal, reinstall=False):
    """
    remove any possible left-overs from the image editor on Image types
    """
    
    if not reinstall:
        catalog = getToolByName(portal, 'portal_catalog')
        
        images = catalog.searchResults(portal_type=["Image"])
        
        for image in images:
            image = image.getObject()
            
            if hasattr(image, 'stack_pos'):
                delattr(image, 'stack_pos')
                
            if hasattr(image, 'unredostack'):
                delattr(image, 'unredostack')
                
            image._p_changed
            
            
