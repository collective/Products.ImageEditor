from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
try:
    from collective.js.jqueryui.interfaces import IJQueryUIPlugins
    HAS_NEW_JQUI = True
except ImportError:
    HAS_NEW_JQUI = False


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


jqui_plugins = [
    'ui_widget',
    'ui_mouse',
    "ui_position",
    "ui_draggable",
    "ui_droppable",
    "ui_resizable",
    "ui_selectable",
    "ui_sortable",
    "ui_button",
    "ui_dialog",
    "ui_slider"
]

def activate_jqui_plugins():
    if not HAS_NEW_JQUI:
        return
    registry = getUtility(IRegistry)
    proxy = registry.forInterface(IJQueryUIPlugins)
    for plugin in jqui_plugins:
        setattr(proxy, plugin, True)


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


def upgrade_to_1_7(context):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    qi = getToolByName(portal, 'portal_quickinstaller')

    if not qi.isProductInstalled('collective.js.jqueryui'):
        qi.installProduct('collective.js.jqueryui')


def upgrade_to_1_8(context):
    context.runAllImportStepsFromProfile(to_1_8_profile)


def upgrade_to_2_0(context):
    activate_jqui_plugins()
