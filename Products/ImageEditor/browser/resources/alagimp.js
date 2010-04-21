function Event(){
    this.handlers = [];
}

var EVENTS = {
    before_image_reload : new Event(),
    after_image_reload : new Event(),
    before_action_execute : new Event(),
    after_action_execute : new Event(),
    action_button_clicked : new Event(),
    apply_button_clicked : new Event(),
    editor_loaded : new Event(),
    before_image_zoom_change: new Event(),
    after_image_zoom_change: new Event()
}

function on(events){
    return {
        accomplish : function(fn){
            if(typeof(events) == "string"){
                events = [events];
            }
            for(var i = 0; i < events.length; i++){
                EVENTS[events[i]].handlers.push(fn);   
            }
        }
    };
};

function fire(event, arg){
    for(var i = 0; i < EVENTS[event].handlers.length; i++){
        if(arg == undefined){
            EVENTS[event].handlers[i]();
        }else{
            EVENTS[event].handlers[i](arg);
        }
    }
}


var IMAGE_INFORMATION = { height: "-", width: "-", size: "" };

function set_status_bar_info(){
    (function($){
    $('#status-bar-information').html(
        IMAGE_INFORMATION.size + " " + 
        IMAGE_INFORMATION.width + "x" + 
        IMAGE_INFORMATION.height
    );
    })(jQuery);
}

function set_image_size_by_percentage(){
    var percentage = parseFloat(jQuery("#zoom-slider-value").attr('value'));
    
    var w = Math.round(IMAGE_INFORMATION.width*percentage);
    var h = Math.round(IMAGE_INFORMATION.height*percentage);

    jQuery('#source-image').width(w);
    jQuery('#source-image').height(h);
}

function set_image_zoom_labels(arg){
    jQuery("#zoom-slider p").html((parseFloat(jQuery("#zoom-slider-value").attr('value')) * 100) + "%");
}

