function insertInline(type, id, classname, name) {
    if (type != '----------' && id != '') {
        inline = '<inline type="'+type.replace('/', '.')+'" id="'+id+'" class="'+classname+'" />';
        field = document.getElementById('id_'+name);
        field.value = field.value + inline + '\n';
    }
}
