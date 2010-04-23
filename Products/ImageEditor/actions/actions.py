from base import BaseImageEditorAction
from zope.interface import implements
from Products.ImageEditor.interfaces.actions import IImageEditorAction
from options import INoOptions, IBlurOptions, ICompressOptions, IContrastOptions, \
    IBrightnessOptions, ISharpenOptions, IDropShadowOptions, ISepiaOptions, ISaveAsOptions
from zope.formlib import form
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
from widgets import SliderWidget
from Products.CMFCore.utils import getToolByName
from zope.component import queryUtility
from plone.i18n.normalizer.interfaces import IURLNormalizer

class CropAction(BaseImageEditorAction):
    implements(IImageEditorAction)

    options = form.FormFields(INoOptions)
    name = u"Crop"
    description = u"Crop the image."
    icon = u"++resource++imageeditor/icons/stock-selection-intersect-16.png"
    
    def on_setup(self):
        return """
function add_crop(){
    var w = $('#source-image').width(), h = $('#source-image').height();
    start_selection = {
        x1: w/4,
        y1: h/4,
        x2: w-w/4,
        y2: h-h/4
    };
    window.crop_selection = start_selection;
    
    function create_cropper(ratio){
        var options = {
            onSelectChange: function(image, selection){
                window.crop_selection = selection;
            },
            selectionColor: 'blue',
            enable: true,
            border: 2,
            handles: true,
            show: true,
            parent: '#image-container',
            x1 : start_selection.x1,
            y1 : start_selection.y1,
            x2 : start_selection.x2,
            y2 : start_selection.y2
        }
        if(ratio != null){
            options.aspectRatio = ratio;
        }
        $('#source-image').imgAreaSelect(options);
    }
    create_cropper(null);
    
    $("#aspect-ratio-selector").dialog({
        position : 'right',
        title : "Aspect Ratio",
        autoOpen:true,
        resizable:false,
        modal: false,
        draggable: true,
        width:200,
        buttons : {
            "Manual" : function(){
                $('#source-image').imgAreaSelect({ enable: false, hide: true });
                create_cropper(null);
            },
            "3:2" : function(){
                $('#source-image').imgAreaSelect({ enable: false, hide: true });
                create_cropper("3:2");
            },
            "4:3" : function(){
                $('#source-image').imgAreaSelect({ enable: false, hide: true });
                create_cropper("4:3");
            },
            "16:9" : function(){
                $('#source-image').imgAreaSelect({ enable: false, hide: true });
                create_cropper("16:9");
            },
            "5:4" : function(){
                $('#source-image').imgAreaSelect({ enable: false, hide: true });
                create_cropper("5:4");
            },
            "1:1" : function(){
                $('#source-image').imgAreaSelect({ enable: false, hide: true });
                create_cropper("1:1");
            }
        }
    });
    
}

function remove_crop(){
    $('#source-image').imgAreaSelect({ enable: false, hide: true });
    $("#aspect-ratio-selector").dialog('destroy');
}
        
on('action_button_clicked').accomplish(function(btn){

if($(btn).attr('id') == "crop-button"){
    add_crop();
}else{
    remove_crop();
}

});

on('before_image_reload').accomplish(function(){
    remove_crop();
});

on('before_image_zoom_change').accomplish(function(params){
    var active_btn = $('input.edit-button.active');
    if(active_btn.attr('id') == 'crop-button'){
        remove_crop();
    }
});
on('after_image_zoom_change').accomplish(function(params){
    var active_btn = $('input.edit-button.active');
    if(active_btn.attr('id') == 'crop-button'){
        add_crop();
    }
});
        """
    
    def action_parameters(self):
        return """(function(){
    var cs = {};
    var zoom = parseFloat(jQuery("#zoom-slider-value").attr('value'));
    cs['crop.x1'] = window.crop_selection.x1/zoom;
    cs['crop.x2'] = window.crop_selection.x2/zoom;
    cs['crop.y1'] = window.crop_selection.y1/zoom;
    cs['crop.y2'] = window.crop_selection.y2/zoom;
    return cs;
})"""
    
    def __call__(self, x1, y1, x2, y2):
        image = self.editor.get_current_image()
        box = (int(float(x1)), int(float(y1)), int(float(x2)), int(float(y2)))
        new_image = image.crop(box=box)
        new_image.load()
        
        self.editor.set_image(new_image, image.format)
        
        
