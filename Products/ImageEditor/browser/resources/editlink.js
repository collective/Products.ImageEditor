(function($){
$(document).ready(function(){

    $('body').append('<div id="image-editor" />');
    $('div > div.field:first-child > img:first-child').
        parent().parent().next().
        append('&mdash; <a href="">Edit this image</a>').
        click(function(event) {
            event.preventDefault();
            var field = $(this).parent()[0].id.replace('archetypes-fieldname-', '')
            var url = window.location.pathname + '/../@@imageeditor.inline?field=' + field;
            $('#image-editor').load(encodeURI(url), function() {
                $('.ui-dialog-titlebar-close').attr('href',
                    window.location.href);
                fire('editor_loaded', IMAGE_INFORMATION);
            });
        });

});
})(jQuery);
