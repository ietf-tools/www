(function() {
    (function($) {
        return $.widget('IKS.hallowagtailsnippetlink', {
            options: {
                uuid: '',
                editable: null
            },
            populateToolbar: function(toolbar) {
                var button, widget;

                widget = this;
                button = $('<span class="' + this.widgetName + '"></span>');
                button.hallobutton({
                    uuid: this.options.uuid,
                    editable: this.options.editable,
                    label: 'Snippets',
                    icon: 'icon-plus',
                    command: null
                });
                toolbar.append(button);
                return button.on('click', function(event) {
                    var lastSelection;

                    lastSelection = widget.options.editable.getSelection();
                    return ModalWorkflow({
                        url: window.chooserUrls.snippetLinkChooser,
                        responses: {
                            snippetChosen: function(snippetData) {
                                var a;

                                a = document.createElement('a');
                                a.setAttribute('href', snippetData.url);
                                a.setAttribute('data-id', snippetData.data.id);
                                a.setAttribute('data-linktype', snippetData.type);
                                if ((!lastSelection.collapsed) && lastSelection.canSurroundContents()) {
                                    lastSelection.surroundContents(a);
                                } else {
                                    a.appendChild(document.createTextNode(snippetData.title));
                                    lastSelection.insertNode(a);
                                }

                                return widget.options.editable.element.trigger('change');
                            }
                        }
                    });
                });
            }
        });
    })(jQuery);

}).call(this);
