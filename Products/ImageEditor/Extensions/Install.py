from Products.CMFCore.utils import getToolByName
from Products.ImageEditor import dependencies

def install(portal, reinstall=False):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.ImageEditor:default')
    
    qi = getToolByName(portal, 'portal_quickinstaller')

    for d in dependencies:
        if qi.isProductInstallable(d) and not qi.isProductInstalled(d):
            qi.installProduct(d)


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
                
            image._p_changed = 1
            
            
        portal_actions = getToolByName(portal, 'portal_actions')
        object_buttons = portal_actions.object

        actions_to_remove = ('image_editor',)
        for action in actions_to_remove:
            if action in object_buttons.objectIds():
                object_buttons.manage_delObjects([action])
                
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.ImageEditor:uninstall')