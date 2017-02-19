from __future__ import unicode_literals

import os

from bs4 import BeautifulSoup, NavigableString, Tag

from django.core.files.images import ImageFile
from django.template import TemplateSyntaxError
from django.test import TestCase as DjangoTestCase

from inline_media.conf import settings
from inline_media.models import Picture
from inline_media.parser import (inlines, render_inline, get_app_model_tuple,
                                 get_model, get_css_class, get_size)
from inline_media.tests.models import ModelMediaTest


# selfClosingTags = ['inline','img','br','input','meta','link','hr']


class ParserTestCase(DjangoTestCase):
    def setUp(self):
        self.obj = ModelMediaTest.objects.create(title="The Title",
                                                 description="Blah blah ...")
        self.tag = ('<inline type="%(type)s" id="%(id)d" class="%(class)s"'
                    '/>') % {"type": "tests.modelmediatest",
                             "id": self.obj.id,
                             "class": "inline_small_left"}

    def test_render_inline(self):
        soup = BeautifulSoup(self.tag, 'html.parser')
        rendered_inline = render_inline(soup.find("inline"))
        self.assert_(rendered_inline.get("context", None) is not None)
        self.assert_(rendered_inline.get("template", None) is not None)
        self.assert_(rendered_inline["context"]["object"] == self.obj)
        self.assertEqual(rendered_inline["context"]["class"],
                         'inline_small_left')
        self.assertEqual(rendered_inline["context"]["content_type"],
                         'tests.modelmediatest')
        self.assertEqual(rendered_inline["template"][0],
                         'inline_media/tests.modelmediatest.small.html')
        self.assertEqual(rendered_inline["template"][1],
                         'inline_media/tests.modelmediatest.default.html')

    def test_inlines_with_return_list_false(self):
        html_content = inlines(self.tag, return_list=False)
        self.assertEqual(('<div class="inline_small_left"><h3>The Title</h3>'
                          '<p>Blah blah ...</p></div>\n'),
                         html_content)

    def test_inlines_with_return_list_true(self):
        inline_list = inlines(self.tag, return_list=True)
        self.assert_(len(inline_list) == 1)
        self.assert_(inline_list[0]["object"] == self.obj)
        self.assert_(inline_list[0]["class"] == 'inline_small_left')
        self.assert_(inline_list[0]["content_type"] == 'tests.modelmediatest')


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

        value = ('<p>The <a href="https://www.djangoproject.com/foundation/">'
                 'Django Software Foundation (DSF)</a> is kicking off the new '
                 'year with a <a href="https://www.djangoproject.com/'
                 'foundation/corporate-membership/">corporate membership</a> '
                 'drive. Membership of the DSF is one tangible way that your '
                 'company can publicly demonstrate its support for the Django '
                 'project, and give back to the Open Source community that has '
                 'developed Django.</p><p><inline type="inline_media.picture" '
                 'id="3" class="inline_medium_right" />To kick off this '
                 'membership drive, we\'re proud to announce our first two '
                 'corporate members: <a href="http://www.imagescape.com/">'
                 'Imaginary Landscapes</a> and the <a href="'
                 'http://www.caktusgroup.com/">Caktus Consulting Group</a>. '
                 'The DSF would like to thank these two companies for their '
                 'generous contributions, and for their public support of the '
                 'DSF and it\'s mission.</p>')
        docsoup = BeautifulSoup(value, 'html.parser')
# selfClosingTags=selfClosingTags)

        rendered_string = ('<div class="inline inline_medium_right"><img src="'
                           '/media/cache/86/a7/86a7fce73e5af30cde30bbbcd2e598f6'
                           '.png" alt="Django" /><p class="inline_description">'
                           '<a href="https://www.djangoproject.com/">The Web '
                           'Framework for perfectionists with deadlines</a>'
                           '</p></div>')
        picsoup = BeautifulSoup(rendered_string, 'html.parser')
# selfClosingTags=selfClosingTags)
        inline = docsoup.find('inline')
        inline.replaceWith(picsoup)
        self.html_content = "%s" % docsoup

    def test_beautifulsoup_replace_with(self):
        expected = ('<p>The <a href="https://www.djangoproject.com/foundation/"'
                    '>Django Software Foundation (DSF)</a> is kicking off the '
                    'new year with a <a href="https://www.djangoproject.com/'
                    'foundation/corporate-membership/">corporate membership</a>'
                    ' drive. Membership of the DSF is one tangible way that '
                    'your company can publicly demonstrate its support for the '
                    'Django project, and give back to the Open Source community'
                    ' that has developed Django.</p><p><div class="inline '
                    'inline_medium_right"><img alt="Django" src="'
                    '/media/cache/86/a7/86a7fce73e5af30cde30bbbcd2e598f6.png"/>'
                    '<p class="inline_description"><a href="https://www.'
                    'djangoproject.com/">The Web Framework for perfectionists '
                    'with deadlines</a></p></div>To kick off this membership '
                    'drive, we\'re proud to announce our first two corporate '
                    'members: <a href="http://www.imagescape.com/">Imaginary '
                    'Landscapes</a> and the <a href="http://www.caktusgroup.'
                    'com/">Caktus Consulting Group</a>. The DSF would like to '
                    'thank these two companies for their generous '
                    'contributions, and for their public support of the DSF '
                    'and it\'s mission.</p>')
        self.maxDiff = None
        self.assertEqual(expected, self.html_content)