class RotateLeftAction(BaseImageEditorAction):
    
    implements(IImageEditorAction)
    
    options = form.FormFields(INoOptions)
    
    name = u"Rotate Left"
    description = u"Rotate the image to the left."
    skip_apply = True
    icon = u"++resource++imageeditor/icons/stock-rotate-270-16.png"
    def __call__(self):
        original = self.editor.get_current_image()
        image = original.rotate(90)

        self.editor.set_image(image, original.format)
        
class BlurAction(BaseImageEditorAction):
    implements(IImageEditorAction)
    
    options = form.FormFields(IBlurOptions)
    options['amount'].custom_widget = SliderWidget
    name = u"Blur"
    description = u"Blur this image."
    icon = u"++resource++imageeditor/icons/stock-tool-blur-16.png"
    
    def __call__(self, amount):
        image = self.editor.get_current_image()
        fmt = image.format
        for x in range(0, int(amount)):
            image = image.filter(ImageFilter.BLUR)
            
        self.editor.set_image(image, fmt)
    
class SaveImageEditAction(BaseImageEditorAction):
    implements(IImageEditorAction)
    
    options = form.FormFields(INoOptions)
    
    name = "Save"
    description = "Save the edited image."
    skip_apply = True
    icon = u"++resource++imageeditor/icons/apply.png"
    
    def on_setup(self):
        return """
function save_reload(data){
    var btn = $('#save-button');

    if(data.can_save){
        btn[0].disabled = false;
        btn.removeClass('disabled');
    }else{
        btn[0].disabled = true;
        btn.addClass('disabled');
    }
}
on('after_image_reload').accomplish(save_reload);
save_reload(IMAGE_INFORMATION);
        """
    
    def __call__(self):
        portal_repository = getToolByName(self.editor.context, 'portal_repository')
        if portal_repository.isVersionable(self.editor.context):
            portal_repository.save(self.editor.context, comment = "saved from image editor")

        self.editor.save_edit()
        
        self.editor.context.reindexObject() #stop image caching on browser
    
class SaveAsImageEditAction(BaseImageEditorAction):
    implements(IImageEditorAction)

    options = form.FormFields(ISaveAsOptions)
    
    name = "Save As"
    description = "Save the edited image as another content item."
    icon = None

    def on_setup(self):
        return """
function redirect(data){
    if(data.previous_action == 'save-as'){
        window.location = data.new_type_location;
    }
}
on('after_image_reload').accomplish(redirect);
"""

    def __call__(self, type_to_save_as, title, *args, **kwargs):
        """
        create the new type, pass along the url to the client and then
        the javascript will redirect the browser
        """
        if not title:
            title = self.editor.context.Title()
            
        parent = self.editor.context.getParentNode()
        
        new_id = orig_id = queryUtility(IURLNormalizer).normalize(title)
        
        count = 1
        while new_id in parent.objectIds():
            new_id = orig_id + "-" + str(count)
            count += count
        
        parent.invokeFactory(
            type_to_save_as,
            new_id,
            title = title,
            image = self.editor.get_current_image_data()
        )
        
        return {'new_type_location' : parent.absolute_url() + "/" + new_id + "/edit"}
        
class CancelImageEditAction(BaseImageEditorAction):
    implements(IImageEditorAction)

    options = form.FormFields(INoOptions)

    name = "Cancel"
    description = "Cancel the current edit."
    skip_apply = True
    icon = u"++resource++imageeditor/icons/process-stop.png"
    
    def on_setup(self):
        return """
        
function cancel_reload(data){
    var btn = $('#cancel-button');

    if(data.can_save){
        btn[0].disabled = false;
        btn.removeClass('disabled');
    }else{
        btn[0].disabled = true;
        btn.addClass('disabled');
    }
}
on('after_image_reload').accomplish(cancel_reload);
cancel_reload(IMAGE_INFORMATION);
        """
    
    def __call__(self):
        self.editor.clear_edits()

class RedoAction(BaseImageEditorAction):
    implements(IImageEditorAction)

    options = form.FormFields(INoOptions)
    name = u"Redo"
    description = u"Redo the previous undo action."
    skip_apply = True
    icon = u"++resource++imageeditor/icons/edit-redo.png"
    
    def on_setup(self):
        return """
        
function redo_reload(data){
    var btn = $('#redo-button');

    if(data.can_redo){
        btn[0].disabled = false;
        btn.removeClass('disabled');
    }else{
        btn[0].disabled = true;
        btn.addClass('disabled');
    }
}
        
on('after_image_reload').accomplish(redo_reload);
redo_reload(IMAGE_INFORMATION)
        """
    
    def __call__(self):
        self.editor.redo()
        
class UndoAction(BaseImageEditorAction):
    implements(IImageEditorAction)

    options = form.FormFields(INoOptions)
    name = u"Undo"
    description = u"Go back to the previous change."
    skip_apply = True
    icon = u"++resource++imageeditor/icons/edit-undo.png"

    def on_setup(self):
        return """
function undo_reload(data){
    var btn = $('#undo-button');

    if(data.can_undo){
        btn[0].disabled = false;
        btn.removeClass('disabled');
    }else{
        btn[0].disabled = true;
        btn.addClass('disabled');
    }
}
        
on('after_image_reload').accomplish(undo_reload);
undo_reload(IMAGE_INFORMATION);
        """

    def __call__(self):
        self.editor.undo()
        
class RotateRightAction(BaseImageEditorAction):
    implements(IImageEditorAction)

    options = form.FormFields(INoOptions)
    name = u"Rotate Right"
    description = u"Rotate the image right."
    skip_apply = True
    icon = u"++resource++imageeditor/icons/stock-rotate-90-16.png"
    
    def __call__(self):
        original = self.editor.get_current_image()
        image = original.rotate(270)

        self.editor.set_image(image, original.format)

class FlipOnVerticalAxisAction(BaseImageEditorAction):
    implements(IImageEditorAction)

    options = form.FormFields(INoOptions)
    name = u"Flip Vertical"
    description = u"Flip the image on vertically."
    skip_apply = True
    icon = u"++resource++imageeditor/icons/stock-tool-rotate-16.png"
    
    def __call__(self):
        original = self.editor.get_current_image()
        image = original.transpose(Image.FLIP_TOP_BOTTOM)

        self.editor.set_image(image, original.format)

class CompressAction(BaseImageEditorAction):
    implements(IImageEditorAction)

    options = form.FormFields(ICompressOptions)
    options['amount'].custom_widget = SliderWidget
    name = u"Compress"
    description = u"Compress this image to make it lower quality."
    icon = u"++resource++imageeditor/icons/stock-template-16.png"

    def __call__(self, amount):
        image = self.editor.get_current_image().convert('RGB') # if it is a png, convert it...
        self.editor.set_image(image, quality=float(amount))

class ContrastAction(BaseImageEditorAction):
    implements(IImageEditorAction)
    
    options = form.FormFields(IContrastOptions)
    options['amount'].custom_widget = SliderWidget
    name = u"Contrast"
    description = u"Change the contrast of the image."
    icon = u"++resource++imageeditor/icons/stock-tool-contrast-16.png"
    
    def __call__(self, amount):
        image = self.editor.get_current_image()
        enhancer = ImageEnhance.Contrast(image)
        newImage = enhancer.enhance((float(amount)/100)*2.0)

        self.editor.set_image(newImage, image.format)
    
class BrightnessAction(BaseImageEditorAction):
    implements(IImageEditorAction)
    
    options = form.FormFields(IBrightnessOptions)
    options['amount'].custom_widget = SliderWidget
    name = u"Brightness"
    description = u"Change the brightness of the image."
    icon = u"++resource++imageeditor/icons/stock-tool-brightness-16.png"
    
    def __call__(self, amount):
        image = self.editor.get_current_image()
        enhancer = ImageEnhance.Brightness(image)
        #can enhance from 0.0-2.0, 1.0 being original image
        newImage = enhancer.enhance((float(amount)/100)*2.0)

        self.editor.set_image(newImage, image.format)
        
        
class SharpenAction(BaseImageEditorAction):
    implements(IImageEditorAction)
    
    options = form.FormFields(ISharpenOptions)
    options['amount'].custom_widget = SliderWidget
    name = u"Sharpen"
    description = u"Sharpen the image."
    icon = u"++resource++imageeditor/icons/stock-tool-colorize-16.png"
    
    def __call__(self, amount):
        image = self.editor.get_current_image()
        enhancer = ImageEnhance.Sharpness(image)
        newImage = enhancer.enhance(int(amount))

        self.editor.set_image(newImage, image.format)

class FlipOnHorizontalAxisAction(BaseImageEditorAction):
    implements(IImageEditorAction)
    
    options = form.FormFields(INoOptions)
    name = u"Flip Horizontally"
    description = u"Flip the image on the horizontal axis."
    skip_apply = True
    icon = u"++resource++imageeditor/icons/stock-tool-flip-16.png"
    
    def __call__(self):
        original = self.editor.get_current_image()
        image = original.transpose(Image.FLIP_LEFT_RIGHT)

        self.editor.set_image(image, original.format)

class ResizeAction(BaseImageEditorAction):
    implements(IImageEditorAction)
    
    options = form.FormFields(INoOptions)
    name = u"Resize"
    description = u"Resize the image.."
    icon = u"++resource++imageeditor/icons/stock-resize-16.png"
    
    def on_setup(self):
        return """
function add_resize(){
    $('#image-container')[0].scrollTop = 5000;
    $('#image-container')[0].scrollLeft = 5000;
    
    function create_resizable(){
        $('#source-image').resizable({
            handles: 'all',
            resize: function(e, ui){
                //nothing
            }
        });
    }
    create_resizable();
    
    $('#resize-to-fields').dialog({
        autoOpen:true,
        resizable:false,
        modal: false,
        draggable: true,
        title: "Manual Resize",
        zindex: 1002,
        position: 'right',
        buttons: {
            Resize: function() {
                $('#source-image').resizable('destroy');
                var width = $('#resize-width').val();
                var height = $('#resize-height').val();
                if(isNaN(width) || isNaN(height)){
                    alert("You must enter a number for the width and height.");
                }else{
                    var zoom = parseFloat(jQuery("#zoom-slider-value").attr('value'));
                
                    $('#source-image').width(Math.floor(parseInt(width)*zoom) + "px");
                    $('#source-image').height(Math.floor(parseInt(height)*zoom) + "px");
                }
                
                create_resizable();
            },
            Close: function() {
                $(this).dialog('close');
            }
        }
        
    });
}
function remove_resize(){
    $('#source-image').resizable('destroy');
    $('#resize-to-fields').dialog('destroy');
}
on('action_button_clicked').accomplish(function(btn){

if($(btn).attr('id') == "resize-button"){
    add_resize();
}else{
    remove_resize();
}

});

on('before_image_reload').accomplish(function(){
    remove_resize();
});

on('before_image_zoom_change').accomplish(function(params){
    var active_btn = $('input.edit-button.active');
    if(active_btn.attr('id') == 'resize-button'){
        remove_resize();
    }
});
on('after_image_zoom_change').accomplish(function(params){
    var active_btn = $('input.edit-button.active');
    if(active_btn.attr('id') == 'resize-button'){
        add_resize();
    }
});
            """

    def action_parameters(self):
        return """(function(){
    var res = {};
    var zoom = parseFloat(jQuery("#zoom-slider-value").attr('value'));
    
    res['resize.width'] = jQuery('#source-image').width()/zoom;
    res['resize.height'] = jQuery('#source-image').height()/zoom;
    return res;
})"""
    
    def __call__(self, width, height):
        image = self.editor.get_current_image()
        size=(int(float(width)), int(float(height)))
        new_image = image.resize(size, Image.ANTIALIAS)
        
        self.editor.set_image(new_image, image.format)

class DropShadowAction(BaseImageEditorAction):
    implements(IImageEditorAction)
    
    options = form.FormFields(IDropShadowOptions)
    name = u"Drop Shadow"
    description = u"Adds a drop shadow to the image."
    icon = u"++resource++imageeditor/icons/stock-transparency-16.png"
    
    def __call__(self, offset_x, offset_y, background_color, shadow_color, border, iterations):
        image = self.editor.get_current_image().convert('RGB') #convert to png if it isn't--shadow won't work without this.
        offset = (int(offset_x), int(offset_y))
        background=eval("0x" + background_color[:6]) #precaution in case code is attempted to be injected
        shadow=eval("0x" + shadow_color[:6]) #precaution in case code is attempted to be injected
        border=int(border)
        iterations=int(iterations)
        
        # Create the backdrop image -- a box in the background colour with a 
        # shadow on it.
        totalWidth = image.size[0] + abs(offset[0]) + 2*border
        totalHeight = image.size[1] + abs(offset[1]) + 2*border
        back = Image.new(image.mode, (totalWidth, totalHeight), background)

        # Place the shadow, taking into account the offset from the image
        shadowLeft = border + max(offset[0], 0)
        shadowTop = border + max(offset[1], 0)
        back.paste(
            shadow, 
            [shadowLeft, shadowTop, shadowLeft + image.size[0], shadowTop + image.size[1]] 
        )

        # Apply the filter to blur the edges of the shadow.  Since a small kernel
        # is used, the filter must be applied repeatedly to get a decent blur.
        for n in range(0, iterations):
            back = back.filter(ImageFilter.BLUR)

        # Paste the input image onto the shadow backdrop  
        imageLeft = border - min(offset[0], 0)
        imageTop = border - min(offset[1], 0)
        back.paste(image, (imageLeft, imageTop))
        
        self.editor.set_image(back)

class SepiaAction(BaseImageEditorAction):
    implements(IImageEditorAction)
    
    options = form.FormFields(ISepiaOptions)
    options['red'].custom_widget = SliderWidget
    options['green'].custom_widget = SliderWidget
    options['blue'].custom_widget = SliderWidget
    
    name = u"Sepia"
    description = u"Applies the sepia effect to the image."
    icon = None
    
    def make_linear_ramp(self, white):
        # putpalette expects [r,g,b,r,g,b,...]
        ramp = []
        r, g, b = white
        for i in range(255):
            ramp.extend((r*i/255, g*i/255, b*i/255))
        return ramp        
    
    def __call__(self, red, green, blue):
        """
        found at http://effbot.org/zone/pil-sepia.htm
        """
        sepia = self.make_linear_ramp((int(red), int(green), int(blue)))
        image = self.editor.get_current_image()

        # convert to grayscale
        if image.mode != "L":
            image = image.convert("L")

        # optional: apply contrast enhancement here, e.g.
        image = ImageOps.autocontrast(image)

        # apply sepia palette
        image.putpalette(sepia)

        # convert back to RGB so we can save it as JPEG
        # (alternatively, save it in PNG or similar)
        image = image.convert("RGB")
        
        self.editor.set_image(image)