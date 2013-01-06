#-*- coding: utf-8 -*-

from django.db.models import fields, get_model

from inline_media.conf import TEXTAREA_ATTRS
from inline_media.widgets import TextareaWithInlines


textarea_attrs = None 


def build_textarea_attrs(attrdict):
    newdict = {}
    for k, v in attrdict.iteritems():
        if k == 'default':
            newdict[k] = v
            continue
        app_label = ".".join(k.split('.')[0:-1])
        model = k.split('.')[-1]
        klass = get_model(app_label, model)
        newdict[klass] = v
    return newdict


def get_attrs(model, formfield):
    global textarea_attrs
    if textarea_attrs == None:
        textarea_attrs = build_textarea_attrs(TEXTAREA_ATTRS)
    attrs = textarea_attrs.get('default', {})
    if textarea_attrs.get(model, False):
        attrs.update(textarea_attrs[model].get(formfield, {}))
    return attrs


class TextFieldWithInlines(fields.TextField):

    def formfield(self, **kwargs):
        attrs = get_attrs(self.model, self.formfield.im_self.name)
        if attrs:
            widget = TextareaWithInlines(attrs=attrs)
        else: widget = TextareaWithInlines
        defaults = {"widget": widget}
        kwargs.update(defaults)
        return super(TextFieldWithInlines, self).formfield(**kwargs)

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^inline_media\.fields\.TextFieldWithInlines"])
