from __future__ import unicode_literals

import copy
from django import VERSION
import json
import six

from django.contrib.admin.widgets import AdminTextareaWidget
from django.core.urlresolvers import reverse
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from inline_media.conf import settings


default_sizes = ['mini', 'small', 'medium', 'large', 'full']


def build_imSizes_array():
    im_sizes = {}
    for inline_type in settings.INLINE_MEDIA_TYPES:
        im_type = inline_type.replace('.', '/')
        im_sizes[im_type] = copy.copy(default_sizes)
        custom_sizes = settings.INLINE_MEDIA_CUSTOM_SIZES.get(inline_type, {})
        for k in [k for k, v in six.iteritems(custom_sizes) if not v]:
            im_sizes[im_type].remove(k)
    return json.dumps(im_sizes)


class BaseInlinesDialogStr(object):

    def __init__(self, id):
        self.name = id[3:]
        self.widget = None

    def widget_string(self):
        return self._do_the_widget()

    def _do_element_select_type(self, attrs=None):
        widget = '''
<script>
//<![CDATA[
var imSizes = %(imSizes)s;
function changeInlineClass(name, type) {
    var opts = '';
    if(imSizes[type] == undefined) {
        opts = '<option>----------</option>';
    } else
        for(var i=0; i<imSizes[type].length; i++) {
            var size = imSizes[type][i];
            opts += '<option value="inline_'+size+'_left">'\
+gettext(size+' left')+'</option>';
            if(imSizes[type][i]=='full')
                opts += '<option value="inline_full_center">'\
+gettext('full center')+'</option>';
            opts += '<option value="inline_'+size+'_right">'\
+gettext(size+' right')+'</option>';
        }
    var elem = document.getElementById('id_inline_class_for_'+name);
    elem.innerHTML = opts;
}
//]]>
</script>''' % {'imSizes': build_imSizes_array()}
        widget += '\
<strong>%(_inline_type_)s:</strong>&nbsp;\
<select id="id_inline_content_type_for_%(name)s" \
onchange="changeInlineClass(\'%(name)s\', this.value);\
document.getElementById(\'lookup_id_inline_for_%(name)s\').href \
= \'/admin/\'+this.value+\'/\';" style="margin-left:2px;margin-right:20px;" '
        if attrs:
            widget += " ".join(['%s="%s"' % (key, value)
                                for key, value in six.iteritems(attrs)])
        widget += '><option>----------</option>'
        for inline_type in getattr(settings, 'INLINE_MEDIA_TYPES', []):
            chunks = inline_type.split('.')
            app_label = '.'.join(chunks[:-1])
            model_name = chunks[-1]
            widget += '\
  <option value="%(app_label)s/%(model)s">\
    %(app_label_cap)s: %(model_cap)s\
  </option>' % {"app_label": app_label,
                "model": model_name,
                "app_label_cap": app_label.capitalize(),
                "model_cap": model_name.capitalize()}
        widget += '</select>'
        return widget % {"_inline_type_": _("Inline type"),
                         "name": self.name}

    def _do_element_input_object(self, attrs=None):
        html = ('<strong>Object:</strong>&nbsp;'
                '<input type="text" class="vIntegerField" '
                'id="id_inline_for_%(name)s" size="10" ')
        if attrs:
            html += " ".join(['%s="%s"' % (key, value)
                              for key, value in six.iteritems(attrs)])
        html += ('/><a id="lookup_id_inline_for_%(name)s" href="#" '
                 'class="related-lookup" onclick='
                 '"if(document.getElementById(\''
                 'id_inline_content_type_for_%(name)s\').value != '
                 '\'----------\') { return '
                 'showRelatedObjectLookupPopup(this); }" '
                 'style="margin-right:20px;">')
        if VERSION < (1, 9):
            html += ('<img src="%(path)s/admin/img/selector-search.gif" '
                     'width="18" height="18" alt="Loopup" /></a>')
            widget = html % {"name": self.name, "path": settings.STATIC_URL}
        else:
            html += '</a>'
            widget = html % {"name": self.name}
        return widget

    def _do_element_select_class(self, attrs=None):
        widget = ('<strong>Class:</strong>&nbsp;<select id='
                  '"id_inline_class_for_%(name)s" ')
        if attrs:
            widget += " ".join(['%s="%s"' % (key, value)
                                for key, value in six.iteritems(attrs)])
        widget += '><option>----------</option></select>'
        return widget % {'name': self.name}

    def _do_element_button_add(self, attrs=None):
        widget = ('<input type="button" value="%(_add_)s" '
                  'style="margin-left:10px;" ')
        if attrs:
            widget += " ".join(['%s="%s"' % (key, value)
                                for key, value in six.iteritems(attrs)])
        widget += '/>'
        return widget % {'_add_': _("Add"), 'name': self.name}

    def _do_element_button_cancel(self, attrs=None):
        widget = ('<input type="button" value="%(_cancel_)s" '
                  'style="margin-left:5px" ')
        if attrs:
            widget += " ".join(['%s="%s"' % (key, value)
                                for key, value in six.iteritems(attrs)])
        widget += '/>'
        return widget % {"_cancel_": _("Cancel")}

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
        attrs = {"onclick": ("return insertInline(document.getElementById"
                             "(\'id_inline_content_type_for_%(name)s\').value, "
                             "document.getElementById(\'id_inline_for_%(name)s"
                             "\').value, document.getElementById(\'"
                             "id_inline_class_for_%(name)s\').value, "
                             "\'%(name)s\')")}
        return super(InlinesDialogStr, self)._do_element_button_add(attrs)

    def _do_element_button_cancel(self, attrs=None):
        return ""


