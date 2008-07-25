ImageEditor = function(){
    
    imageEditor = this;
    
    imageEditor.resizeButton = $('div.imageButtons input.resize');
    imageEditor.cropButton = $('div.imageButtons input.crop');
    imageEditor.saveButton = $('div.imageButtons input.save');
    imageEditor.rotateRightButton = $('div.imageButtons input.rotate-right');
    imageEditor.rotateLeftButton = $('div.imageButtons input.rotate-left');
    imageEditor.flipHorizontallyButton = $('div.imageButtons input.flipOnHorizontalAxis');
    imageEditor.flipVerticallyButton = $('div.imageButtons input.flipOnVerticalAxis');
    imageEditor.serverResizeSaveButton = $('input#serverResizeSaveButton');
    imageEditor.serverCropSaveButton = $('input#serverCropSaveButton');

    imageEditor.image = $('div.imageEditor div.imageContainer img.sourceImage');
    imageEditor.imageWidth = $('div.imageEditor input.imageWidth').attr('value');
    imageEditor.imageHeight = $('div.imageEditor input.imageHeight').attr('value');
    imageEditor.cropSelection = null;
    imageEditor.cropperBorderSize = 2;
    imageEditor.imageContainer = $('div.imageEditor div.imageContainer');
    imageEditor.slider = $('div.imageButtons div#slider');
    imageEditor.sliderPercentage = $('div.imageButtons div#slider p');
    
    imageEditor.initialize = function(){
        imageEditor.setInitialSizes();
        imageEditor.setupResizeButton();
        imageEditor.setupCropButton();
        imageEditor.setupSaveButton();
        imageEditor.setupRotates();
        imageEditor.setupSlider();
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
                var width = imageEditor.imageWidth;
                var height = imageEditor.imageHeight;
                if(ui.value != 100){
                    imageEditor.image.width(Math.round(width*imageEditor.getPct(ui.value)));
                    imageEditor.image.height(Math.round(height*imageEditor.getPct(ui.value)));
                }else{
                    imageEditor.image.width(width);
                    imageEditor.image.height(height);
                }
                imageEditor.sliderPercentage.html(ui.value + '%');
            }
        });
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
    
    imageEditor.addResizable = function(){
        imageEditor.image.resizable({
            animate: true,
            animateDuration: 'fast',
            animateEasing: 'swing',
            ghost: true
        });
		imageEditor.resizeButton.attr('value', 'Cancel Resize');
		imageEditor.resizeButton.addClass('editing');
    };
    imageEditor.removeResizable = function(){
        imageEditor.image.resizable('destroy');
		imageEditor.resizeButton.attr('value', 'resize');
		imageEditor.image.attr('style', "");
		imageEditor.image.attr('width', imageEditor.imageWidth);
		imageEditor.image.attr('height', imageEditor.imageHeight);
		imageEditor.resizeButton.removeClass('editing');
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
    };
    imageEditor.removeCropper = function(){
        imageEditor.image.imgAreaSelect({ 
            enable: false,
            hide: true
        });
        imageEditor.cropButton.attr('value', 'crop');
        imageEditor.cropButton.removeClass('editing');
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
    
    imageEditor.getZoom = function(){
        var pc = imageEditor.sliderPercentage.html()
        return parseInt(pc.substr(0, pc.length-1));
    }
    
    imageEditor.getResize = function(){
        var zoom = imageEditor.getZoom();
        if(zoom == 100){
            return {
                width: imageEditor.image.width(),
                height: imageEditor.image.height()
            }
        }else{
            return{
                width: Math.round(imageEditor.image.width()/imageEditor.getPct(zoom)),
                height: Math.round(imageEditor.image.height()/imageEditor.getPct(zoom)),
            }
        }
    };
    
    imageEditor.getCropSelection = function(){
        var zoom = imageEditor.getZoom();
        var zoomPct = imageEditor.getPct(zoom);
        if(zoom == 100){
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
    
    imageEditor.setupSaveButton = function(){
        imageEditor.saveButton.click(function(){
            if(imageEditor.resizeButton.attr('value').substring(0, 6) == "Cancel"){
                var size = imageEditor.getResize();
                kukit.dom.setKssAttribute(imageEditor.serverResizeSaveButton[0], 'width', size.width);
                kukit.dom.setKssAttribute(imageEditor.serverResizeSaveButton[0], 'height', size.height);

                imageEditor.serverResizeSaveButton.trigger('click');
            }else if(imageEditor.cropButton.attr('value').substring(0, 6) == "Cancel"){
                var cs = imageEditor.getCropSelection();
                kukit.dom.setKssAttribute(imageEditor.serverCropSaveButton[0], 'tlx', cs.x1);
                kukit.dom.setKssAttribute(imageEditor.serverCropSaveButton[0], 'tly', cs.y1);
                kukit.dom.setKssAttribute(imageEditor.serverCropSaveButton[0], 'brx', cs.x2);
                kukit.dom.setKssAttribute(imageEditor.serverCropSaveButton[0], 'bry', cs.y2);

                imageEditor.serverCropSaveButton.trigger('click');
            }
        });
    };
    
    imageEditor.initialize();
    
};

$(document).ready(function(){
    document.imageEditor = new ImageEditor();
});