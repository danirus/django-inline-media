#-*- coding: utf-8 -*-

from django.db.models import fields

from inline_media.widgets import TextareaWithInlines


class TextFieldWithInlines(fields.TextField):

    def formfield(self, **kwargs):
        defaults = {"widget": TextareaWithInlines}
        defaults.update(kwargs)
        return super(TextFieldWithInlines, self).formfield(**defaults)
