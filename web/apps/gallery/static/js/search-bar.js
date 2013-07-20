!function($){

    "use strict";

    var data = JSON.parse($('#id_search').attr('data-dict'))
    var limit = parseInt($('#id_search').attr('data-items'))

    $('#id_search').parent().append("<ul class=\"typeahead\"></ul>");
    $('.typeahead').hide();

    $('#id_search').on('input', function() {
        var input = this;
        var no_display = false;
        var items = 0

        $('.typeahead').empty()
        $.each(data, function(key, val){
            if ( $(input).val() != '' ) {
                var re = new RegExp($(input).val().toLowerCase());
                if ( key.toLowerCase().match(re) ) {
                    $('.typeahead').append("<li><span class=\"icon-user\"></span><h2>" + key + "</h2></li><li><ul class=\"ul_" + key + "\"></ul></li>");
                    for(var i = 0; i < val.length; i++) {
                        items++;
                        var elt = val[i]
                        $('.typeahead .ul_' + key).append("<li data-owner=\"" + key + "\" data-slug=\"" + elt.slug + "\">" + elt.name + " (" + elt.count + " photos)</li>")
                        if (items >= limit) {
                            break;
                        }
                    }
                    no_display = true;
                }
            }
        });
        if ( !no_display ) {
            $('.typeahead').hide();
        } else {
            var last_state = false;
            var elements = $('ul.typeahead ul li');

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
            $('ul.typeahead ul li').click(function() {
                $('#id_search').val($(this).text() + ' de ' + $(this).attr('data-owner'));
                $('.typeahead').slideUp(400);
                $('#id_search').focus()
            });
        }
    });

    $('#id_search').keydown(function(e) {
        var last_up = false
        var last_down = false
        var elements = $('ul.typeahead ul li');
        var last_input = $('#id_search').val()

        if (e.keyCode == 40) {
            for (var j = 0; j < elements.length; j++) {
                if (elements.eq(j).hasClass('active')) {
                    if (j + 1 < elements.length) {
                        elements.eq(j).removeClass('active');
                        elements.eq(j + 1).addClass('active');
                        $('#id_search').val(elements.eq(j + 1).text() + ' de ' + elements.eq(j + 1).attr('data-owner'));
                        last_up = true;
                        break;
                    } else {
                        elements.eq(0).addClass('active');
                        $('#id_search').val(elements.eq(0).text() + ' de ' + elements.eq(0).attr('data-owner'));
                        elements.eq(elements.length - 1).removeClass('active');
                    }
                }
            }
            if (!last_up) {
                elements.eq(0).addClass('active');
                $('#id_search').val(elements.eq(0).text() + ' de ' + elements.eq(0).attr('data-owner'));
                elements.eq(elements.length).removeClass('active');
            }
        } else if (e.keyCode == 38) {
            for (var i = 0; i < elements.length; i++) {
                if (elements.eq(i).hasClass('active')) {
                    if (i - 1 >= 0) {
                        elements.eq(i).removeClass('active');
                        elements.eq(i - 1).addClass('active');
                        $('#id_search').val(elements.eq(i - 1).text() + ' de ' + elements.eq(i - 1).attr('data-owner'));
                        last_down = true;
                        break;
                    }
                }
            }
            if (!last_down) {
                elements.eq(0).removeClass('active');
                elements.eq(elements.length - 1).addClass('active');
                $('#id_search').val(elements.eq(elements.length - 1).text() + ' de ' + elements.eq(elements.length - 1).attr('data-owner'));
            }
        } else if (e.which == 13) {
            $('#id_search').val($('ul.typeahead ul li.active').attr('data-owner') + ';' + $('ul.typeahead ul li.active').attr('data-slug'))
        } else {
        }
    });

}(window.jQuery);