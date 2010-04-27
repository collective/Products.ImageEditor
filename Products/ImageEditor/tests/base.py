from StringIO import StringIO
from os.path import dirname, join
from PIL import Image
from Products.PloneTestCase import ptc
from Products.CMFCore.utils import getToolByName
from Products.ImageEditor import testing, tests
from Products.ImageEditor.adapters.imageeditor import ImageEditorAdapter


ptc.setupPloneSite()
ptc.utils.setupCoreSessions()


class ImageEditorTestCase(ptc.PloneTestCase):
    """ base class for integration tests """

    layer = testing.basic

    def afterSetUp(self):
        self.setRoles(('Manager',))
        # put SESSION object into REQUEST
        sdm = self.app.session_data_manager
        self.app.REQUEST.set('SESSION', sdm.getSessionData())

    def getImageContentType(self):
        try:
            images_folder = self.portal.invokeFactory(type_name="Folder", id="images_folder")
        except Exception:
            images_folder = "images_folder"

        try:

            id = self.portal['images_folder'].invokeFactory(type_name="Image", id="testimage")
        except Exception:
            id = 'testimage'
        image = self.portal[images_folder][id]
        image.setTitle('test')
        #(Pdb) p context.getField('image').get(context)
        #<Image at /plone/bug-mantis-01.png/image>
        #(Pdb) p context.getField('image').get(context).data
        #<OFS.Image.Pdata object at 0xb277db6c>
        #(Pdb) p context.getField('image').get(context).data.data
        #'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x04N\x00\x00...
        #...
        #
        #In testcase:
        #(Pdb) image.getField('image').get(image)
        #<Image at /plone/testimage/image>
        #(Pdb) image.getField('image').get(image).data
        #'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\...
        im = self.getOriginal()
        imageData = StringIO()
        im.save(imageData, im.format)
        image.setImage(imageData)
        return image

    def uninstall(self):
        setup_tool = getToolByName(self.portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-Products.ImageEditor:uninstall')

    def getEditor(self, context):
        return ImageEditorAdapter(context)

    def getImageEditorAdapter(self):
        image = self.getImageContentType()
        return ImageEditorAdapter(image)

    def getOriginal(self):
        return self.getImage('original.jpg')

    def getImagePath(self, name):
        return join(dirname(tests.__file__), 'testimages', name)

    def getImage(self, name):
        return Image.open(self.getImagePath(name))
