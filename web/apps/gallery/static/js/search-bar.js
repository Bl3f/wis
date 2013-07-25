!function($){

    "use strict";

    var Gallery = function(data) {
        this.owner = data.owner;
        this.name = data.name;
        this.slug = data.slug;
        this.count = data.count;
    }

    var SearchBar = function(element, options) {
        this.element = element;
        this.limit = element.attr('data-items');
        this.galleries = [];

        var data = JSON.parse(element.attr('data-dict'));
        for (var i = 0; i < data.length; i++) {
            this.galleries.push(new Gallery(data[i]));
        }
        element.removeAttr('data-dict');
        this.options = options;

        this.init_listeners();
    }

    SearchBar.prototype.init_listeners = function() {
        // DOM initialisation with elements we need
        this.element.attr('autofocus', true)
        this.element.empty();
        this.element.parent().append(this.options.hint);
        this.element.insertAfter($('.tt-hint'));
        this.element.parent().append(this.options.menu);
        this.dropdown = this.element.next($.parseHTML(this.options.menu).class).hide();
        this.hint = $('.tt-hint');

        var that = this;

        // Listener on input
        this.element.on('input', function() {
            var input = $(this).val()

            if (input.length == 0) {
                that.hint.val('');
                return that.dropdown.slideUp(400);
            }

            var galleries = that.find_galleries(input);
            if (galleries.length == 0) {
                that.dropdown.slideUp(400);
                that.hint.val('');
                return;
            }
            if (that.display_in_dropdown(galleries)) {
                that.dropdown.slideDown(400);
            }
            that.active_next();
        }).focus(function() {
            return !that.input_is_empty() && that.dropdown.slideDown(400);
        }).blur(function() {
            that.dropdown.slideUp(400);
        }).keydown(function(e) {
            var keyCode = e.keyCode || e.which;

            if (that.dropdown.children().length == 0 || that.input_is_empty()) {
                return 0;
            }
            if (keyCode == 40 || keyCode == 9) {
                e.preventDefault();
                that.active_next();
            } else if (keyCode == 38) {
                e.preventDefault();
                that.active_previous();
            } else if (keyCode == 13) {
                e.preventDefault();
                $.ajax({
                    url:"/search",
                    type: "POST",
                    data: that.get_gallery_active(),
                    success:function(data){
                        window.location.href = data.redirect;
                    },
                    complete:function(){},
                    error:function (xhr, textStatus, thrownError){

                    }
                });
            }
        });
    }

    SearchBar.prototype.find_galleries = function(input) {
        var re = new RegExp(input.toLowerCase());
        var galleries = this.galleries;
        var matching = [];
        for (var i = 0; i < galleries.length; i++) {
            if (matching.length >= this.limit) {
                return matching;
            }
            if (galleries[i].owner.toLowerCase().match(re) || galleries[i].name.toLowerCase().match(re)) {
                matching.push(galleries[i]);
            }
        }
        return matching.sort(function(elt1, elt2) {
            if (elt1.owner > elt2.owner) {
                return -1;
            } else if (elt1.owner < elt2.owner) {
                return 1;
            } else {
                return 0;
            }
        });
    }

    SearchBar.prototype.display_in_dropdown = function(galleries) {
        this.dropdown.empty();
        var owners_header = new Array();

        for (var i = 0; i < galleries.length; i++) {
            var gallery = galleries[i];
            if ($.inArray(gallery.owner, owners_header)) {
                this.dropdown.append($('<h2>').html(this.options.header).find('h2').append(this.format_header(gallery)));
                owners_header.push(gallery.owner);
            }
            this.dropdown.append($('<span>').html(this.options.item).find('span').append(this.format_suggestions(gallery)).attr('data-index', i));
        }
        return true;
    }

    SearchBar.prototype.format_suggestions = function(gallery){
        return '<p>' + gallery.name + ' - ' + gallery.count + ' photos</p>';
    }

    SearchBar.prototype.format_header = function(gallery) {
        return gallery.owner;
    }

    SearchBar.prototype.active_next = function() {
        var active = this.dropdown.find('.active');
        var items = $('.tt-suggestions', this.dropdown);
        var index = 0;

        for (var i = 0; i < items.length; i++) {
            if (items.eq(i).hasClass('active')) {
                index = (i + 1) % items.length;
            }
        }
        active.removeClass('active');
        items.eq(index).addClass('active');
        this.display_hint(this.get_active());
    }

    SearchBar.prototype.active_previous = function() {
        var active = this.dropdown.find('.active');
        var items = $('.tt-suggestions', this.dropdown);
        var index = items.length - 1;

        for (var i = 0; i < items.length; i++) {
            if (items.eq(i).hasClass('active')) {
                if (i - 1 >= 0) {
                    index = (i - 1);
                }
            }
        }
        active.removeClass('active');
        items.eq(index).addClass('active');
        this.display_hint(this.get_active());
    }

    SearchBar.prototype.is_active = function() {
        if ($('.active', this.dropdown).length == 1) {
            return true;
        }
        return false;
    }

    SearchBar.prototype.input_is_empty = function() {
        return this.element.val() == '';
    }

    SearchBar.prototype.get_active = function() {
        var index = $('.active', this.dropdown).attr('data-index');
        var gallery = this.galleries[index];
        var input = this.element.val();
        var name_result = '', owner_result = '';
        var owner_end = Infinity, name_end = 0;
        for (var i = 0; i < gallery.owner.length; i++) {
            if (input[i] != undefined && input[i].toLowerCase() == gallery.owner[i].toLowerCase()) {
                owner_result += input[i];
            } else {
                owner_end = i;
                owner_result += gallery.owner.slice(i, gallery.owner.length);
                break;
            }
        }
        for (var i = 0; i < gallery.name.length; i++) {
            if (input[i] != undefined && input[i].toLowerCase() == gallery.name[i].toLowerCase()) {
                name_result += input[i];
            } else {
                name_end = i
                name_result += gallery.name.slice(i, gallery.name.length)
                break;
            }
        }

        return (owner_end > name_end) ? owner_result : name_result;
    }

    SearchBar.prototype.get_gallery_active = function() {
        if (this.is_active()) {
            return this.galleries[$('.active', this.dropdown).attr('data-index')];
        }
    }

    SearchBar.prototype.display_hint = function(hint) {
        if (this.is_active()) {
                this.hint.val(hint);
            }

    }

    var options = {
        menu: '<div class="tt-dropdown-menu"></div>',
        item: '<span class="tt-suggestions"></span>',
        hint: '<input class="tt-hint" type="text" autocomplete="off" disabled">',
        header: '<h2 class="gallery-owner"></h2>'
    }

    var searchbar = new SearchBar($('#id_search'), options);

}(window.jQuery);