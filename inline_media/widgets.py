#-*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.admin.widgets import AdminTextareaWidget
from django.forms.util import flatatt
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from wysihtml5.widgets import Wysihtml5AdminTextareaWidget

from inline_media.models import InlineType

# Defaulted to Django 1.4 path
ADMIN_IMAGES_PATH = getattr(settings, "ADMIN_IMAGES_PATH", "%s/admin/img" % settings.STATIC_URL)


def inlines_dialog(id):
    name = id[3:]
    widget = u'\
<strong>%(_inline_type_)s:</strong>&nbsp;\
<select id="id_inline_content_type_for_%(name)s" onchange="document.getElementById(\'lookup_id_inline_for_%(name)s\').href = \'../../../\'+this.value+\'/\';" style="margin-right:20px;">\
  <option>----------</option>' % { '_inline_type_': _("Inline type"),
                                   'name': name }
    for inline in InlineType.objects.all():
        widget += u'\
  <option value="%(app_label)s/%(model)s">\
    %(app_label_cap)s: %(model_cap)s\
  </option>' % { "app_label":     inline.content_type.app_label,
                 "model":         inline.content_type.model, 
                 "app_label_cap": inline.content_type.app_label.capitalize(), 
                 "model_cap":     inline.content_type.model.capitalize() }
    widget += u'\
</select>\
<strong>Object:</strong>&nbsp;\
<input type="text" class="vIntegerField" id="id_inline_for_%(name)s" size="10" /> \
<a id="lookup_id_inline_for_%(name)s" href="#" class="related-lookup" onclick="if(document.getElementById(\'id_inline_content_type_for_%(name)s\').value != \'----------\') { return showRelatedObjectLookupPopup(this); }" style="margin-right:20px;">\
  <img src="%(path)s/selector-search.gif" width="16" height="16" alt="Loopup" />\
</a>' % {"name": name,  "path": ADMIN_IMAGES_PATH}
    widget += u'\
<strong>Class:</strong>\
<select id="id_inline_class_for_%(name)s">\
  <option value="inline_mini_left">%(_mini_left_)s</option>\
  <option value="inline_mini_right">%(_mini_right_)s</option>\
  <option value="inline_small_left">%(_small_left_)s</option>\
  <option value="inline_small_right">%(_small_right_)s</option>\
  <option value="inline_medium_left">%(_medium_left_)s</option>\
  <option value="inline_medium_right">%(_medium_right_)s</option>\
  <option value="inline_large_left">%(_large_left_)s</option>\
  <option value="inline_large_right">%(_large_right_)s</option>\
  <option value="inline_full_left">%(_full_left_)s</option>\
  <option value="inline_full_right">%(_full_right_)s</option>\
  <option value="inline_full">%(_full_centered_)s</option>\
</select>' % {'name': name, 
              '_mini_left_': _("Mini left"), 
              '_mini_right_': _("Mini right"),
              '_small_left_': _("Small left"),
              '_small_right_': _("Small right"),
              '_medium_left_': _("Medium left"), 
              '_medium_right_': _("Medium right"),
              '_large_left_': _("Large left"), 
              '_large_right_': _("Large right"),
              '_full_left_': _("Full left"), 
              '_full_right_': _("Full right"),
              '_full_centered_': _("Full centered")}
    widget += u'<input type="button" value="%(_add_)s" style="margin-left:10px;" onclick="return insertInline(document.getElementById(\'id_inline_content_type_for_%(name)s\').value, document.getElementById(\'id_inline_for_%(name)s\').value, document.getElementById(\'id_inline_class_for_%(name)s\').value, \'%(name)s\')" />' % { '_add_': _("Add"), 'name': name }
    return widget


def wysihtml5_render_insert_image_dialog(id):
    return u'\
<div data-wysihtml5-dialog="insertImage" style="display:none">\
  <label>%(_link_)s:</label>&nbsp;\
  <input data-wysihtml5-dialog-field="src" value="http://">\
  <a data-wysihtml5-dialog-action="save" class="button">%(_ok_)s</a>&nbsp;\
  <a data-wysihtml5-dialog-action="cancel" class="button">%(_cancel_)s</a>\
</div>' % { "_link_": _("Image"),
            "_ok_": _("Save"),
            "_cancel_": _("Cancel")
        }


class TextareaWithInlines(AdminTextareaWidget):

    class Media:
        js = (settings.STATIC_URL + "admin/inline_media/js/inlines.js",)

    def __init__(self, attrs=None):
        super(TextareaWithInlines, self).__init__(attrs=attrs)        

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        textarea_widget = u'<textarea%s>%s</textarea>' % (
            flatatt(final_attrs),
            conditional_escape(force_unicode(value)))

        inlines_widget = u'<div style="margin-top:10px">'
        inlines_widget += '<label>'+_("Inlines")+u':</label>'
        inlines_widget += inlines_dialog(final_attrs.get("id", "unknown"))
        inlines_widget += u'<p class="help">'+_("Insert inlines into your body by choosing an inline type, then an object, then a class.")+u'</p>'
        inlines_widget += u'</div>'

        return mark_safe(textarea_widget + inlines_widget)


class Wysihtml5TextareaWithInlines(Wysihtml5AdminTextareaWidget):

    def __init__(self, attrs=None):
        super(Wysihtml5TextareaWithInlines, self).__init__(attrs=attrs)        
        
    def render(self, name, value, attrs=None):
        super_widget = super(Wysihtml5TextareaWithInlines, 
                             self).render(name, value, attrs=attrs)
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        inlines_widget = u'<div style="margin-top:10px">'
        inlines_widget += '<label>'+_("Inlines")+u':</label>'
        inlines_widget += inlines_dialog(final_attrs.get("id", "unknown"))
        inlines_widget += u'<p class="help">'+_("Insert inlines into your body by choosing an inline type, then an object, then a class.")+u'</p>'
        inlines_widget += u'</div>'

        return super_widget + mark_safe(inlines_widget)
