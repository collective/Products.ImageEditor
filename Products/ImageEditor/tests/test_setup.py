import unittest
from Products.ImageEditor.tests.base import ImageEditorTestCase
from Products.CMFCore.utils import getToolByName
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from zope.component import getUtility

class TestSetup(ImageEditorTestCase):
    """
    
    """
    
    def test_jquery_css_added(self):
        pcss = getToolByName(self.portal, 'portal_css')
        self.failUnless('++resource++jquery.ui.all.css' in [css.getId() for css in pcss.getResources()])

    def test_editor_css_added(self):
        pcss = getToolByName(self.portal, 'portal_css')
        self.failUnless('++resource++imageeditor-style.css' in [css.getId() for css in pcss.getResources()])

    def test_kss_added(self):
        kcss = getToolByName(self.portal, 'portal_kss')
        self.failUnless('++resource++imageeditor.kss' in [kss.getId() for kss in kcss.getResources()])
        
    def test_js_added(self):
        pjavascripts = getToolByName(self.portal, 'portal_javascripts')
        self.failUnless('++resource++jquery-1.2.6.js' in [js.getId() for js in pjavascripts.getResources()])
        self.failUnless('++resource++jquery-ui-imageeditor.min.js' in [js.getId() for js in pjavascripts.getResources()])
        self.failUnless('++resource++jquery.imgareaselect-0.4.2.min.js' in [js.getId() for js in pjavascripts.getResources()])
        self.failUnless('++resource++imageeditor.js' in [js.getId() for js in pjavascripts.getResources()])
        
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite