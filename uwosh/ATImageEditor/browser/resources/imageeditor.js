var setKssAttr = function(element, key, value){
    element = $(element);
    var classes = element[0].className.split(' ');
    
    var startsplit = 'kssattr-'.length;
    var endsplit = startsplit + key.length;
    
    for(var i = 0; i < classes.length; i++){
        if(classes[i].substring(0, startsplit) == 'kssattr-'){
            if(classes[i].substring(startsplit, endsplit) == key){
                element.removeClass(classes[i]);
                classes[i] = 'kssattr-' + key + '-' + value;
                element.addClass(classes[i]);
                return;
            }
        }
    }
};

ImageEditor = function(){
    
    var imageEditor = this;

    //Manage elements
    imageEditor.manageButtons = $('div#manageButtons');

    imageEditor.saveButton = $('div#manageButtons input#save');
    imageEditor.cancelButton = $('div#manageButtons input#cancel');
    imageEditor.slider = $('div#manageButtons div#slider');
    imageEditor.sliderPercentage = $('div#manageButtons div#slider p');
    imageEditor.useZoomInput = $('div#manageButtons div.useZoom input#useZoom');
    
    //Action elements
    imageEditor.actionButtons = $('div#actionButtons');

    imageEditor.resize = {
        button: $('div#actionButtons div#cropAndResizeButtonContainer input#resize'),
        config: function(){
            return {
                handles: 'se,e,s',
                resize: function(e, ui){
                    imageEditor.calculateWidthAndHeight();
                }
            }
        }
    };
    imageEditor.crop = {
        button: $('div#actionButtons div#cropAndResizeButtonContainer input#crop'),
        config: function(){
            var w = imageEditor.image.width();
            var h = imageEditor.image.height();
            imageEditor.cropSelection = {
                x1: w/4,
                y1: h/4,
                x2: w-w/4,
                y2: h-h/4
            };
            
            return {
                onSelectChange: function(image, selection){
                    imageEditor.cropSelection = selection;
                    imageEditor.imagePixels.html(Math.round(selection.x2-selection.x1) + "x" + Math.round(selection.y2-selection.y1));
                },
                selectionColor: 'blue',
                enable: true,
                border: 2,
                show: true,
                x1: imageEditor.cropSelection.x1,
                y1: imageEditor.cropSelection.y1,
                x2: imageEditor.cropSelection.x2,
                y2: imageEditor.cropSelection.y2
            }
        }
    }
    imageEditor.applyButton = $('div#actionButtons div#cropAndResizeButtonContainer input#apply');

    imageEditor.rotateRightButton = $('div#actionButtons input#rotate-right');
    imageEditor.rotateLeftButton = $('div#actionButtons input#rotate-left');
    imageEditor.flipHorizontallyButton = $('div#actionButtons input#flipOnHorizontalAxis');
    imageEditor.flipVerticallyButton = $('div#actionButtons input#flipOnVerticalAxis');
    imageEditor.serverResizeSaveButton = $('input#serverResizeSaveButton');
    imageEditor.serverCropSaveButton = $('input#serverCropSaveButton');
    imageEditor.serverCropAndResize = $('div#actionButtons input#cropAndResize');
    imageEditor.undoButton = $('input#undo');
    imageEditor.redoButton = $('input#redo');
    
    imageEditor.actions = {
        list: ['sharpen', 'blur', 'compression', 'contrast', 'brightness'],
        blur: {
            perform: $('div#actionButtons div#blurdialog input#performBlur'),
            performClick: function(){ imageEditor.actions.blur.dialog.dialog('close'); },
            button: $('div#actionButtons input#blur'),
            buttonClick: function(){ imageEditor.actions.blur.dialog.dialog('open'); },
            dialog: $('div#blurdialog'),
            slider: {
                element: $('div#blurslider'),
                min:0,
                max:8,
                steps:8,
                startValue: 1,
                change: function(e, ui){
                    imageEditor.actions.blur.percentage.html(String(ui.value));
                    setKssAttr(imageEditor.actions.blur.perform[0], 'amount', String(ui.value));
                }
            },
            percentage: $('div#blurslider p')
        },
        compression: {
            perform: $('div#actionButtons div#compressiondialog input#performCompression'),
            performClick: function(){ imageEditor.actions.compression.dialog.dialog('close'); },
            button: $('div#actionButtons input#compression'),
            buttonClick: function(){ imageEditor.actions.compression.dialog.dialog('open'); },
            dialog: $('div#actionButtons div#compressiondialog'),
            slider: {
                element: $('div#compressionslider'),
                min:0,
                max:100,
                steps:100,
                startValue: 75,
                change: function(e, ui){
                    imageEditor.actions.compression.percentage.html(ui.value + "%");
                    setKssAttr(imageEditor.actions.compression.perform[0], 'amount', ui.value);
                }
            },
            percentage: $('div#compressionslider p')
        },
        contrast: {
            perform: $('div#actionButtons div#contrastdialog input#performContrast'),
            performClick: function(){ imageEditor.actions.contrast.dialog.dialog('close'); },
            button: $('div#actionButtons input#contrast'),
            buttonClick: function(){ imageEditor.actions.contrast.dialog.dialog('open'); },
            dialog: $('div#actionButtons div#contrastdialog'),
            slider: {
                element: $('div#contrastslider'),
                min:0,
                max:100,
                steps:100,
                startValue: 50,
                change: function(e, ui){
                    imageEditor.actions.contrast.percentage.html(ui.value + "%");
                    setKssAttr(imageEditor.actions.contrast.perform[0], 'amount', ui.value);
                }
            },
            percentage: $('div#contrastslider p')
        },
        brightness: {
            perform: $('div#actionButtons div#brightnessdialog input#performBrightness'),
            performClick: function(){ imageEditor.actions.brightness.dialog.dialog('close'); },
            button: $('div#actionButtons input#brightness'),
            buttonClick: function(){ imageEditor.actions.brightness.dialog.dialog('open'); },
            dialog: $('div#actionButtons div#brightnessdialog'),
            slider: {
                element: $('div#brightnessslider'),
                min:0,
                max:100,
                steps:100,
                startValue: 50,
                change: function(e, ui){
                    imageEditor.actions.brightness.percentage.html(ui.value + "%");
                    setKssAttr(imageEditor.actions.brightness.perform[0], 'amount', ui.value);
                }
            },
            percentage: $('div#brightnessslider p')
        },
        sharpen: {
            perform: $('div#actionButtons div#sharpendialog input#performSharpen'),
            performClick: function(){ imageEditor.actions.sharpen.dialog.dialog('close'); },
            button: $('div#actionButtons input#sharpen'),
            buttonClick: function(){ imageEditor.actions.sharpen.dialog.dialog('open'); },
            dialog: $('div#actionButtons div#sharpendialog'),
            slider: {
                element: $('div#sharpenslider'),
                min:0,
                max:80,
                steps:80,
                startValue: 10,
                change: function(e, ui){
                    var value = "0";
                    if(ui.value != 0){
                        value = String(ui.value/10);
                    }
                    imageEditor.actions.sharpen.percentage.html(value);
                    setKssAttr(imageEditor.actions.sharpen.perform[0], 'amount', value);
                }
            },
            percentage: $('div#sharpenslider p')
        }
    };

    imageEditor.imagePixels = $('span#imagePixels');

    imageEditor.image = $('div#imageEditor div#imageContainer img#sourceImage');
    imageEditor.imageContainer = $('div#imageEditor div#imageContainer');

    imageEditor.cropSelection = null;
    imageEditor.cropperBorderSize = 2;
    
    imageEditor.dialogSettings = {
        autoOpen: false,
        modal: true,
        resizable:false,
        overlay: {
            opacity: 0.7,
            background: 'black'
        },
        width: 225,
        height: 115
    };
    
    imageEditor.initialize = function(){
        imageEditor.setupResizeButton();
        imageEditor.setupCropButton();
        imageEditor.setupApplyButton();
        imageEditor.setupRotates();
        imageEditor.setupSlider();
        imageEditor.setupUserWarning();
        imageEditor.setupActions();
        imageEditor.actionButtons.draggable();
        imageEditor.calculateWidthAndHeight();
        
        if($('input.canCompress').attr('value') == "False"){
            imageEditor.actions.compression.button.addClass('disabled');
        }
        imageEditor.image.naturalWidth = parseInt($('input.imageWidth').attr('value'));
        imageEditor.image.naturalHeight = parseInt($('input.imageHeight').attr('value'));
    };
    
    imageEditor.calculateWidthAndHeight = function(){
        imageEditor.imagePixels.html(imageEditor.image.width() + "x" + imageEditor.image.height());
    };
    
    imageEditor.setupActions = function(){
        
        var actions = imageEditor.actions.list;
        
        for(var i = 0; i < actions.length; i++){            
            imageEditor.actions[actions[i]].dialog.show();//hidden at first...
            imageEditor.actions[actions[i]].slider.element.slider({
                min: imageEditor.actions[actions[i]].slider.min,
                max: imageEditor.actions[actions[i]].slider.max,
                steps: imageEditor.actions[actions[i]].slider.steps,
                startValue: imageEditor.actions[actions[i]].slider.startValue,
                change: imageEditor.actions[actions[i]].slider.change
            });
            imageEditor.actions[actions[i]].dialog.dialog(imageEditor.dialogSettings);
            imageEditor.actions[actions[i]].perform.click(imageEditor.actions[actions[i]].performClick);
            imageEditor.actions[actions[i]].button.click(imageEditor.actions[actions[i]].buttonClick);
        }
    }
    
    imageEditor.setDefaultSliderPositions = function(){
        var actions = imageEditor.actions.list;
        
        for(var i = 0; i < actions.length; i++){
            imageEditor.actions[actions[i]].slider.element.slider('moveTo', imageEditor.actions[actions[i]].slider.startValue);
        }
    };
    
    imageEditor.reset = function(){
        imageEditor.slider.slider('destroy');
        imageEditor.setupSlider();
        imageEditor.sliderPercentage.html("100%");
        //imageEditor.setDefaultSliderPositions();
    };
    
    imageEditor.getPct = function(value){
        if(value == 100){
            return 1;
        }else if(value > 9){
            return parseFloat('.' + value);
        }else{
            return parseFloat('.0' + value);
        }
    };
    
    imageEditor.resetImageSize = function(){
        var currentZoom = imageEditor.getCurrentImageZoomPct();
        var w = Math.round(imageEditor.image.naturalWidth*currentZoom);
        var h = Math.round(imageEditor.image.naturalHeight*currentZoom);

        imageEditor.image.width(w);
        imageEditor.image.height(h);
    }
    
    /*
     * @param pct: should be integer
    */
    imageEditor.setImagePercentSize = function(pct){
        var w = imageEditor.image.naturalWidth;
        var h = imageEditor.image.naturalHeight;
        
        var ic = imageEditor.isCropping();
        var ir = imageEditor.isResizing();
        var newPct = imageEditor.getPct(pct);
        
        w = Math.round(w*newPct);
        h = Math.round(h*newPct);
        
        //cannot resize or crop while changing image size
        if(ic){
            imageEditor.image.imgAreaSelect({ enable: false, hide: true });
        }else if(ir){
            w = imageEditor.image.width();
            h = imageEditor.image.height();
            var currentZoom = imageEditor.getCurrentImageZoomPct();
            w = Math.round((w/currentZoom)*newPct);
            h = Math.round((h/currentZoom)*newPct);
            
            imageEditor.image.resizable('destroy');
    	}
        
        imageEditor.image.width(w);
        imageEditor.image.height(h);
        
        if(ic){
            imageEditor.image.imgAreaSelect(imageEditor.crop.config());
        }else if(ir){
    		imageEditor.image.resizable(imageEditor.resize.config());
    	}
    };
    
    imageEditor.setImageZoomTitle = function(value){
        imageEditor.sliderPercentage.html(value + '%');
    };
    imageEditor.getCurrentImageZoomPct = function(){
        var html = imageEditor.sliderPercentage.html();
        var v = parseInt(html.substr(0, html.length-1));
        return imageEditor.getPct(v);
    }
    
    imageEditor.isCropping = function(){
        return imageEditor.crop.button.hasClass('editing');
    };
    
    imageEditor.isResizing = function(){
        return imageEditor.resize.button.hasClass('editing');
    }
    
    imageEditor.setupSlider = function(){        
        imageEditor.slider.slider({
            min:0,
            max:100,
            steps:100,
            startValue:100,
            change: function(e, ui){
                imageEditor.setImagePercentSize(ui.value);
                imageEditor.setImageZoomTitle(ui.value);
            }
        });
    };
    
    imageEditor.setupUserWarning = function(){
        if($.browser.mozilla || $.browser.safari){
            $(window).unload(function(){
                if(!imageEditor.saveButton.hasClass('disabled')){
                    return 'You have unsaved changes to this image that will be lost.';
                }
            });
        }
    };
    
    imageEditor.setupRotates = function(){
        $([imageEditor.rotateLeftButton, imageEditor.rotateRightButton, 
            imageEditor.flipHorizontallyButton, imageEditor.flipVerticallyButton]).each(function(){
            $(this).click(function(){
                imageEditor.removeResizableUnintrusive();
                imageEditor.removeCropperUnintrusive();
            });
        });
    };
    
    imageEditor.canApply = function(v){
        imageEditor.can(v, imageEditor.applyButton);
        if(v){
            imageEditor.applyButton.addClass('enabled');
        }else{
            imageEditor.applyButton.removeClass('enabled');
        }
    };
    
    imageEditor.can = function(v, button){
        if(v){
            button.removeClass('disabled');
            button[0].disabled = false;
        }else{
            button.addClass('disabled');
            button[0].disabled = true;
        }
    };
    
    imageEditor.canUndo = function(v){
        imageEditor.can(v, imageEditor.undoButton);
    };
    
    imageEditor.canRedo = function(v){
        imageEditor.can(v, imageEditor.redoButton);
    };
    
    imageEditor.canSave = function(v){
        imageEditor.can(v, imageEditor.saveButton);
        imageEditor.can(v, imageEditor.cancelButton);
    };
    
    imageEditor.addResizable = function(){
        imageEditor.image.resizable(imageEditor.resize.config());
		imageEditor.resize.button.attr('value', 'Cancel Resize');
		imageEditor.resize.button.addClass('editing');
		imageEditor.canApply(true);
    };
    
    imageEditor.removeResizableUnintrusive = function(){
        imageEditor.image.resizable('destroy');
		imageEditor.resize.button.attr('value', 'resize');
		imageEditor.image.attr('style', "");
		imageEditor.resize.button.removeClass('editing');
		imageEditor.canApply(false);
    };
    
    imageEditor.removeResizable = function(){
        imageEditor.removeResizableUnintrusive();
		imageEditor.calculateWidthAndHeight();
		imageEditor.resetImageSize();
    };
    
    imageEditor.setupResizeButton = function(){
        imageEditor.resize.button.click(function(){
            if(imageEditor.isCropping()){
                imageEditor.removeCropper();
                imageEditor.addResizable();
            }else if(imageEditor.isResizing()){
                imageEditor.removeResizable();
        	}else{
        		imageEditor.addResizable();
        	}
        });
    };
    
    imageEditor.setupCropButton = function(){
        imageEditor.crop.button.click(function(){
            if(imageEditor.isResizing()){
                imageEditor.removeResizable();
                imageEditor.addCropper();
            }else if(imageEditor.isCropping()){
                imageEditor.removeCropper();
        	}else{
                imageEditor.addCropper();
        	}
        });
    };
    
    imageEditor.addCropper = function(){
        imageEditor.image.imgAreaSelect(imageEditor.crop.config());
        imageEditor.imagePixels.html((imageEditor.cropSelection.x2-imageEditor.cropSelection.x1) + "x" + (imageEditor.cropSelection.y2-imageEditor.cropSelection.y1));
        imageEditor.crop.button.attr('value', 'Cancel Cropping');
        imageEditor.crop.button.addClass('editing');
        imageEditor.canApply(true);
    };
    
    imageEditor.removeCropperUnintrusive = function(){
        imageEditor.image.imgAreaSelect({ enable: false, hide: true });
        imageEditor.crop.button.attr('value', 'crop');
        imageEditor.crop.button.removeClass('editing');
        imageEditor.canApply(false);
    }
    
    imageEditor.removeCropper = function(){
        imageEditor.removeCropperUnintrusive()
        imageEditor.calculateWidthAndHeight();
    };
    
    imageEditor.useZoom = function(){
        return imageEditor.useZoomInput[0].checked;
    };
    
    imageEditor.getZoom = function(){
        var pc = imageEditor.sliderPercentage.html();
        return parseInt(pc.substr(0, pc.length-1));
    };
    
    imageEditor.getResize = function(){
        var zoom = imageEditor.getZoom();
        if(zoom == 100 || imageEditor.useZoom()){
            return {
                width: imageEditor.image.width(),
                height: imageEditor.image.height()
            }
        }else{
            return{
                width: imageEditor.image.width()/imageEditor.getPct(zoom),
                height: imageEditor.image.height()/imageEditor.getPct(zoom)
            }
        }
    };
    
    imageEditor.getCropSelection = function(){
        var zoom = imageEditor.getZoom();
        var zoomPct = imageEditor.getPct(zoom);
        if(zoom == 100  || imageEditor.useZoom()){
            return imageEditor.cropSelection;
        }else{
            var cs = imageEditor.cropSelection;
            cs.x1 = cs.x1/zoomPct;
            cs.x2 = cs.x2/zoomPct;
            cs.y1 = cs.y1/zoomPct;
            cs.y2 = cs.y2/zoomPct;
            return cs
        }
    };
    
    imageEditor.setupApplyButton = function(){
        imageEditor.applyButton.click(function(){
            if(imageEditor.isResizing()){
                var size = imageEditor.getResize();
                setKssAttr(imageEditor.serverResizeSaveButton[0], 'width', Math.round(size.width));
                setKssAttr(imageEditor.serverResizeSaveButton[0], 'height', Math.round(size.height));

                imageEditor.serverResizeSaveButton.trigger('click');
            }else if(imageEditor.isCropping()){
                var cs = imageEditor.getCropSelection();
                
                var action = null;
                if(imageEditor.useZoom()){//must resize and then crop
                    action = imageEditor.serverCropAndResize;
                    setKssAttr(action[0], 'width', Math.round(imageEditor.image.width()));
                    setKssAttr(action[0], 'height', Math.round(imageEditor.image.height()));
                }else{
                    action = imageEditor.serverCropSaveButton;
                }
                
                setKssAttr(action[0], 'tlx', Math.round(cs.x1));
                setKssAttr(action[0], 'tly', Math.round(cs.y1));
                setKssAttr(action[0], 'brx', Math.round(cs.x2));
                setKssAttr(action[0], 'bry', Math.round(cs.y2));

                action.trigger('click');
            }
        });
    };
    
    imageEditor.initialize();
    
};

$(document).ready(function(){
    document.imageEditor = new ImageEditor();
});