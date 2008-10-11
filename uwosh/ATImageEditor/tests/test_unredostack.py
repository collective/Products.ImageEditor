import unittest
from uwosh.ATImageEditor.tests.base import UWOshATImageEditorTestCase
from Products.CMFCore.utils import getToolByName
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from zope.component import getUtility

class TestUnredoStack(UWOshATImageEditorTestCase):
    """
    
    """
    

        
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestUnredoStack))
    return suite