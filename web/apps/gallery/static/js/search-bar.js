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
        data = JSON.parse(element.attr('data-dict'));
        for (var i = 0; i < data.length; i++) {
            this.galleries.push(new Gallery(data[i]));
        }
        element.removeAttr('data-dict');
        this.options = options;

        this.init_listeners();
    }

    SearchBar.prototype.debugMyObj = function() {
        console.log("Limit is defined to " + this.limit + " elements");
        console.log(this.galleries);
    }

    SearchBar.prototype.init_listeners = function() {
        // DOM initialisation with elements we need
        this.element.empty();
        this.element.parent().append(this.options.hint);
        this.element.insertAfter($('.tt-hint'));
        this.element.parent().append(this.options.menu);
        this.dropdown = this.element.next($.parseHTML(this.options.menu).class).hide();

        var _ = this;

        // Listener on input
        this.element.on('input', function() {
            var input = $(this).val()

            if (input.length == 0) {
                return _.dropdown.slideUp(400);
            }

            var galleries = _.find_galleries(input);
            if (_.display_in_dropdown(galleries)) {
                _.dropdown.slideDown(400);
            }
        })
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
            this.dropdown.append($('<span>').html(this.options.item).find('span').append(this.format_suggestions(gallery)));
        }
        console.log(owners_header);
        return true;
    }

    SearchBar.prototype.format_suggestions = function(gallery){
        return '<p>' + gallery.name + ' - ' + gallery.count + ' photos</p>';
    }

    SearchBar.prototype.format_header = function(gallery) {
        return gallery.owner;
    }

    var options = {
        menu: '<div class="tt-dropdown-menu"></div>',
        item: '<span class="tt-suggestions"></span>',
        hint: '<input class="tt-hint" type="text" autocomplete="off" disabled">',
        header: '<h2 class="gallery-owner"></h2>'
    }

    var searchbar = new SearchBar($('#id_search'), options);

}(window.jQuery);