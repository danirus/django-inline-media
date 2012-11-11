#-*- coding: utf-8 -*-

from django.db.models import fields

from inline_media.widgets import TextareaWithInlines, Wysihtml5TextareaWithInlines


class TextFieldWithInlines(fields.TextField):

    def formfield(self, **kwargs):
        defaults = {"widget": TextareaWithInlines}
        defaults.update(kwargs)
        return super(TextFieldWithInlines, self).formfield(**defaults)

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^inline_media\.fields\.TextFieldWithInlines"])


class Wysihtml5TextFieldWithInlines(fields.TextField):

    def formfield(self, **kwargs):
        defaults = {"widget": Wysihtml5TextareaWithInlines}
        defaults.update(kwargs)
        return super(Wysihtml5TextFieldWithInlines, self).formfield(**defaults)

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^inline_media\.fields\.Wysihtml5TextFieldWithInlines"])
