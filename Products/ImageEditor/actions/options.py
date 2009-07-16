from zope.component import Interface
from zope import schema
from Products.ImageEditor import imageeditor_message_factory as _

class INoOptions(Interface):
    """
    when there are no options available....
    """
    
class IBlurOptions(Interface):
    """
    """
    
    amount = schema.Int(
        title=_(u"label_blur_amount_title", default=u"Blur Amount"),
        description=_(u"label_blur_amount_description",
            default=u"Choose the level you want to blur the image"),
        min=0,
        max=8,
        default=2
    )
    
class ICompressOptions(Interface):
    
    amount = schema.Float(
        title=_(u"label_compress_amount_title", default=u"Compress Amount"),
        description=_(u"label_compress_amount_description", 
            default=u"How far to compress"),
        min=0.0,
        max=100.0,
        default=60.0
    )

class IContrastOptions(Interface):

    amount = schema.Float(
        title=_(u"label_contrast_amount_title", default=u"Amount"),
        description=_(u"label_contrast_amount_description", 
            default=u"Number between 0 and 100 to set the contrast to."),
        min=0.0,
        max=100.0,
        default=50.0
    )
    
class IBrightnessOptions(Interface):
    
    amount = schema.Float(
        title=_(u"label_brightness_amount_title", default=u"Amount"),
        description=_(u"label_brightness_amount_description",
            default=u"The Amount the brightness should be adjusted"),
        min=0.0,
        max=100.0,
        default=50.0
    )
    
    
class ISharpenOptions(Interface):
    
    amount = schema.Int(
        title=_(u"label_sharpen_amount_title", default=u"Amount"),
        description=_(u"label_sharpen_amount_description",
            default=u"The amount to sharpen the image"),
        min=1,
        max=10,
        default=2
    )
    
class IDropShadowOptions(Interface):
    
    offset_x = schema.Int(
        title=_(u"label_dropshadow_offset_x_title", default=u"Offset X"),
        description=_(u"label_dropshadow_offset_x_description",
            default=u"The offset the shadow should have on the x axis"),
        default=5
    )
    
    offset_y = schema.Int(
        title=_(u"label_dropshadow_offset_y_title", default=u"Offset Y"),
        description=_(u"label_dropshadow_offset_y_description",
            default=u"The offset the shadow should have on the y axis"),
        default=5
    )
    
    background_color = schema.TextLine(
        title=_(u"label_dropshadow_background_color_title", default=u"Background color"),
        description=_(u"label_dropshadow_background_color_description",
            default=u"The hex of the background color to use"),
        default=u"ffffff"
    )
    
    shadow_color = schema.TextLine(
        title=_(u"label_dropshadow_shadow_color_title", default=u"Shadow Color"),
        description=_(u"label_dropshadow_shadow_color_description",
            default=u"The hex of the color that will be used for the shadow."),
        default=u"444444"
    )
    
    border = schema.Int(
        title=_(u"label_dropshadow_border_title", default=u"Width"),
        description=_(u"label_dropshadow_border_description",
            default=u"How wide the shadow will be."),
        default=8
    )
    
    iterations = schema.Int(
        title=_(u"label_dropshadow_iterations_title", default=u"Softness"),
        description=_(u"label_dropshadow_iterations_description",
            default=u"Affects how heavy the shadow appears."),
        default=3
    )
    
class ISepiaOptions(Interface):
    
    red = schema.Int(
        title=_(u"label_sepia_red", default=u"Red"),
        description=_(u"label_description_sepia_red", 
            default=u"The level for red to apply for the sepia effect."),
        min=0,
        max=255,
        default=255
    )
    
    green = schema.Int(
        title=_(u"label_sepia_green", default=u"Green"),
        description=_(u"label_description_sepia_green", 
            default=u"The level for green to apply for the sepia effect."),
        min=0,
        max=255,
        default=240
    )
    
    blue = schema.Int(
        title=_(u"label_sepia_blue", default=u"Blue"),
        description=_(u"label_description_sepia_blue", 
            default=u"The level for blue to apply for the sepia effect."),
        min=0,
        max=255,
        default=192
    )
    
class ISaveAsOptions(Interface):
    
    type_to_save_as = schema.Choice(
        title=_(u"label_type_to_save_as", default=u"Type"),
        description=_(u"label_description_type_to_save_as",
            default=u"Content type to save image as."),
        default="Image",
        required=True,
        vocabulary="plone.app.vocabularies.ImageContentTypes"
    )
    
    title = schema.TextLine(
        title=_(u"label_title_save_as", default=u"Title"),
        description=_(u"label_description_title_save_as",
            default=u"Title of the content type that is also used to generate its id."),
        required=True
    )