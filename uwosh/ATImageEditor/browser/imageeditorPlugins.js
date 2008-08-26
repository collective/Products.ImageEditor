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
    
    oper.parms.canRedo == '1' ? ie.redoButton.removeClass('disabled') : ie.redoButton.addClass('disabled');
    oper.parms.canUndo == '1' ? ie.undoButton.removeClass('disabled') : ie.undoButton.addClass('disabled');
    oper.parms.canSave == '1' ? ie.saveButton.removeClass('disabled') : ie.saveButton.addClass('disabled');
    oper.parms.canSave == '1' ? ie.cancelButton.removeClass('disabled') : ie.cancelButton.addClass('disabled');
});

kukit.commandsGlobalRegistry.registerFromAction('setImage', kukit.cr.makeSelectorCommand);
