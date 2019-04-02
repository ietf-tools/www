function(modal) {
    modal.respond('snippetChosen', {{ json|safe }});
    modal.close();
}
