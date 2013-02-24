function insertInline(type, id, classname, name) {
    if (type != '----------' && id != '') {
        inline = '<inline type="'+type.replace('/', '.')+'" id="'+id+'" class="'+classname+'" />';
        field = document.getElementById('id_'+name);
	if (document.selection) { // IE
	    field.focus();
	    sel = document.selection.createRange();
	    sel.text = inline;
	} else if (field.selectionStart || field.selectionStart == '0') { // others
	    field.value = field.value.substring(0, field.selectionStart) + inline
		+ field.value.substring(field.selectionEnd, field.value.length);
	} else {
	    field.value += inline;
	}
    }
}

