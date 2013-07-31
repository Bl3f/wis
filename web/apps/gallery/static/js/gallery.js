!function($){

    "use strict";

    $.fn.get_best = function(){
        var best = null
        $('#gallery .column').each(function() {
            if (best != null) {
                if (best.height() > $(this).height()) {
                    best = $(this)
                }
            } else {
                best = $(this)
            }
        });
        return best;
    };

    $('#gallery a img').each(function(index) {
        var img = $(this).attr('src', $(this).attr('data-url')).load(function() {
            if (!this.complete || typeof this.naturalWidth == "undefined" || this.naturalWidth == 0) {
                console.log('Broken image.')
            } else {
                $.fn.get_best().append($(this).append(img).parent());
            }
        });
    });
}(window.jQuery);