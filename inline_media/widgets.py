#-*- coding: utf-8 -*-

from django.contrib.admin.widgets import AdminTextareaWidget
from django.core.urlresolvers import reverse
from django.forms.util import flatatt
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from inline_media.conf import settings
from inline_media.models import InlineType


class BaseInlinesDialogStr(object):

    def __init__(self, id):
        self.name = id[3:]
        self.widget = None

    def widget_string(self):
        return self._do_the_widget()

    def _do_element_select_type(self, attrs=None):
        widget = u'\
<strong>%(_inline_type_)s:</strong>&nbsp;\
<select id="id_inline_content_type_for_%(name)s" onchange="document.getElementById(\'lookup_id_inline_for_%(name)s\').href = \'../../../\'+this.value+\'/\';" style="margin-left:2px;margin-right:20px;" '
        if attrs:
            widget += " ".join([u'%s="%s"' % (key, value) for key, value in attrs.iteritems()])
        widget += u'><option>----------</option>'
        for inline in InlineType.objects.all():
            widget += u'\
  <option value="%(app_label)s/%(model)s">\
    %(app_label_cap)s: %(model_cap)s\
  </option>' % { "app_label":     inline.content_type.app_label,
                 "model":         inline.content_type.model, 
                 "app_label_cap": inline.content_type.app_label.capitalize(), 
                 "model_cap":     inline.content_type.model.capitalize() }
        widget += u'</select>'
        return widget % {"_inline_type_": _("Inline type"), 
                         "name": self.name}

    def _do_element_input_object(self, attrs=None):
        widget = u'<strong>Object:</strong>&nbsp;\
<input type="text" class="vIntegerField" id="id_inline_for_%(name)s" size="10" '
        if attrs:
            widget += " ".join([u'%s="%s"' % (key, value) for key, value in attrs.iteritems()])
        widget += u'/><a id="lookup_id_inline_for_%(name)s" href="#" class="related-lookup" onclick="if(document.getElementById(\'id_inline_content_type_for_%(name)s\').value != \'----------\') { return showRelatedObjectLookupPopup(this); }" style="margin-right:20px;">'
        widget += u'<img src="%(path)s/selector-search.gif" width="16" height="16" alt="Loopup" /></a>'
        return widget % {"name": self.name,  "path": settings.ADMIN_IMAGES_PATH}
        
    def _do_element_select_class(self, attrs=None):
        widget = u'<strong>Class:</strong>&nbsp;<select id="id_inline_class_for_%(name)s" '
        if attrs:
            widget += " ".join(['%s="%s"' % (key, value) for key, value in attrs.iteritems()])
        widget += u'>\
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
  <option value="inline_full_center">%(_full_center_)s</option>\
</select>'
        return widget % {'name': self.name, 
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
                         '_full_center_': _("Full center")}
    
    def _do_element_button_add(self, attrs=None):
        widget = u'<input type="button" value="%(_add_)s" style="margin-left:10px;" '
        if attrs:
            widget += " ".join([u'%s="%s"' % (key, value) for key, value in attrs.iteritems()])
        widget += u'/>'
        return widget % { '_add_': _("Add"), 'name': self.name }

    def _do_element_button_cancel(self, attrs=None):
        widget = u'<input type="button" value="%(_cancel_)s" style="margin-left:5px" '
        if attrs:
            widget += " ".join([u'%s="%s"' % (key, value) for key, value in attrs.iteritems()])
        widget += u'/>'
        return widget % { "_cancel_": _("Cancel") }

    def _do_the_widget(self):
        if not self.widget:
            self.widget = self._do_element_select_type()
            self.widget += self._do_element_input_object()
            self.widget += self._do_element_select_class()
            self.widget += self._do_element_button_add()
            self.widget += self._do_element_button_cancel()
        return self.widget


class InlinesDialogStr(BaseInlinesDialogStr):
    def _do_element_button_add(self, attrs=None):
        attrs = {"onclick": u"return insertInline(document.getElementById(\'id_inline_content_type_for_%(name)s\').value, document.getElementById(\'id_inline_for_%(name)s\').value, document.getElementById(\'id_inline_class_for_%(name)s\').value, \'%(name)s\')"}
        return super(InlinesDialogStr, self)._do_element_button_add(attrs)

    def _do_element_button_cancel(self, attrs=None):
        return ""


