#-*- coding: utf-8 -*-

import os

from django.core.files.images import ImageFile
from django.test import TestCase as DjangoTestCase

from inline_media.conf import settings
from inline_media.models import Picture, PictureSet
from inline_media.tests.forms import TestModelForm

class PictureTestCase(DjangoTestCase):
    def setUp(self):
        curdir = os.path.dirname(__file__)
        image_1 = ImageFile(open(os.path.join(curdir, "images/android.png"), "rb"))
        self.picture_1 = Picture.objects.create(title="android original", picture=image_1)
        image_2 = ImageFile(open(os.path.join(curdir, "images/palandroid.png"), "rb"))
        self.picture_2 = Picture.objects.create(title="android clone", picture=image_2)
        

    def test_find_duplicates_of_a_picture(self):
        duplicates = Picture.objects.find_duplicates(self.picture_1)
        self.assert_(len(duplicates) == 1)
        self.assert_(duplicates[0] == self.picture_2)
        # test duplicates as a property
        self.assert_(self.picture_1.duplicates == [self.picture_2])


class PictureSetTestCase(DjangoTestCase):
    def setUp(self):
        curdir = os.path.dirname(__file__)
        image_1 = ImageFile(open(os.path.join(curdir, "images/android.png"), "rb"))
        self.picture_1 = Picture.objects.create(title="android original", picture=image_1)
        image_2 = ImageFile(open(os.path.join(curdir, "images/palandroid.png"), "rb"))
        self.picture_2 = Picture.objects.create(title="android clone", picture=image_2)
        image_3 = ImageFile(open(os.path.join(curdir, "images/theweb.jpg"), "rb"))
        self.picture_3 = Picture.objects.create(title="the web", picture=image_3)
        self.picset = PictureSet.objects.create(title="example set", slug="example-set", 
                                                cover=self.picture_3, order="3,1,2")
        self.picset.pictures.add(self.picture_1)
        self.picset.pictures.add(self.picture_2)
        self.picset.pictures.add(self.picture_3) 

                                  
    def test_pictureset_get_picture_titles_as_ul(self):
        self.assertEqual(
            self.picset.picture_titles_as_ul(),
            '<ul><li>the web (cover)</li><li>android original</li><li>android clone</li></ul>')

    def test_pictureset_get_picture_titles_as_ul(self):
        self.assertEqual(
            self.picset.pictures_in_order(), 
            [self.picture_3, self.picture_1, self.picture_2])


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
        for k, v in attrs.iteritems():
            self.assert_(widget.attrs.get(k, '') == v)
