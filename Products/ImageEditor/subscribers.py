from Products.ImageEditor.interfaces import IImageEditorAdapter


def handle_image_edit(object, event):
    for field in object.Schema().fields():
        if field.getType() != \
                'plone.app.blob.subtypes.image.ExtensionBlobField':
            continue
        imageeditor = IImageEditorAdapter(object)
        imageeditor.set_field(field.__name__)
        # XXX Check if base image is different
        if str(field.get(object)) != imageeditor.stack[0]:
            imageeditor.clear_edits()
