# -*- coding: utf-8 -*-

from plone import api
from plone.browserlayer.utils import registered_layers
from Products.ImageEditor.testing import INTEGRATION_TESTING

import unittest2 as unittest

EXPECTED_JS = u'++resource++imageeditor/editlink.js'


class SetupTestCase(unittest.TestCase):
    """Test if install of the product is well done"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

    def test_actions(self):
        actionTool = self.portal['portal_actions']
        with api.env.adopt_roles(['Manager']):
            actionInfo = actionTool.getActionInfo(['object/image_editor'])
        self.assertEqual(actionInfo['url'], '/@@imageeditor.alagimp')

    def test_addon_layer_is_registered(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertIn('IImageEditorLayer', layers)

    def test_js_added(self):
        portal_js = self.portal['portal_javascripts']
        actual_js = portal_js.getResourceIds()
        self.assertIn(EXPECTED_JS, actual_js)

    def test_should_install_collective_js_jqueryui(self):
        self.assertTrue(self.qi.isProductInstalled('collective.js.jqueryui'))

    def test_edit_images_permission(self):
        permission = 'Product.ImageEditor: Edit Images'
        roles = self.portal.rolesOfPermission(permission)
        roles = [r['name'] for r in roles if r['selected']]
        expected_roles = ['Editor', 'Manager', 'Owner', 'Site Administrator']
        self.assertListEqual(roles, expected_roles)


class UninstallTestCase(unittest.TestCase):
    """Ensure product is properly uninstalled."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.qi.uninstallProducts(products=['ImageEditor'])

    def test_should_remove_action_object_on_uninstall_profile(self):
        actionTool = self.portal['portal_actions']
        object_actions = actionTool.object
        self.assertNotIn(u'image_editor', object_actions.objectIds())

    def test_addon_layer_is_unregistered(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertNotIn('IImageEditorLayer', layers)

    def test_should_remove_javascript_on_uninstall_profile(self):
        portal_js = self.portal['portal_javascripts']
        actual_js = portal_js.getResourceIds()
        self.assertNotIn(EXPECTED_JS, actual_js)
