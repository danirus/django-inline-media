#-*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.admin.widgets import AdminTextareaWidget
from django.forms.util import flatatt
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from inline_media.models import InlineType


class TextareaWithInlines(AdminTextareaWidget):

    class Media:
        js = (settings.ADMIN_MEDIA_PREFIX + "inline_media/js/inlines.js",)

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
        inlines_widget += u'<strong>' + _("Inline type") +':</strong>&nbsp;'
        inlines_widget += u'<select id="id_inline_content_type_for_'+name+'" onchange="document.getElementById(\'lookup_id_inline_for_'+name+'\').href = \'../../../\'+this.value+\'/\';" style="margin-right:20px;">'
        inlines_widget += u'<option>----------</option>'

        for inline in InlineType.objects.all():
            inlines_widget += u'<option value="%(app_label)s/%(model)s">%(app_label_cap)s: %(model_cap)s</option>' % (
            {"app_label":     inline.content_type.app_label, 
             "model":         inline.content_type.model, 
             "app_label_cap": inline.content_type.app_label.capitalize(), 
             "model_cap":     inline.content_type.model.capitalize() })
        inlines_widget += u'</select>'

        inlines_widget += u'<strong>Object:</strong>&nbsp;'
        inlines_widget += u'<input type="text" class="vIntegerField" id="id_inline_for_'+name+'" size="10" /> '
        inlines_widget += u'<a id="lookup_id_inline_for_'+name+'" href="#" class="related-lookup" onclick="if(document.getElementById(\'id_inline_content_type_for_'+name+'\').value != \'----------\') { return showRelatedObjectLookupPopup(this); }" style="margin-right:20px;"><img src="%simg/admin/selector-search.gif" width="16" height="16" alt="Loopup" /></a> ' % settings.ADMIN_MEDIA_PREFIX
      
        inlines_widget += u'<strong>Class:</strong> '
        inlines_widget += u'<select id="id_inline_class_for_'+name+'">'
        inlines_widget += u'<option value="inline_small_left">'+_("Small left")+u'</option>'
        inlines_widget += u'<option value="inline_small_right">'+_("Small right")+u'</option>'
        inlines_widget += u'<option value="inline_medium_left">'+_("Medium left")+u'</option>'
        inlines_widget += u'<option value="inline_medium_right">'+_("Medium right")+u'</option>'
        inlines_widget += u'<option value="inline_large_left">'+_("Large left")+u'</option>'
        inlines_widget += u'<option value="inline_large_right">'+_("Large right")+u'</option>'
        inlines_widget += u'<option value="inline_full">'+_("Full centered")+u'</option>'
        inlines_widget += u'</select>'
      
        inlines_widget += u'<input type="button" value="'+_("Add")+u'" style="margin-left:10px;" onclick="return insertInline(document.getElementById(\'id_inline_content_type_for_'+name+'\').value, document.getElementById(\'id_inline_for_'+name+'\').value, document.getElementById(\'id_inline_class_for_'+name+'\').value, \''+name+u'\')" />'
        inlines_widget += u'<p class="help">'+_("Insert inlines into your body by choosing an inline type, then an object, then a class.")+u'</p>'
        inlines_widget += u'</div>'

        return mark_safe(textarea_widget + inlines_widget)