class PictureTemplatesTestCase(DjangoTestCase):

    def setUp(self):
        curdir = os.path.dirname(__file__)
        pic = Picture.objects.create(title="android original")
        with open(os.path.join(curdir, "images/android.png"), "rb") as f:
            image_file = ImageFile(f)
            pic.picture.save('android.png', image_file, True)
        self.tag = '<inline type="%(type)s" id="%(id)d" class="%(class)s" />'
        self.params = {"type": "inline_media.picture", "id": pic.id}

    def _inline_with_css_class(self, css_class):
        self.params['class'] = css_class
        inline_tag = self.tag % self.params
        soup = BeautifulSoup(inline_tag, 'html.parser')
# selfClosingTags=['inline'])
        result_dict = render_inline(soup.find('inline'))
        return result_dict['template']

    def test_picture_mini_template(self):
        self.assert_('inline_media/inline_media.picture.mini.html' in
                     self._inline_with_css_class('inline_mini_right'))

    def test_picture_default_template(self):
        self.assert_('inline_media/inline_media.picture.default.html' in
                     self._inline_with_css_class('inline_small_right'))
        self.assert_('inline_media/inline_media.picture.default.html' in
                     self._inline_with_css_class('inline_medium_right'))
        self.assert_('inline_media/inline_media.picture.default.html' in
                     self._inline_with_css_class('inline_large_right'))

    def test_picture_full_template(self):
        self.assert_('inline_media/inline_media.picture.full.html' in
                     self._inline_with_css_class('inline_full_center'))

    def test_mini_picture_custom_size_setting(self):
        self.params['class'] = 'inline_mini_right'
        inline_tag = self.tag % self.params
        soup = BeautifulSoup(inline_tag, 'html.parser')
# selfClosingTags=selfClosingTags)
        rendered_inline = render_inline(soup.find("inline"))
        custom_sizes = settings.INLINE_MEDIA_CUSTOM_SIZES
        self.assertEqual(int(rendered_inline['context']['size']),
                         custom_sizes['inline_media.picture']['mini'])


class ParserHelpersTestCase(DjangoTestCase):
    def setUp(self):
        html = ('<p><inline type="inline_media.picture" id="3" '
                'class="inline_medium_right" />To kick off this...</p>')
        soup = BeautifulSoup(html, 'html.parser')
        self.inline = soup.findAll('inline')[0]

    def test_get_app_model_tuple(self):
        self.assertEqual(get_app_model_tuple(self.inline),
                         ('inline_media', 'picture'))

    def test_get_model(self):
        self.assertEqual(get_model('inline_media', 'picture'), Picture)

    def test_get_css_class(self):
        self.assertEqual(get_css_class(self.inline), 'inline_medium_right')


class ParserHelpersBadInlineTestCase(DjangoTestCase):
    def setUp(self):
        html = ('<p><inline type="inline_media.pictuRRRU" id="3" '
                'classSSS="inline_medium_right" />To kick off this...</p>')
        soup = BeautifulSoup(html, 'html.parser')
        self.inline = soup.findAll('inline')[0]

    def test_get_model_raises_template_syntax_error(self):
        with self.assertRaises(TemplateSyntaxError):
            get_model('inline_media', 'picturegkjr')

    def test_get_css_class_raises_template_syntax_error(self):
        with self.assertRaises(TemplateSyntaxError):
            get_css_class(self.inline)


class ParserHelperGetSizeTestCase(DjangoTestCase):
    def test_with_wrong_size_class(self):
        inline_type = 'inline_media.picture'
        css_class = 'inlime_mediuN_bright'
        self.assert_(get_size(inline_type, css_class) == (None, None))

    def test_with_wrong_inline_type(self):
        inline_type = 'inliMe_meRDE.pictuRR'
        css_class = 'inline_medium_right'
        self.assert_(get_size(inline_type, css_class) == (None, 'medium'))

    def test_with_modified_class(self):
        inline_type = 'inline_media.picture'
        css_class = 'inline_mini_right'
        self.assert_(get_size(inline_type, css_class) == ('81', 'mini'))

    def test_with_disabled_class(self):
        inline_type = 'inline_media.pictureset'
        css_class = 'inline_small_left'
        self.assert_(get_size(inline_type, css_class) == (None, None))
        css_class = 'inline_small_right'
        self.assert_(get_size(inline_type, css_class) == (None, None))

    def test_with_regular_picture(self):
        inline_type = 'inline_media.picture'
        css_class = 'inline_medium_right'
        self.assert_(get_size(inline_type, css_class) == ('200', 'medium'))


class RenderInlineTestCase(DjangoTestCase):
    def test_raises_when_not_size_class(self):
        html = ('<p><inline type="inline_media.picture" id="3" '
                'class="inline_mediuN_right" />To kick off this...</p>')
        soup = BeautifulSoup(html, 'html.parser')
        inline = soup.findAll('inline')[0]
        with self.assertRaises(Exception):
            render_inline(inline)

    def test_raises_when_object_does_not_exist(self):
        html = ('<p><inline type="inline_media.picture" id="30000" '
                'class="inline_medium_right" />To kick off this...</p>')
        soup = BeautifulSoup(html, 'html.parser')
        inline = soup.findAll('inline')[0]
        with self.assertRaises(Picture.DoesNotExist):
            render_inline(inline)

    def test_raises_when_no_inline_has_no_id_attribute(self):
        html = ('<p><inline type="inline_media.picture" '
                'class="inline_medium_right" />To kick off this...</p>')
        soup = BeautifulSoup(html, 'html.parser')
        inline = soup.findAll('inline')[0]
        with self.assertRaises(TemplateSyntaxError):
            render_inline(inline)
