#-*- coding: utf-8 -*-

import os
import six

from django.core.files.images import ImageFile
from django.test import TestCase as DjangoTestCase

from inline_media.conf import settings
from inline_media.models import License, Picture, PictureSet
from inline_media.tests.forms import TestModelForm

def get_license():
    try:
        return License.objects.get(pk=1)
    except License.DoesNotExist:
        return License.objects.create(
            name="default license",
            link="http://creativecommons.org/licenses/by-sa/3.0/")

def create_picture_1():
    curdir = os.path.dirname(__file__)
    file_1 = os.path.join(curdir, "images/android.png")
    image_1 = ImageFile(open(file_1, "rb"))
    picture_1 = Picture.objects.create(title="android original",
                                       description="picture 1 description",
                                       author="picture 1 author",
                                       license=get_license(),
                                       picture=image_1)
    return picture_1

def create_picture_2():
    curdir = os.path.dirname(__file__)
    file_2 = os.path.join(curdir, "images/palandroid.png")
    image_2 = ImageFile(open(file_2, "rb"))
    picture_2 = Picture.objects.create(title="android clone",
                                       description="picture 2 description",
                                       author="picture 2 author",
                                       license=get_license(),
                                       picture=image_2)
    return picture_2

def create_picture_3():
    curdir = os.path.dirname(__file__)
    file_3 = os.path.join(curdir, "images/theweb.jpg")
    image_3 = ImageFile(open(file_3, "rb"))
    picture_3 = Picture.objects.create(title="the web", 
                                       description="picture 3 description",
                                       author="picture 3 author",
                                       license=get_license(),
                                       picture=image_3)
    return picture_3


class PictureTestCase(DjangoTestCase):
    def setUp(self):
        self.picture_1 = create_picture_1()
        self.picture_2 = create_picture_2()

    def test_picture_defaults(self):
        self.assertTrue(self.picture_1.show_as_link)
        self.assertTrue(self.picture_1.show_description_inline)
        self.assertFalse(self.picture_1.show_author)
        self.assertFalse(self.picture_1.show_license)

    def test_find_duplicates_of_a_picture(self):
        duplicates = Picture.objects.find_duplicates(self.picture_1)
        self.assert_(len(duplicates) == 1)
        self.assert_(duplicates[0] == self.picture_2)
        # test duplicates as a property
        self.assert_(self.picture_1.duplicates == [self.picture_2])


class PictureSetTestCase(DjangoTestCase):
    def setUp(self):
        self.picture_1 = create_picture_1()
        self.picture_2 = create_picture_2()
        self.picture_3 = create_picture_3()
        self.values = {
            'title': 'example set', 
            'slug': 'example-set', 
            'order': '3,1,2'
        }

    def create_object(self, **kwargs):
        self.picset = PictureSet.objects.create(**kwargs)
        self.picset.pictures.add(self.picture_1,
                                 self.picture_2,
                                 self.picture_3) 
                                  
    def test_pictureset_get_picture_titles_as_ul(self):
        self.create_object(**self.values)
        self.assertEqual(
            self.picset.picture_titles_as_ul(),
            '<ul><li>the web (cover)</li><li>android original</li><li>android clone</li></ul>')

    def test_pictureset_get_picture_titles_as_ul(self):
        self.create_object(**self.values)
        self.assertEqual(
            [pic for pic in self.picset.next_picture()], 
            [self.picture_3, self.picture_1, self.picture_2])

    def test_should_not_fail_when_no_order(self):
        self.values.pop('order')
        self.create_object(**self.values)
        self.assert_(self.picset.cover() == self.picture_3)

    def test_should_not_fail_when_order_is_uncomplete(self):
        self.values['order'] = "2,"
        self.create_object(**self.values)
        expected_order = [2] + [p.id for p in self.picset.pictures.all() 
                                if p.id!=2]
        retrieved_order = []
        for pic in self.picset.next_picture():
            retrieved_order.append(pic.id)
        self.assertEqual(expected_order, retrieved_order)

    def test_should_not_fail_when_order_has_unrelated_ids(self):
        self.values['order'] = "2234,3123,45656,23"
        self.create_object(**self.values)
        expected_order = [p.id for p in self.picset.pictures.all()]
        retrieved_order = []
        for pic in self.picset.next_picture():
            retrieved_order.append(pic.id)
        self.assertEqual(expected_order, retrieved_order)

    def test_cover_when_order_has_unrelated_ids(self):
        self.values['order'] = "2234,3123,45656,23"
        self.create_object(**self.values)
        self.assertEqual(self.picset.cover(),
                         self.picset.pictures.all()[0])


class ModelFormTestCase(DjangoTestCase):
    """
    Test setting INLINE_MEDIA_TEXTAREA_ATTRS.
    """
    def test_field(self):
        attrs = {}
        attrs.update(settings.INLINE_MEDIA_TEXTAREA_ATTRS['default'])
        attrs.update(settings.INLINE_MEDIA_TEXTAREA_ATTRS['tests.TestModel']['second_text'])
        form = TestModelForm()
        widget = form.fields['second_text'].widget
        for k, v in six.iteritems(attrs):
            self.assert_(widget.attrs.get(k, '') == v)
