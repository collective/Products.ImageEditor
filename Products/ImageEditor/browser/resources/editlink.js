(function($){
$(document).ready(function(){

    $('body').append('<div id="image-editor" />');
    $('div > div.field:first-child > img:first-child').
        parent().parent().next().
        append('&mdash; <a href="" id="edit-image">Edit this image</a>');
        $('#edit-image').
        click(function(event) {
            event.preventDefault();
            var field = $(this).parent()[0].id.replace('archetypes-fieldname-', '');
            var url = window.location.pathname + '/../@@imageeditor.inline?field=' + field;
            $('#image-editor').load(encodeURI(url), function() {
                $('.ui-dialog-titlebar-close').attr('href',
                    window.location.href);
                fire('editor_loaded', IMAGE_INFORMATION);
            });
        });

});
})(jQuery);
