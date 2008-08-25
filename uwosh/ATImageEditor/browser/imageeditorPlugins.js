kukit.actionsGlobalRegistry.register('setImage', function(oper) {
;;; oper.componentName = '[setImage] action';
    var image = document.imageEditor.image;
    image.fadeOut('def', function(){
        document.imageEditor.removeCropper();
        document.imageEditor.removeResizable();
        $(this).parent().children().remove();
        //do this to force browser to reload image
        document.imageEditor.image = $("<img class='sourceImage' style='display:none' src='" + 
                                        image.attr('src') + "?" + Math.floor(Math.random()*900) + "' />");
        document.imageEditor.imageContainer.append(document.imageEditor.image);
        document.imageEditor.image.fadeIn('fast');
        
        document.imageEditor.reset();
    });
});

kukit.commandsGlobalRegistry.registerFromAction('setImage', kukit.cr.makeSelectorCommand);
