#-*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase as DjangoTestCase
from django.utils.html import conditional_escape

from inline_media.models import InlineType
from inline_media.widgets import TextareaWithInlines
from inline_media.tests.models import ModelTest


class AdminTextareaWithInlinesWidgetTestCase(DjangoTestCase):
    def setUp(self):
        ct_picture = ContentType.objects.get(app_label="inline_media", model="picture")
        ct_pictureset = ContentType.objects.get(app_label="inline_media", model="pictureset")
        InlineType.objects.create(title="Picture", content_type=ct_picture)
        InlineType.objects.create(title="PictureSet", content_type=ct_pictureset)
        
    def test_render_textareawithinlines_widget(self):
        neilmsg = ModelTest.objects.create(
            first_text="One small step for man", 
            second_text="One giant leap for mankind")
        w = TextareaWithInlines()
        manually_rendered = u'<textarea rows="10" cols="40" name="test" class="vLargeTextField">One giant leap for mankind</textarea><div style="margin-top:10px"><label>Inlines:</label><strong>Inline type:</strong>&nbsp;<select id="id_inline_content_type_for_test" onchange="document.getElementById(\'lookup_id_inline_for_test\').href = \'../../../\'+this.value+\'/\';" style="margin-right:20px;"><option>----------</option><option value="inline_media/picture">Inline_media: Picture</option><option value="inline_media/pictureset">Inline_media: Pictureset</option></select><strong>Object:</strong>&nbsp;<input type="text" class="vIntegerField" id="id_inline_for_test" size="10" /> <a id="lookup_id_inline_for_test" href="#" class="related-lookup" onclick="if(document.getElementById(\'id_inline_content_type_for_test\').value != \'----------\') { return showRelatedObjectLookupPopup(this); }" style="margin-right:20px;"><img src="%simg/admin/selector-search.gif" width="16" height="16" alt="Loopup" /></a> <strong>Class:</strong> <select id="id_inline_class_for_test"><option value="inline_mini_left">Mini left</option><option value="inline_mini_right">Mini right</option><option value="inline_small_left">Small left</option><option value="inline_small_right">Small right</option><option value="inline_medium_left">Medium left</option><option value="inline_medium_right">Medium right</option><option value="inline_large_left">Large left</option><option value="inline_large_right">Large right</option><option value="inline_full_left">Full left</option><option value="inline_full_right">Full right</option><option value="inline_full">Full centered</option></select><input type="button" value="Add" style="margin-left:10px;" onclick="return insertInline(document.getElementById(\'id_inline_content_type_for_test\').value, document.getElementById(\'id_inline_for_test\').value, document.getElementById(\'id_inline_class_for_test\').value, \'test\')" /><p class="help">Insert inlines into your body by choosing an inline type, then an object, then a class.</p></div>' % settings.ADMIN_MEDIA_PREFIX
        self.assertEqual(conditional_escape(w.render("test", neilmsg.second_text)), 
                         manually_rendered)
