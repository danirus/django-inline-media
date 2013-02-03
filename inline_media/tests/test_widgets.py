#-*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.forms.models import modelform_factory
from django.test import TestCase as DjangoTestCase
from django.utils.html import conditional_escape

from inline_media.models import InlineType
from inline_media.widgets import TextareaWithInlines, InlinesDialogStr
from inline_media.tests.models import TestModel, AnotherTestModel


class TextareaWithInlinesWidgetAttrs(DjangoTestCase):
    def test_setting_textarea_attrs(self):
        ModelForm1 = modelform_factory(TestModel)
        ModelForm2 = modelform_factory(AnotherTestModel)
        defwidget = ModelForm1.base_fields['first_text'].widget
        widget1 = ModelForm1.base_fields['second_text'].widget
        widget2 = ModelForm2.base_fields['second_text'].widget
        # Model tests.TestModel has specific customized settings
        # for 'second_text' field (see: tests/settings.py)
        self.assertEqual(widget1.attrs['style'], 'font: 13px monospace')
        self.assertEqual(widget1.attrs['rows'], '20')
        # Model tests.AnotherTestModel doesn't have specific settings
        # but inherits 'style' as it's part of 'default' key of
        # settings.INLINE_MEDIA_TEXTAREA_ATTRS
        self.assertEqual(widget2.attrs['style'], 'font: 13px monospace')
        self.assertEqual(widget2.attrs['rows'], defwidget.attrs['rows'])


class AdminTextareaWithInlinesWidgetTestCase(DjangoTestCase):
    def setUp(self):
        ct_picture = ContentType.objects.get(
            app_label="inline_media", model="picture")
        ct_pictureset = ContentType.objects.get(
            app_label="inline_media", model="pictureset")
        InlineType.objects.create(title="Picture", 
                                  content_type=ct_picture)
        InlineType.objects.create(title="PictureSet", 
                                  content_type=ct_pictureset)
        
    def test_render_textareawithinlines_widget(self):
        neilmsg = TestModel.objects.create(
            first_text="One small step for man", 
            second_text="One giant leap for mankind")
        widget = TextareaWithInlines()
        manually_rendered = (u'<textarea rows="10" cols="40" name="test" '
                             u'class="vLargeTextField">One giant leap for '
                             u'mankind</textarea><div style="margin-top:10px">'
                             u'<label>Inlines:</label>')
        manually_rendered += InlinesDialogStr("id_test").widget_string()
        manually_rendered += (u'<p class="help">Insert inlines into your body '
                              u'by choosing an inline type, then an object, '
                              u'then a class.</p></div>')
        self.assertEqual(
            conditional_escape(widget.render("test", neilmsg.second_text)), 
            manually_rendered)

        
