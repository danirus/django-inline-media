#-*- coding: utf-8 -*-

import os
import shutil
import tempfile

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase as DjangoTestCase

from inline_media.models import InlineType
from inline_media.parser import MySoup, inlines, render_inline
from inline_media.widgets import TextareaWithInlines
from inline_media.tests.models import MediaModelTest


selfClosingTags = ['inline','img','br','input','meta','link','hr']


class ParserTestCase(DjangoTestCase):
    def setUp(self):
        test_content_type = ContentType.objects.get(app_label="tests", model="modeltest")
        InlineType.objects.create(title="testobj", content_type=test_content_type)
        self.obj = MediaModelTest.objects.create(title="The Title", description="Blah blah ...")
        self.tag = u'<inline type="%(type)s" id="%(id)d" class="%(class)s" />' % {
            "type": "tests.mediamodeltest", "id": self.obj.id, "class": "inline_small_left" }

    def test_render_inline(self):
        soup = MySoup(self.tag, selfClosingTags=selfClosingTags)
        rendered_inline = render_inline(soup.find("inline"))
        self.assert_(rendered_inline.get("context", None) != None)
        self.assert_(rendered_inline.get("template", None) != None)
        self.assert_(rendered_inline["context"]["object"] == self.obj)
        self.assert_(rendered_inline["context"]["class"] == u'inline_small_left')
        self.assert_(rendered_inline["context"]["content_type"] == u'tests.mediamodeltest')
        self.assert_(rendered_inline["template"] == u'inline_media/tests_mediamodeltest.html')

    def test_inlines_with_return_list_false(self):
        html_content = inlines(self.tag, return_list=False)
        self.assertEqual(
            '<div class="inline_small_left"><H3>The Title</H3><p>Blah blah ...</p></div>\n',
            html_content)

    def test_inlines_with_return_list_true(self):
        inline_list = inlines(self.tag, return_list=True)
        self.assert_(len(inline_list) == 1)
        self.assert_(inline_list[0]["object"] == self.obj)
        self.assert_(inline_list[0]["class"] == u'inline_small_left')
        self.assert_(inline_list[0]["content_type"] == u'tests.mediamodeltest')

