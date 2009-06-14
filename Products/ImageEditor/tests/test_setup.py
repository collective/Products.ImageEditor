import unittest
from Products.ImageEditor.tests.base import ImageEditorTestCase
from Products.CMFCore.utils import getToolByName
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from zope.component import getUtility

class TestSetup(ImageEditorTestCase):
    """Test if install of the product is well done"""
    
    def test_css_registry(self):
        pcss = self.portal.portal_css
        self.failUnless('++resource++imageeditor-style.css' in [css.getId() for css in pcss.getResources()])

    def test_actions(self):
        actionTool = self.portal.portal_actions
        actionInfo = actionTool.getActionInfo(['object/image_editor'])
        self.failUnless(actionInfo['url'] == "/@@editor")

    def test_js_added(self):
        pjavascripts = getToolByName(self.portal, 'portal_javascripts')
        self.failUnless('++resource++imageeditor.js' in [js.getId() for js in pjavascripts.getResources()])
        self.failUnless('++resource++jquery.imgareaselect-0.8.min.js' in [js.getId() for js in pjavascripts.getResources()])
        self.failUnless('++resource++imageeditor.js' in [js.getId() for js in pjavascripts.getResources()])

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
