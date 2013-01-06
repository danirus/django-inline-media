#-*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase as DjangoTestCase
from django.utils.html import conditional_escape

from inline_media.models import InlineType
from inline_media.widgets import TextareaWithInlines, InlinesDialogStr
from inline_media.tests.models import TestModel


class AdminTextareaWithInlinesWidgetTestCase(DjangoTestCase):
    def setUp(self):
        ct_picture = ContentType.objects.get(app_label="inline_media", model="picture")
        ct_pictureset = ContentType.objects.get(app_label="inline_media", model="pictureset")
        InlineType.objects.create(title="Picture", content_type=ct_picture)
        InlineType.objects.create(title="PictureSet", content_type=ct_pictureset)
        
    def test_render_textareawithinlines_widget(self):
        neilmsg = TestModel.objects.create(
            first_text="One small step for man", 
            second_text="One giant leap for mankind")
        widget = TextareaWithInlines()
        manually_rendered = u'<textarea rows="10" cols="40" name="test" class="vLargeTextField">One giant leap for mankind</textarea><div style="margin-top:10px"><label>Inlines:</label>'
        manually_rendered += InlinesDialogStr("id_test").widget_string()
        manually_rendered += u'<p class="help">Insert inlines into your body by choosing an inline type, then an object, then a class.</p></div>'
        self.assertEqual(conditional_escape(widget.render("test", neilmsg.second_text)), 
                         manually_rendered)

        
