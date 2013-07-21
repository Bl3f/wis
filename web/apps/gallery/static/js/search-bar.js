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
        this.element.empty();
        this.element.parent().append(this.options.hint);
        this.element.insertAfter($('.tt-hint'));
        this.element.parent().append(this.options.menu);
    }

    var options = {
        menu: '<ul class="typeahead dropdown-menu"></ul>',
        item: '<li><a href="#"></a></li>',
        hint: '<input class="tt-hint" type="text" autocomplete="off" disabled">',
        header: '<h2 class="gallery-owner"></h2>'
    }

    var searchbar = new SearchBar($('#id_search'), options);

}(window.jQuery);