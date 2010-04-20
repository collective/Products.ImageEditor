(function($){
$(document).ready(function(){

    $('div > div.field:first-child > img:first-child').
        parent().parent().next().
        append('&mdash; <a href="">Edit this image</a>').
        click(function(event) {
            event.preventDefault();
            alert('...edit...');
        });

});
})(jQuery);
