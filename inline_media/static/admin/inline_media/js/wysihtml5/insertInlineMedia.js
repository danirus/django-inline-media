wysihtml5.commands.insertInlinePicture = {
    exec: function(composer, command, value) {
	django.jQuery.get(value['rurl']+"/"+value['size']+"/"+value['align']+"/"+value['oid'],
			  function(data) {
			      composer.commands.exec("insertImage", data);
			      return;
			  });
    },
    state: function(composer) {
	return false;
    }
};
