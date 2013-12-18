# -*- coding: utf-8 -*-

from collective.testcaselayer.ptc import BasePTCLayer, ptc_layer
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from Products.Five import zcml, fiveconfigure
from Testing.ZopeTestCase import installPackage


class Layer(BasePTCLayer):
    """ basic layer for integration tests """

    def afterSetUp(self):
        # load zcml...
        fiveconfigure.debug_mode = True
        from Products import ImageEditor
        zcml.load_config('testing.zcml', package=ImageEditor)
        fiveconfigure.debug_mode = False
        # initialize packages...
        installPackage('Products.ImageEditor', quiet=True)
        installPackage('collective.js.jqueryui', quiet=True)
        # quick-install...
        self.addProfile('Products.ImageEditor:default')

basic = Layer(bases=[ptc_layer])


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import Products.ImageEditor
        self.loadZCML(package=Products.ImageEditor)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'Products.ImageEditor:default')

FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='Products.ImageEditor:Integration',
)

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE, z2.ZSERVER_FIXTURE),
    name='Products.ImageEditor:Functional',
)
