from Products.CMFCore.utils import getToolByName

def uninstall_import(context):
    
    if context.readDataFile('Products.ImageEditor.txt') is None:
        return

    portal = context.getSite()
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