wysihtml5.commands.insertImage = {
    exec: function(composer, command, html) {
	composer.commands.exec("insertHTML", "<H3>Joder Ostias!</H3>");
	return;
    },
    state: function(composer) {
	return false;
    }
};
