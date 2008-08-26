ImageEditor = function(){
    
    imageEditor = this;
    
    imageEditor.resizeButton = $('div#actionButtons input#resize');
    imageEditor.cropButton = $('div#actionButtons input#crop');
    imageEditor.saveButton = $('div#manageButtons input#save');
    imageEditor.cancelButton = $('div#manageButtons input#cancel');
    imageEditor.rotateRightButton = $('div#actionButtons input#rotate-right');
    imageEditor.rotateLeftButton = $('div#actionButtons input#rotate-left');
    imageEditor.flipHorizontallyButton = $('div#actionButtons input#flipOnHorizontalAxis');
    imageEditor.flipVerticallyButton = $('div#actionButtons input#flipOnVerticalAxis');
    imageEditor.serverResizeSaveButton = $('input#serverResizeSaveButton');
    imageEditor.serverCropSaveButton = $('input#serverCropSaveButton');
    imageEditor.serverCropAndResize = $('div#actionButtons input#cropAndResize');
    imageEditor.applyButton = $('div#actionButtons input#apply');
    imageEditor.undoButton = $('div#actionButtons input#undo');
    imageEditor.redoButton = $('div#actionButtons input#redo');

    imageEditor.manageButton = $('div#manageButtons');
    imageEditor.actionButtons = $('div#actionButtons');

    imageEditor.image = $('div#imageEditor div#imageContainer img#sourceImage');
    imageEditor.imageContainer = $('div#imageEditor div#imageContainer');
    
    imageEditor.slider = $('div#manageButtons div#slider');
    imageEditor.sliderPercentage = $('div#manageButtons div#slider p');
    imageEditor.useZoomInput = $('div#manageButtons div.useZoom input#useZoom');

    imageEditor.cropSelection = null;
    imageEditor.cropperBorderSize = 2;
    
    imageEditor.initialize = function(){
        imageEditor.setInitialSizes();
        imageEditor.setupResizeButton();
        imageEditor.setupCropButton();
        imageEditor.setupApplyButton();
        imageEditor.setupRotates();
        imageEditor.setupSlider();
        imageEditor.setupUserWarning();
        
        imageEditor.actionButtons.draggable();
        
    };
    
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
        if(v){
            imageEditor.applyButton.removeClass('disabled');
            imageEditor.applyButton.addClass('enabled');
            imageEditor.applyButton[0].disabled = false;
        }else{
            imageEditor.applyButton.addClass('disabled');
            imageEditor.applyButton.removeClass('enabled');
            imageEditor.applyButton[0].disabled = true;
        }
    }
    
    imageEditor.addResizable = function(){
        imageEditor.image.resizable({
            aspectRatio: true
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
		
		if(imageEditor.getZoom() != 100){
		    imageEditor.image.width(imageEditor.resizedImageWidth);
    		imageEditor.image.height(imageEditor.resizedImageHeight);
		}else{
		    imageEditor.image.width(imageEditor.imageWidth);
    		imageEditor.image.height(imageEditor.imageHeight);
		}
    };
    
    imageEditor.setupResizeButton = function(){
        imageEditor.resizeButton.click(function(){
            if(imageEditor.cropButton.attr('value').substring(0, 6) == "Cancel"){
                imageEditor.removeCropper();
                imageEditor.addResizable();
            }else if($(this).attr('value').substring(0, 6) != "Cancel"){
        		imageEditor.addResizable();
        	}else{
        		imageEditor.removeResizable();
        	}
        });
    };
    
    imageEditor.addCropper = function(){
        imageEditor.image.imgAreaSelect({
            onSelectChange: function(image, selection){
                imageEditor.cropSelection = selection;
            },
            selectionColor: 'blue',
            enable: true,
            border: 2,
            show: true,
            x1: 0,
            y1: 0,
            x2: 90,
            y2: 90
        });
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
    }
    
    imageEditor.setupCropButton = function(){
        imageEditor.cropButton.click(function(){
            if(imageEditor.resizeButton.attr('value').substring(0, 6) == "Cancel"){
                imageEditor.removeResizable();
                imageEditor.addCropper();
            }else if($(this).attr('value').substring(0, 6) != "Cancel"){
                imageEditor.addCropper();
        	}else{
        		imageEditor.removeCropper();
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