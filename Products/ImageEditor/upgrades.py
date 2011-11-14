from Products.CMFCore.utils import getToolByName


default_profile = 'profile-Products.ImageEditor:default'
to_1_2_profile = 'profile-Products.ImageEditor:upgrade_to_1_2'
to_1_8_profile = 'profile-Products.ImageEditor:upgrade_to_1_8'
ie_views = ['imageeditor', 'imageeditor.alagimp',
            'imageeditor.inline', 'imageeditor.slider']


def remove_stack_pos_and_unredostack_from_images_in_catalog(catalog):
    images = catalog.searchResults(portal_type=["Image"])

    for image in images:
        image = image.getObject()

        if hasattr(image, 'stack_pos'):
            delattr(image, 'stack_pos')

        if hasattr(image, 'unredostack'):
            delattr(image, 'unredostack')

        image._p_changed = 1


def remove_image_editor_tab(portal):
    portal_actions = getToolByName(portal, 'portal_actions')
    object_buttons = portal_actions.object

    actions_to_remove = ('image_editor',)
    for action in actions_to_remove:
        if action in object_buttons.objectIds():
            object_buttons.manage_delObjects([action])


def remove_visual_editor_tab(portal):
    portal_types = getToolByName(portal, 'portal_types')
    actions = list(portal_types.Image._actions[:])

    if 'object/editor' in [a.category + "/" + a.id for a in actions]:
        action = None
        for a in actions:
            if a.id == 'editor' and a.category == 'object':
                action = a
                break

        actions.remove(action)
        portal_types.Image._actions = tuple(actions)
        portal_types.Image._p_changed = 1


def upgrade_to_1_2(context):
    portal = getToolByName(context, 'portal_url').getPortalObject()

    catalog = getToolByName(portal, 'portal_catalog')
    remove_stack_pos_and_unredostack_from_images_in_catalog(catalog)
    remove_image_editor_tab(portal)
    remove_visual_editor_tab(portal)

    context.runAllImportStepsFromProfile(to_1_2_profile)
    context.runAllImportStepsFromProfile(default_profile)


def upgrade_to_1_3(context):
    context.runImportStepFromProfile(default_profile, 'jsregistry')


def set_unintrusive_jqueryui_properties(portal, global_include=None):
    pprops = getToolByName(portal, 'portal_properties')
    jq_props = pprops.jqueryui_properties
    if global_include is not None:
        jq_props.global_include = global_include

    jq_props.views_and_templates = tuple(set(
        jq_props.getProperty('views_and_templates', [])) | set(ie_views))


def upgrade_to_1_7(context):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    qi = getToolByName(portal, 'portal_quickinstaller')

    if not qi.isProductInstalled('collective.js.jqueryui'):
        qi.installProduct('collective.js.jqueryui')
        set_unintrusive_jqueryui_properties(portal, global_include=False)
    else:
        pprops = getToolByName(portal, 'portal_properties')
        if 'jqueryui_properties' not in pprops.objectIds():
            # installed, but not upgraded
            from collective.js.jqueryui.upgrades import upgrade_1891_1892
            upgrade_1891_1892(context)


def upgrade_to_1_8(context):
    context.runAllImportStepsFromProfile(to_1_8_profile)


def upgrade_to_2_0(context):
    pass
