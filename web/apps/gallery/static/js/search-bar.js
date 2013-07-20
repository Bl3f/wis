!function($){

    "use strict";

    var data = JSON.parse($('#id_search').attr('data-dict'))

    $('#id_search').parent().append("<ul class=\"typeahead\"></ul>");
    $('.typeahead').hide();

    $('#id_search').on('input', function() {
        var input = this;
        var no_display = false;
        $('.typeahead').empty()
        $.each(data, function(key, val){
            if ( $(input).val() != '' ) {
                var re = new RegExp($(input).val());
                if ( key.match(re) ) {
                    $('.typeahead').append("<li><span class=\"icon-user\"></span><h2>" + key + "</h2></li><li><ul class=\"ul_" + key + "\"></ul></li>");
                    for(var i = 0; i < val.length; i++) {
                        var elt = val[i]
                        $('.typeahead .ul_' + key).append("<li>" + elt.name + " (" + elt.count + " photos)</li>")
                    }
                    no_display = true;
                }
            }
        });
        if ( !no_display ) {
            $('.typeahead').hide();
        } else {
            var elements = $('ul.typeahead ul li');
            var last_state = false;

            $('.typeahead').slideDown(400);
            $('ul.typeahead ul li').hover(
                function () {
                    for(var i = 0; i < elements.length; i++){
                        if (elements.eq(i).hasClass('active')) {
                            last_state = i;
                            elements.eq(i).removeClass('active')
                            break;
                        }
                    }
                    $(this).addClass('active');
                },
                function () {
                    $(this).removeClass('active');
                    if (last_state) {
                        elements.eq(last_state).addClass('active');
                    }
                }
            );
        }
    });

    $('#id_search').keydown(function(e) {
        var elements = $('ul.typeahead ul li');

        var last_up = false
        var last_down = false
        if (e.keyCode == 40) {
            for (var j = 0; j < elements.length; j++) {
                if (elements.eq(j).hasClass('active')) {
                    if (j + 1 < elements.length) {
                        elements.eq(j).removeClass('active');
                        elements.eq(j + 1).addClass('active');
                        last_up = true;
                        break;
                    } else {
                        elements.eq(0).addClass('active');
                        elements.eq(elements.length - 1).removeClass('active');
                    }
                }
            }
            if (!last_up) {
                elements.eq(0).addClass('active');
                elements.eq(elements.length).removeClass('active');
            }
        } else if (e.keyCode == 38) {
            for (var i = 0; i < elements.length; i++) {
                if (elements.eq(i).hasClass('active')) {
                    if (i - 1 >= 0) {
                        elements.eq(i).removeClass('active');
                        elements.eq(i - 1).addClass('active');
                        last_down = true;
                        break;
                    }
                }
            }
            if (!last_down) {
                elements.eq(0).removeClass('active');
                elements.eq(elements.length - 1).addClass('active');
            }
        } else if (e.keyCode == 13) {
            
        }
    });

}(window.jQuery);