#-*- coding: utf-8 -*-

import os
import shutil
import tempfile

from BeautifulSoup import BeautifulStoneSoup, NavigableString, Tag

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
            '<div class="inline_small_left"><h3>The Title</h3><p>Blah blah ...</p></div>\n',
            html_content)

    def test_inlines_with_return_list_true(self):
        inline_list = inlines(self.tag, return_list=True)
        self.assert_(len(inline_list) == 1)
        self.assert_(inline_list[0]["object"] == self.obj)
        self.assert_(inline_list[0]["class"] == u'inline_small_left')
        self.assert_(inline_list[0]["content_type"] == u'tests.mediamodeltest')


class BeautifulSoupTestCase(DjangoTestCase):
    def setUp(self):

        def print_soup(element):
            html_content = ""
            for entry in element.contents:
                if isinstance(entry, Tag):
                    html_content += print_soup(entry)
                elif isinstance(entry, NavigableString):
                    html_content += "%s" % entry
            return html_content

        selfClosingTags = ['inline','img','br','input','meta','link','hr']
        value = u'<p>The <a href="https://www.djangoproject.com/foundation/">Django Software Foundation (DSF)</a> is kicking off the new year with a <a href="https://www.djangoproject.com/foundation/corporate-membership/">corporate membership</a> drive. Membership of the DSF is one tangible way that your company can publicly demonstrate its support for the Django project, and give back to the Open Source community that has developed Django.</p><p><inline type="inline_media.picture" id="3" class="inline_medium_right" />To kick off this membership drive, we\'re proud to announce our first two corporate members: <a href="http://www.imagescape.com/">Imaginary Landscapes</a> and the <a href="http://www.caktusgroup.com/">Caktus Consulting Group</a>. The DSF would like to thank these two companies for their generous contributions, and for their public support of the DSF and it\'s mission.</p>'
        docsoup = BeautifulStoneSoup(value, selfClosingTags=selfClosingTags)

        rendered_string = u'<div class="inline inline_medium_right"><img src="/media/cache/86/a7/86a7fce73e5af30cde30bbbcd2e598f6.png" alt="Django" /><p class="inline_description"><a href="https://www.djangoproject.com/">The Web Framework for perfectionists with deadlines</a></p></div>'
        picsoup = BeautifulStoneSoup(rendered_string, selfClosingTags=selfClosingTags)
        inline = docsoup.find('inline')
        inline.replaceWith(picsoup)
        self.html_content = "%s" % docsoup

    def test_beautifulsoup_replace_with(self):
        expected = u'<p>The <a href="https://www.djangoproject.com/foundation/">Django Software Foundation (DSF)</a> is kicking off the new year with a <a href="https://www.djangoproject.com/foundation/corporate-membership/">corporate membership</a> drive. Membership of the DSF is one tangible way that your company can publicly demonstrate its support for the Django project, and give back to the Open Source community that has developed Django.</p><p><div class="inline inline_medium_right"><img src="/media/cache/86/a7/86a7fce73e5af30cde30bbbcd2e598f6.png" alt="Django" /><p class="inline_description"><a href="https://www.djangoproject.com/">The Web Framework for perfectionists with deadlines</a></p></div>To kick off this membership drive, we\'re proud to announce our first two corporate members: <a href="http://www.imagescape.com/">Imaginary Landscapes</a> and the <a href="http://www.caktusgroup.com/">Caktus Consulting Group</a>. The DSF would like to thank these two companies for their generous contributions, and for their public support of the DSF and it\'s mission.</p>'
        for char1, char2 in zip(expected, self.html_content):
            print char1, char2
        self.assertEqual(expected, self.html_content)
