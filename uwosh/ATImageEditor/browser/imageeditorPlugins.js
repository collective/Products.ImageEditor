kukit.actionsGlobalRegistry.register('setImage', function(oper) {
;;; oper.componentName = '[setImage] action';
    var image = document.imageEditor.image;
    var ie = document.imageEditor;
    
    ie.removeCropper();
    ie.removeResizable();
    image.remove();
    jq('<img id="sourceImage" src="' + oper.parms.url + '" />').appendTo(ie.imageContainer).show();
    ie.image = ie.imageContainer.children();
    ie.reset();
    
    oper.parms.canRedo == '1' ? ie.canRedo(true) : ie.canRedo(false);
    oper.parms.canUndo == '1' ? ie.canUndo(true) : ie.canUndo(false);
    oper.parms.canSave == '1' ? ie.canSave(true) : ie.canSave(false);
});

kukit.commandsGlobalRegistry.registerFromAction('setImage', kukit.cr.makeSelectorCommand);
