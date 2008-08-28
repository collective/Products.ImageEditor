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

    imageEditor.resizeButton = $('div#actionButtons div#cropAndResizeButtonContainer input#resize');
    imageEditor.cropButton = $('div#actionButtons div#cropAndResizeButtonContainer input#crop');
    imageEditor.applyButton = $('div#actionButtons div#cropAndResizeButtonContainer input#apply');

    imageEditor.rotateRightButton = $('div#actionButtons input#rotate-right');
    imageEditor.rotateLeftButton = $('div#actionButtons input#rotate-left');
    imageEditor.flipHorizontallyButton = $('div#actionButtons input#flipOnHorizontalAxis');
    imageEditor.flipVerticallyButton = $('div#actionButtons input#flipOnVerticalAxis');
    imageEditor.serverResizeSaveButton = $('input#serverResizeSaveButton');
    imageEditor.serverCropSaveButton = $('input#serverCropSaveButton');
    imageEditor.serverCropAndResize = $('div#actionButtons input#cropAndResize');
    imageEditor.undoButton = $('div#actionButtons input#undo');
    imageEditor.redoButton = $('div#actionButtons input#redo');
    
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
                    kukit.dom.setKssAttribute(imageEditor.actions.blur.perform[0], 'amount', String(ui.value));
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
                    kukit.dom.setKssAttribute(imageEditor.actions.compression.perform[0], 'amount', ui.value);
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
                    kukit.dom.setKssAttribute(imageEditor.actions.contrast.perform[0], 'amount', ui.value);
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
                    kukit.dom.setKssAttribute(imageEditor.actions.brightness.perform[0], 'amount', ui.value);
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
                    kukit.dom.setKssAttribute(imageEditor.actions.sharpen.perform[0], 'amount', value);
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
        imageEditor.setInitialSizes();
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
        
    };
    
    imageEditor.setInitialSizes = function(){
        imageEditor.imageWidth = imageEditor.image.width();
        imageEditor.imageHeight = imageEditor.image.height();
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
        imageEditor.setInitialSizes();
        imageEditor.slider.slider('destroy');
        imageEditor.setupSlider();
        imageEditor.sliderPercentage.html("100%");
        //imageEditor.setDefaultSliderPositions();
    };
    
    imageEditor.getPct = function(value){
        value = value + "";
        if(value.length == 3){
            return parseFloat(value[0] + '.' + value[1] + value[2]);
        }else if(value.length == 2){
            return parseFloat('.' + value);
        }else{
            return parseFloat('.0' + value);
        }
    };
    
    imageEditor.setupSlider = function(){        
        imageEditor.slider.slider({
            min:0,
            max:100,
            steps:100,
            startValue:100,
            change: function(e, ui){
                if(imageEditor.imageWidth == 0){
                    imageEditor.imageWidth = imageEditor.image.width();
                    imageEditor.imageHeight = imageEditor.image.height();
                }
                var width = imageEditor.imageWidth;
                var height = imageEditor.imageHeight;
                imageEditor.resizedImageWidth = Math.round(width*imageEditor.getPct(ui.value));
                imageEditor.resizedImageHeight = Math.round(height*imageEditor.getPct(ui.value));
                if(ui.value != 100){
                    imageEditor.image.width(imageEditor.resizedImageWidth);
                    imageEditor.image.height(imageEditor.resizedImageHeight);
                }else{
                    imageEditor.image.width(width);
                    imageEditor.image.height(height);
                }
                imageEditor.sliderPercentage.html(ui.value + '%');
                
                if(imageEditor.cropButton.attr('value').substring(0, 6) == "Cancel"){
                    imageEditor.removeCropper();
                    imageEditor.addCropper();
                }else if(imageEditor.resizeButton.attr('value').substring(0, 6) == "Cancel"){
                    imageEditor.removeResizable();
            		imageEditor.addResizable();
            	}
            }
        });
    };
    
    imageEditor.setupUserWarning = function(){
        window.onbeforeunload = function(){
            if(!imageEditor.saveButton.hasClass('disabled')){
                return 'You have unsaved changes to this image that will be lost.';
            }
        }
    };
    
    imageEditor.setupRotates = function(){
        $([imageEditor.rotateLeftButton, imageEditor.rotateRightButton, 
            imageEditor.flipHorizontallyButton, imageEditor.flipVerticallyButton]).each(function(){
            $(this).click(function(){
                imageEditor.removeCropper();
                imageEditor.removeResizable();
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
        imageEditor.image.resizable({
            handles: 'se,e,s',
            resize: function(e, ui){
                imageEditor.calculateWidthAndHeight();
            }
        });
		imageEditor.resizeButton.attr('value', 'Cancel Resize');
		imageEditor.resizeButton.addClass('editing');
		imageEditor.canApply(true);
    };
    
    imageEditor.removeResizable = function(){
        imageEditor.image.resizable('destroy');
		imageEditor.resizeButton.attr('value', 'resize');
		imageEditor.image.attr('style', "");
		imageEditor.resizeButton.removeClass('editing');
		imageEditor.canApply(false);
		imageEditor.calculateWidthAndHeight();
		
		if(imageEditor.getZoom() != 100){
		    imageEditor.image.width(imageEditor.resizedImageWidth);
    		imageEditor.image.height(imageEditor.resizedImageHeight);
		}else{
		    imageEditor.image.css('width', '');
    		imageEditor.image.css('height', '');
		}
    };
    
    imageEditor.setupResizeButton = function(){
        imageEditor.resizeButton.click(function(){
            if(imageEditor.cropButton.attr('value').substring(0, 6) == "Cancel"){
                imageEditor.removeCropper();
                imageEditor.addResizable();
            }else if($(this).attr('value').substring(0, 6) == "Cancel"){
                imageEditor.removeResizable();
        	}else{
        		imageEditor.addResizable();
        	}
        });
    };
    
    imageEditor.addCropper = function(){
        var w = imageEditor.image.width();
        var h = imageEditor.image.height();
        imageEditor.cropSelection = {
            x1: w/4,
            y1: h/4,
            x2: w-w/4,
            y2: h-h/4
        };
        imageEditor.image.imgAreaSelect({
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
        });
        imageEditor.imagePixels.html((imageEditor.cropSelection.x2-imageEditor.cropSelection.x1) + "x" + (imageEditor.cropSelection.y2-imageEditor.cropSelection.y1));
        imageEditor.cropButton.attr('value', 'Cancel Cropping');
        imageEditor.cropButton.addClass('editing');
        imageEditor.canApply(true);
    };
    
    imageEditor.removeCropper = function(){
        imageEditor.image.imgAreaSelect({ 
            enable: false,
            hide: true
        });
        imageEditor.cropButton.attr('value', 'crop');
        imageEditor.cropButton.removeClass('editing');
        imageEditor.canApply(false);
        imageEditor.calculateWidthAndHeight();
    };
    
    imageEditor.setupCropButton = function(){
        imageEditor.cropButton.click(function(){
            if(imageEditor.resizeButton.attr('value').substring(0, 6) == "Cancel"){
                imageEditor.removeResizable();
                imageEditor.addCropper();
            }else if($(this).attr('value').substring(0, 6) == "Cancel"){
                imageEditor.removeCropper();
        	}else{
                imageEditor.addCropper();
        	}
        });
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
            if(imageEditor.resizeButton.attr('value').substring(0, 6) == "Cancel"){
                var size = imageEditor.getResize();
                kukit.dom.setKssAttribute(imageEditor.serverResizeSaveButton[0], 'width', size.width);
                kukit.dom.setKssAttribute(imageEditor.serverResizeSaveButton[0], 'height', size.height);

                imageEditor.serverResizeSaveButton.trigger('click');
            }else if(imageEditor.cropButton.attr('value').substring(0, 6) == "Cancel"){
                var cs = imageEditor.getCropSelection();
                
                var action = null;
                if(imageEditor.useZoom()){//must resize and then crop
                    action = imageEditor.serverCropAndResize;
                    kukit.dom.setKssAttribute(action[0], 'width', imageEditor.image.width());
                    kukit.dom.setKssAttribute(action[0], 'height', imageEditor.image.height());
                }else{
                    action = imageEditor.serverCropSaveButton;
                }
                
                kukit.dom.setKssAttribute(action[0], 'tlx', cs.x1);
                kukit.dom.setKssAttribute(action[0], 'tly', cs.y1);
                kukit.dom.setKssAttribute(action[0], 'brx', cs.x2);
                kukit.dom.setKssAttribute(action[0], 'bry', cs.y2);

                action.trigger('click');
            }
        });
    };
    
    imageEditor.initialize();
    
};

$(document).ready(function(){
    document.imageEditor = new ImageEditor();
});