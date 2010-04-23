from Products.ImageEditor.tests.base import ImageEditorTestCase
from Products.CMFCore.utils import getToolByName


class TestSetup(ImageEditorTestCase):
    """Test if install of the product is well done"""
    
    def test_actions(self):
        actionTool = self.portal.portal_actions
        actionInfo = actionTool.getActionInfo(['object/image_editor'])
        self.failUnless(actionInfo['url'] == "/@@imageeditor")

    def test_js_added(self):
        pjavascripts = getToolByName(self.portal, 'portal_javascripts')
        self.failUnless('++resource++jquery.imgareaselect-0.8.min.js' not in [js.getId() for js in pjavascripts.getResources()])

    def test_should_install_collective_js_jqueryui(self):
        qi = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(qi.isProductInstalled('collective.js.jqueryui'))

    def test_should_remove_action_object_on_uninstall_profile(self):
        self.uninstall()
        actionTool = self.portal.portal_actions
        object_actions = actionTool.object
        self.assertEquals('image_editor' in object_actions.objectIds(), False)
        
    def test_should_remove_javascript_on_uninstall_profile(self):
        self.uninstall()
        pjavascripts = getToolByName(self.portal, 'portal_javascripts')
        jsresources = [js.getId() for js in pjavascripts.getResources()]
        self.failUnless('++resource++jquery.imgareaselect-0.8.min.js' not in jsresources)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSetup))
    return suite