(function($){
$(document).ready(function(){

    function reload_image(data){
        fire('before_image_reload', data);
        IMAGE_INFORMATION = data;
        
        var image = $("#source-image");
        var image_container = $("#image-container");

        //remove old, add new image
        image_container.html('<img id="source-image" style="display:none" src="' + data.url + '" />');
        image_container.children().show()

        fire('after_image_reload', data);
    }

    function execute(name){
        fire('before_action_execute', name);
        var params = {};
        
        if(ACTION_PARAMETERS[name] == undefined){
            $("#" + name + "-options input").each(function(){
                if ($(this).attr('type') != "button"){
                    params[$(this).attr('name')] = $(this).attr('value');
                }
            });
            $("#" + name + "-options select").each(function(){
                var select = $(this);
                select.find('option').each(function(){
                    if(this.selected){
                        params[select.attr('name')] = $(this).attr('value');
                    }
                });
            });
        }else{
            params = ACTION_PARAMETERS[name]();
        }

        $("#kss-spinner").show()
        $.getJSON(
            $('base').attr('href') + '/@@execute?action_name=' + name, 
            params, 
            function(data, status){
                reload_image(data);
                $("#kss-spinner").hide()
            }
        );
        
        $('div.image-edit-action').hide();
        $('input.active').removeClass('active');
        
        fire('after_action_execute', name);
    }

    $('.image-edit-apply-button').click(function(){
        fire('apply_button_clicked', this);
        execute($(this).attr('name'));
    });

    //setup dialogs
    $("div#options div.image-edit-action").each(function(){
        var obj = $(this);
        var id = obj.attr('id');
        if(obj.children().size() > 1){
            obj.dialog({
                autoOpen:false,
                resizable:true,
                modal: true,
                draggable: true,
                title: $("#" + id.substring(0, id.length - "-options".length) + "-button").attr('alt'),
                overlay: {
                    opacity: 0.7,
                    background: 'black'
                },
                close: function(event, ui){
                    obj.removeClass('active');
                    $('input.active').removeClass('active');
                }
            });
        }
    });

    $("#buttons input").click(function(){
        var action = $(this).attr('name');
        var apply_button = $("#" + action + "-apply-button");
        var current_options = $("div#options .active");
        var current_button = $('input.active');
        var new_options = $("#" + action + "-options");
        var new_button = $(this);
        
        if(current_button.attr('id') == new_button.attr('id')){
            return;
        }
        
        if (apply_button.size() > 0){
            var btn = this;
            
            function show_options(){
                new_options.show();
                new_options.dialog('open');
                new_options.addClass('active');
                new_button.addClass('active');
                fire('action_button_clicked', btn);
            }
            
            if(current_options.size() == 1){
                //options already down
                current_options.removeClass('active');
                current_button.removeClass('active');
                current_options.hide();
                current_options.dialog('close');
                show_options();
            }else{
                show_options();
            }
        }else{
            execute($(this).attr('name'));
            fire('action_button_clicked', this);
        }
    });
    
    var window_width, window_height;
    if(window.innerWidth!=undefined){
        window_width = window.innerWidth;
        window_height = window.innerHeight;
    }else{
        window_width = document.documentElement.clientWidth;
        window_height = document.documentElement.clientHeight;
    }    
    
    $("#image-container").dialog({
        autoOpen:true,
        resizable:true,
        modal: false,
        draggable: true,
        title: "Image",
        width:window_width - 250,
        height:window_height - 40,
        position:[225, 10],
        close: function(event, ui){
            $("#image-editor-controls").close();
            $("#zoom-slider-wrapper").close();
        },
        closeOnEscape: false,
    });
    
    $("#image-editor-controls").dialog({
        autoOpen:true,
        resizable:false,
        modal:false,
        draggable:true,
        title: "Actions",
        width:200,
        position:[10, 10],
        dialogClass: "image-editor-controls",
        open: function(event, ui) {
            $(".image-editor-controls .ui-dialog-titlebar-close").hide();
        },
        closeOnEscape: false,
    });
    
    /*
    
    Slider Setup
    
    */
    
    $("#zoom-slider").slider({
        min:0,
        max:100,
        value: 100,
        change: function(e, ui){
            fire('before_image_zoom_change', [percentage, e, ui]);
            var percentage = ui.value;
            
            if(percentage == 100){ percentage = 1; }
            else if(percentage > 9){ percentage = parseFloat('.' + percentage); }
            else{ percentage = parseFloat('.0' + percentage); }
            
            $("#zoom-slider-value").attr('value', percentage);
            fire('after_image_zoom_change', [percentage, e, ui]);
        }
    });
    
    /*
    
    End Slider Setup
    
    */
    
    /*
    
    Grabber Setup
    
    */
    
    function add_grabber(){
        $('#source-image').css('cursor', 'move');
        $('#source-image').draggable();
    }
    
    function remove_grabber(){
        $('#source-image').css('cursor', 'default');
        $('#source-image').draggable('destroy');
    }
    
    on(['editor_loaded', 'after_image_reload']).accomplish(function(data){
        add_grabber();
    });
    
    on('action_button_clicked').accomplish(function(btn){
        var action_button_id = $(btn).attr('id');
        if(action_button_id == "resize-button" || action_button_id == "crop-button"){
            remove_grabber();
        }else{
            add_grabber();
        }
    });
    
    /*
    
    End Grabber Setup
    
    */
    
    /*
    
    events
    
    */
    on(['after_image_reload', 'editor_loaded']).accomplish(set_status_bar_info);
    on(['after_image_zoom_change', 'after_image_reload']).accomplish(set_image_size_by_percentage);
    on(['editor_loaded', 'after_image_zoom_change']).accomplish(set_image_zoom_labels);
    on(['after_action_execute']).accomplish(function(name){
        var obj = $("#" + name + "-options");
        if(obj.children().size() > 1){
            obj.dialog('close');
        }
    });
    on(['before_action_execute']).accomplish(function(name){
        $('#status-bar-information').html("applying...");
    });
    
    fire('editor_loaded', IMAGE_INFORMATION);
});
})(jQuery);