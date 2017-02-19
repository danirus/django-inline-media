import copy
import six

from django.db.models import fields
try:
    from django.db.models import get_model
except ImportError:
    from django.apps import apps
    get_model = apps.get_model

from inline_media.conf import settings
from inline_media.widgets import TextareaWithInlines


textarea_attrs = None


def build_textarea_attrs(attrdict):
    newdict = {}
    for k, v in six.iteritems(attrdict):
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
    if textarea_attrs is None:
        textarea_attrs = build_textarea_attrs(
            settings.INLINE_MEDIA_TEXTAREA_ATTRS)
    if textarea_attrs.get('default', False):
        attrs = copy.deepcopy(textarea_attrs['default'])
    else:
        attrs = {}
    if textarea_attrs.get(model, False):
        attrs.update(textarea_attrs[model].get(formfield, {}))
    return attrs


class TextFieldWithInlines(fields.TextField):

    def formfield(self, **kwargs):
        # attrs = get_attrs(self.model, self.formfield.im_self.name)
        attrs = get_attrs(self.model, self.name)
        if attrs:
            widget = TextareaWithInlines(attrs=attrs)
        else:
            widget = TextareaWithInlines
        defaults = {"widget": widget}
        kwargs.update(defaults)
        return super(TextFieldWithInlines, self).formfield(**kwargs)


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^inline_media\.fields\.TextFieldWithInlines"])
except:
    pass
