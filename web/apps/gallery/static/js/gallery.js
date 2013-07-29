!function($){

    "use strict";

    $('#gallery a img').each(function(index) {
        var img = $(this).attr('src', $(this).attr('data-url')).load(function() {
            if (!this.complete || typeof this.naturalWidth == "undefined" || this.naturalWidth == 0) {
                alert('broken image!');
            } else {
                $(this).append(img);
            }
        });
    });
}(window.jQuery);