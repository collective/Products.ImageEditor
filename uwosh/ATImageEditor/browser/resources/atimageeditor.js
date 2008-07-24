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
    
    imageEditor.initialize = function(){
        
        imageEditor.setupResizeButton();
        imageEditor.setupCropButton();
        imageEditor.setupSaveButton();
        imageEditor.setupRotates();
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
    
    imageEditor.getResize = function(){
        return {
            width: imageEditor.image.width(),
            height: imageEditor.image.height()
        }
    };
    
    imageEditor.setupSaveButton = function(){
        imageEditor.saveButton.click(function(){
            if(imageEditor.resizeButton.attr('value').substring(0, 6) == "Cancel"){
                var size = imageEditor.getResize();
                kukit.dom.setKssAttribute(imageEditor.serverResizeSaveButton[0], 'width', size.width);
                kukit.dom.setKssAttribute(imageEditor.serverResizeSaveButton[0], 'height', size.height);

                imageEditor.serverResizeSaveButton.trigger('click');
            }else if(imageEditor.cropButton.attr('value').substring(0, 6) == "Cancel"){
                kukit.dom.setKssAttribute(imageEditor.serverCropSaveButton[0], 'tlx', imageEditor.cropSelection.x1);
                kukit.dom.setKssAttribute(imageEditor.serverCropSaveButton[0], 'tly', imageEditor.cropSelection.y1);
                kukit.dom.setKssAttribute(imageEditor.serverCropSaveButton[0], 'brx', imageEditor.cropSelection.x2);
                kukit.dom.setKssAttribute(imageEditor.serverCropSaveButton[0], 'bry', imageEditor.cropSelection.y2);

                imageEditor.serverCropSaveButton.trigger('click');
            }
        });
    };
    
    imageEditor.initialize();
    
};

$(document).ready(function(){
    document.imageEditor = new ImageEditor();
});