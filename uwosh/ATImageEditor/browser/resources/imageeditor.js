ImageEditor = function(){
    
    imageEditor = this;

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
    
    imageEditor.blur = {
        perform: $('div#actionButtons div#blurdialog input#performBlur'),
        button: $('div#actionButtons input#blur'),
        dialog: $('div#blurdialog'),
        slider: $('div#blurslider'),
        percentage: $('div#blurslider p')
    }
    imageEditor.compression = {
        perform: $('div#actionButtons div#compressiondialog input#performCompression'),
        button: $('div#actionButtons input#compression'),
        dialog: $('div#actionButtons div#compressiondialog'),
        slider: $('div#compressionslider'),
        percentage: $('div#compressionslider p')
    }
    imageEditor.contrast = {
        perform: $('div#actionButtons div#contrastdialog input#performContrast'),
        button: $('div#actionButtons input#contrast'),
        dialog: $('div#actionButtons div#contrastdialog'),
        slider: $('div#contrastslider'),
        percentage: $('div#contrastslider p')
    }
    imageEditor.brightness = {
        perform: $('div#actionButtons div#brightnessdialog input#performBrightness'),
        button: $('div#actionButtons input#brightness'),
        dialog: $('div#actionButtons div#brightnessdialog'),
        slider: $('div#brightnessslider'),
        percentage: $('div#brightnessslider p')
    }
    imageEditor.sharpen = {
        perform: $('div#actionButtons div#sharpendialog input#performSharpen'),
        button: $('div#actionButtons input#sharpen'),
        dialog: $('div#actionButtons div#sharpendialog'),
        slider: $('div#sharpenslider'),
        percentage: $('div#sharpenslider p')
    }

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
        imageEditor.setupBlur();
        imageEditor.setupCompression();
        imageEditor.setupContrast();
        imageEditor.setupBrightness();
        imageEditor.setupSharpen();
        imageEditor.actionButtons.draggable();
        imageEditor.calculateWidthAndHeight();
    };
    
    imageEditor.calculateWidthAndHeight = function(){
        imageEditor.imagePixels.html(imageEditor.image.width() + "x" + imageEditor.image.height());
    }
    
    imageEditor.setupBlur = function(){
        imageEditor.blur.slider.slider({
            minValue:0,
            maxValue:8,
            steps:8,
            startValue:4,
            change: function(e, ui){
                imageEditor.blur.percentage.html(Math.round(ui.value/12.5));
                kukit.dom.setKssAttribute(imageEditor.blur.perform[0], 'amount', String(Math.round(ui.value/12.5)));
            }
        });
        imageEditor.blur.dialog.show();//hidden at first...
        imageEditor.blur.perform.click(function(){
            imageEditor.blur.dialog.dialog('close');
        });
        
        imageEditor.blur.dialog.dialog(imageEditor.dialogSettings);
        imageEditor.blur.button.click(function(){
            imageEditor.blur.dialog.dialog('open');
        });
    }
    
    imageEditor.setupCompression = function(){
        imageEditor.compression.slider.slider({
            minValue:0,
            maxValue:100,
            steps:100,
            startValue:100,
            change: function(e, ui){
                imageEditor.compression.percentage.html(ui.value + "%");
                kukit.dom.setKssAttribute(imageEditor.compression.perform[0], 'amount', ui.value);
            }
        });
        imageEditor.compression.dialog.show();//hidden at first...
        imageEditor.compression.perform.click(function(){
            imageEditor.compression.dialog.dialog('close');
        });
        
        imageEditor.compression.dialog.dialog(imageEditor.dialogSettings);
        imageEditor.compression.button.click(function(){
            imageEditor.compression.dialog.dialog('open');
        });
    }
    imageEditor.setupContrast = function(){
        imageEditor.contrast.slider.slider({
            minValue:0,
            maxValue:100,
            steps:100,
            startValue:100,
            change: function(e, ui){
                imageEditor.contrast.percentage.html(ui.value + "%");
                kukit.dom.setKssAttribute(imageEditor.contrast.perform[0], 'amount', ui.value);
            }
        });
        imageEditor.contrast.dialog.show();//hidden at first...
        imageEditor.contrast.perform.click(function(){
            imageEditor.contrast.dialog.dialog('close');
        });
        
        imageEditor.contrast.dialog.dialog(imageEditor.dialogSettings);
        imageEditor.contrast.button.click(function(){
            imageEditor.contrast.dialog.dialog('open');
        });
    }
    imageEditor.setupBrightness = function(){
        imageEditor.brightness.slider.slider({
            minValue:0,
            maxValue:100,
            steps:100,
            startValue:100,
            change: function(e, ui){
                imageEditor.brightness.percentage.html(ui.value + "%");
                kukit.dom.setKssAttribute(imageEditor.brightness.perform[0], 'amount', ui.value);
            }
        });
        imageEditor.brightness.dialog.show();//hidden at first...
        imageEditor.brightness.perform.click(function(){
            imageEditor.brightness.dialog.dialog('close');
        });
        
        imageEditor.brightness.dialog.dialog(imageEditor.dialogSettings);
        imageEditor.brightness.button.click(function(){
            imageEditor.brightness.dialog.dialog('open');
        });
    }
    imageEditor.setupSharpen = function(){
        imageEditor.sharpen.slider.slider({
            minValue:0,
            maxValue:2,
            steps:100,
            startValue:0,
            change: function(e, ui){
                imageEditor.sharpen.percentage.html(ui.value/50);
                kukit.dom.setKssAttribute(imageEditor.sharpen.perform[0], 'amount', ui.value/50);
            }
        });
        imageEditor.sharpen.dialog.show();//hidden at first...
        imageEditor.sharpen.perform.click(function(){
            imageEditor.sharpen.dialog.dialog('close');
        });
        
        imageEditor.sharpen.dialog.dialog(imageEditor.dialogSettings);
        imageEditor.sharpen.button.click(function(){
            imageEditor.sharpen.dialog.dialog('open');
        });
    }
    
    imageEditor.reset = function(){
        imageEditor.setInitialSizes();
        imageEditor.slider.slider('destroy');
        imageEditor.setupSlider();
        imageEditor.sliderPercentage.html("100%");
    }
    
    imageEditor.setInitialSizes = function(){
        imageEditor.imageWidth = imageEditor.image.width();
        imageEditor.imageHeight = imageEditor.image.height();
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
            minValue:0,
            maxValue:100,
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
    }
    
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
    }
    imageEditor.can = function(v, button){
        if(v){
            button.removeClass('disabled');
            button[0].disabled = false;
        }else{
            button.addClass('disabled');
            button[0].disabled = true;
        }
    }
    imageEditor.canUndo = function(v){
        imageEditor.can(v, imageEditor.undoButton);
    }
    imageEditor.canRedo = function(v){
        imageEditor.can(v, imageEditor.redoButton);
    }
    imageEditor.canSave = function(v){
        imageEditor.can(v, imageEditor.saveButton);
        imageEditor.can(v, imageEditor.cancelButton);
    }
    
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
                imageEditor.imagePixels.html((selection.x2-selection.x1) + "x" + (selection.y2-selection.y1));
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
    }
    
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
    }
    
    imageEditor.getResize = function(){
        var zoom = imageEditor.getZoom();
        if(zoom == 100 || imageEditor.useZoom()){
            return {
                width: imageEditor.image.width(),
                height: imageEditor.image.height()
            }
        }else{
            return{
                width: Math.round(imageEditor.image.width()/imageEditor.getPct(zoom)),
                height: Math.round(imageEditor.image.height()/imageEditor.getPct(zoom))
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
            cs.x1 = Math.round(cs.x1/zoomPct);
            cs.x2 = Math.round(cs.x2/zoomPct);
            cs.y1 = Math.round(cs.y1/zoomPct);
            cs.y2 = Math.round(cs.y2/zoomPct);
            return cs
        }
    }
    
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