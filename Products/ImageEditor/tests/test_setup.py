from Products.ImageEditor.tests.base import ImageEditorTestCase
from Products.CMFCore.utils import getToolByName
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from zope.component import getUtility
from Products.ImageEditor.Extensions import Install

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

    def test_should_not_install_collective_js_jquery_if_plone33(self):
        # need to call this specifically because test setup doesn't dynamically install it for us
        Install.install(self.portal)
        pm = getToolByName(self.portal, 'portal_migration')
        qi = getToolByName(self.portal, 'portal_quickinstaller')
        
        version = pm.getInstanceVersion()
        major, minor = int(version[0]), int(version[2])

        if major >= 3 and minor >= 3:
            self.failUnless(not qi.isProductInstalled('collective.js.jquery'))
        else:
            self.failUnless(qi.isProductInstalled('collective.js.jquery'))
            
    def test_should_install_collective_js_jqueryui(self):
        qi = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(qi.isProductInstalled('collective.js.jqueryui'))

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSetup))
    return suite
