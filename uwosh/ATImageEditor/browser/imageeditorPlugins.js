kukit.actionsGlobalRegistry.register('setImage', function(oper) {
;;; oper.componentName = '[setImage] action';
;;; oper.evaluateParameters(['canRedo', 'canUndo', 'canSave', 'width', 'height', 'size', 'url'], {'withKssSetup':true});

    var oldImage = document.imageEditor.image;
    var newImage = jq('<img style="display:none" id="sourceImage" src="' + oper.parms.url + '" />');
    var ie = document.imageEditor;
    
    ie.imageContainer.css('height', oper.parms.height + "px");
    ie.removeCropperUnintrusive();
    ie.removeResizableUnintrusive();
    
    oldImage.remove();
    newImage.appendTo(ie.imageContainer).fadeIn('slow');
    
    ie.image = ie.imageContainer.children();
    ie.image.naturalWidth = parseInt(oper.parms.width);
    ie.image.naturalHeight = parseInt(oper.parms.height);
    
    ie.reset();
    
    var cr = parseInt(oper.parms.canRedo);
    var cu = parseInt(oper.parms.canUndo);
    var cs = parseInt(oper.parms.canSave);
    
    oper.parms.canRedo == 1 ? ie.canRedo(true) : ie.canRedo(false);
    oper.parms.canUndo == 1 ? ie.canUndo(true) : ie.canUndo(false);
    oper.parms.canSave == 1 ? ie.canSave(true) : ie.canSave(false);
    
    $('span#imageSize').html(oper.parms.size + "");
    ie.imagePixels.html(oper.parms.width + "x" + oper.parms.height);
});

kukit.commandsGlobalRegistry.registerFromAction('setImage', kukit.cr.makeSelectorCommand);
