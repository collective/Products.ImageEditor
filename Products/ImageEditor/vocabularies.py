from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Products.ATContentTypes.interface.image import IImageContent
from Products.Archetypes.ArchetypeTool import _types as registered_types

class ImageContentTypeVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        type_values = registered_types.values()
        impl_image = lambda x : IImageContent.implementedBy(x['klass'])
        image_types = [v['klass'].portal_type for v in type_values if impl_image(v)]

        # remove duplicates when several types have the same content type
        # even if they are not installed at the same time
        _image_types = []
        [_image_types.append(i) for i in image_types if image_types.count(i) == 1]

        items = [SimpleTerm(i, i , i) for i in _image_types]
        return SimpleVocabulary(items)

ImageContentTypeVocabularyFactory = ImageContentTypeVocabulary()