class Wysihtml5InlinesDialogStr(BaseInlinesDialogStr):
    def _do_element_select_type(self, attrs=None):
        widget = u'<input type="hidden" data-wysihtml5-dialog-field="rurl" value="%(rurl)s" />'
        rurl = reverse('inline-media-render-inline', 
                       kwargs={"size": 80, "align": "left", "oid": 0})
        rurl = rurl[:rurl.index("render-image")+len("render-image")]
        return widget % {"rurl":rurl}

    def _do_element_input_object(self, attrs=None):
        widget = u'<strong>%(_image_)s:</strong>&nbsp;\
<input type="text" class="vIntegerField" id="id_inline_for_%(name)s" size="10" data-wysihtml5-dialog-field="oid" style="width:50px"/><a id="lookup_id_inline_for_%(name)s" href="/admin/inline_media/picture/" class="related-lookup" onclick="return showRelatedObjectLookupPopup(this)" style="margin-right:20px;">'
        widget += u'<img src="%(path)s/selector-search.gif" width="16" height="16" alt="Loopup" /></a>'
        return widget % {"_image_": _("Image"), "name": self.name,  "path": settings.ADMIN_IMAGES_PATH}

    def _do_element_select_class(self, attrs=None):
        size_widget = u'\
<strong>%(_size_)s:</strong>&nbsp;\
<select id="id_inline_size_for_%(name)s" data-wysihtml5-dialog-field="size">\
  <option value="80">80</option>\
  <option value="150">150</option>\
  <option value="200">200</option>\
  <option value="250">250</option>\
  <option value="350">350</option>\
</select>' 
        size_widget = size_widget % {'_size_': _("Size"), 'name': self.name}
        align_widget = u'&nbsp;&nbsp;\
<strong>%(_align_)s:</strong>&nbsp;\
<select id="id_inline_align_for_%(name)s" data-wysihtml5-dialog-field="align">\
  <option value="left">%(_left_)s</option>\
  <option value="right">%(_right_)s</option>\
</select>' 
        align_widget = align_widget % {'_align_': _("Align"), 'name': self.name, 
                                       '_left_': _("Left"), '_right_': _("Right") }
        return size_widget + align_widget

    def _do_element_button_add(self, attrs=None):
        attrs = {"data-wysihtml5-dialog-action": "save",
                 "class": "button" }
        return super(Wysihtml5InlinesDialogStr, self)._do_element_button_add(attrs)

    def _do_element_button_cancel(self, attrs=None):
        attrs = {"data-wysihtml5-dialog-action": "cancel",
                 "class": "button" }
        return super(Wysihtml5InlinesDialogStr, self)._do_element_button_cancel(attrs)


class TextareaWithInlines(AdminTextareaWidget):

    class Media:
        css = {
            'all': ("inline_media/css/inline_media.css",)
        }
        js = ("admin/inline_media/js/inlines.js",)

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        textarea_widget = u'<textarea%s>%s</textarea>' % (
            flatatt(final_attrs),
            conditional_escape(force_unicode(value)))

        inlinesWidget = InlinesDialogStr(final_attrs.get("id", "id_%s" % name))
        inlines_widget = u'<div style="margin-top:10px">'
        inlines_widget += '<label>'+_("Inlines")+u':</label>'
        inlines_widget += inlinesWidget.widget_string()
        inlines_widget += u'<p class="help">'+_("Insert inlines into your body by choosing an inline type, then an object, then a class.")+u'</p>'
        inlines_widget += u'</div>'

        return mark_safe(textarea_widget + inlines_widget)


def render_insert_inline_picture_dialog(id):
    inlines_widget = u'<div data-wysihtml5-dialog="insertInlinePicture" style="display:none">'
    inlines_widget += Wysihtml5InlinesDialogStr(id).widget_string()
    inlines_widget += u'</div>'
    inlines_widget += u'<script type="text/javascript" src="admin/inline_media/js/wysihtml5/insertInlineMedia.js"></script>'
    return inlines_widget
