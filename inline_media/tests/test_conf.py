#-*- coding: utf-8 -*-

import os
import sys

from django.conf import settings
from django.test import TestCase as DjangoTestCase

from inline_media.conf import CUSTOM_SIZES, TEXTAREA_ATTRS


class ConfTestCase(DjangoTestCase):

    def test_custom_sizes_setting(self):
        self.assertEqual(CUSTOM_SIZES['inline_media.picture']['mini'], 81)
        
    def test_textarea_attrs_setting(self):
        self.assertTrue(TEXTAREA_ATTRS.get('default', False)) 
        self.assertTrue(TEXTAREA_ATTRS['default'].get('style', False))
        self.assertEqual(TEXTAREA_ATTRS['default']['style'],
                         settings.INLINE_MEDIA_TEXTAREA_ATTRS['default']['style']) 
        self.assertTrue(TEXTAREA_ATTRS.get('tests.TestModel', False)) 
        self.assertTrue(TEXTAREA_ATTRS['tests.TestModel'].get('second_text', False))
        self.assertEqual(TEXTAREA_ATTRS['tests.TestModel']['second_text'],
                         settings.INLINE_MEDIA_TEXTAREA_ATTRS['tests.TestModel']['second_text']) 
