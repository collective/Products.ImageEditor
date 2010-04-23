from Testing.ZopeTestCase import installPackage
from Products.Five import zcml, fiveconfigure
from collective.testcaselayer.ptc import BasePTCLayer, ptc_layer


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
        installPackage('collective.js.jquery', quiet=True)
        installPackage('collective.js.jqueryui', quiet=True)
        # quick-install...
        self.addProfile('Products.ImageEditor:default')


basic = Layer(bases=[ptc_layer])
