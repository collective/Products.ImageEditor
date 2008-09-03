kukit.actionsGlobalRegistry.register('setImage', function(oper) {
;;; oper.componentName = '[setImage] action';
;;; oper.evaluateParameters(['canRedo', 'canUndo', 'canSave', 'width', 'height', 'size', 'url'], {'withKssSetup':true});

    document.imageEditor.setImage(oper.parms);

});

kukit.commandsGlobalRegistry.registerFromAction('setImage', kukit.cr.makeSelectorCommand);