class Wysihtml5InlinesDialogStr(BaseInlinesDialogStr):
    def _do_element_select_type(self, attrs=None):
        widget = ('<input type="hidden" data-wysihtml5-dialog-field="rurl" '
                  'value="%(rurl)s" />')
        rurl = reverse('inline-media-render-inline',
                       kwargs={"size": 80, "align": "left", "oid": 0})
        rurl = rurl[:rurl.index("render-image")+len("render-image")]
        return widget % {"rurl": rurl}

    def _do_element_input_object(self, attrs=None):
        widget = ('<strong>%(_image_)s:</strong>&nbsp;<input type="text" '
                  'class="vIntegerField" id="id_inline_for_%(name)s" '
                  'size="10" data-wysihtml5-dialog-field="oid" '
                  'style="width:50px"/><a id="lookup_id_inline_for_%(name)s" '
                  'href="/admin/inline_media/picture/" class="related-lookup" '
                  'onclick="return showRelatedObjectLookupPopup(this)" '
                  'style="margin-right:20px;">')
        widget += ('<img src="%(path)s/selector-search.gif" width="16" '
                   'height="16" alt="Loopup" /></a>')
        return widget % ({"_image_": _("Image"),
                          "name": self.name,
                          "path": settings.ADMIN_IMAGES_PATH})

    def _do_element_select_class(self, attrs=None):
        size_widget = '\
<strong>%(_size_)s:</strong>&nbsp;\
<select id="id_inline_size_for_%(name)s" data-wysihtml5-dialog-field="size">\
  <option value="80">80</option>\
  <option value="150">150</option>\
  <option value="200">200</option>\
  <option value="250">250</option>\
  <option value="350">350</option>\
</select>'
        size_widget = size_widget % {'_size_': _("Size"), 'name': self.name}
        align_widget = '&nbsp;&nbsp;\
<strong>%(_align_)s:</strong>&nbsp;\
<select id="id_inline_align_for_%(name)s" data-wysihtml5-dialog-field="align">\
  <option value="left">%(_left_)s</option>\
  <option value="right">%(_right_)s</option>\
</select>'
        align_widget = align_widget % {'_align_': _("Align"),
                                       'name': self.name,
                                       '_left_': _("Left"),
                                       '_right_': _("Right")}
        return size_widget + align_widget

    def _do_element_button_add(self, attrs=None):
        attrs = {"data-wysihtml5-dialog-action": "save",
                 "class": "button"}
        return super(Wysihtml5InlinesDialogStr, self).\
            _do_element_button_add(attrs)

    def _do_element_button_cancel(self, attrs=None):
        attrs = {"data-wysihtml5-dialog-action": "cancel",
                 "class": "button"}
        return super(Wysihtml5InlinesDialogStr, self).\
            _do_element_button_cancel(attrs)


class TextareaWithInlines(AdminTextareaWidget):

    class Media:
        css = {
            'all': ("inline_media/css/inline_media.css",)
        }
        js = ("admin/inline_media/js/inlines.js",)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        textarea_widget = '<textarea%s>%s</textarea>' % (
            flatatt(final_attrs),
            conditional_escape(force_text(value)))

        inlinesWidget = InlinesDialogStr(final_attrs.get("id", "id_%s" % name))
        inlines_widget = '<div style="margin-top:10px">'
        inlines_widget += '<label>'+_("Inlines")+':</label>'
        inlines_widget += inlinesWidget.widget_string()
        inlines_widget += ('<p class="help">' +
                           _(("Insert inlines into your body by choosing an "
                              "inline type, then an object, then a class.")) +
                           '</p>')
        inlines_widget += '</div>'

        return mark_safe(textarea_widget + inlines_widget)


def render_insert_inline_picture_dialog(id):
    inlines_widget = ('<div data-wysihtml5-dialog="insertInlinePicture" '
                      'style="display:none">')
    inlines_widget += Wysihtml5InlinesDialogStr(id).widget_string()
    inlines_widget += '</div>'
    inlines_widget += ('<script type="text/javascript" src="'
                       'admin/inline_media/js/wysihtml5/insertInlineMedia.js'
                       '"></script>')
    return inlines_widget
