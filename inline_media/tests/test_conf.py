from inline_media.conf import settings
from django.test import TestCase as DjangoTestCase

CUSTOM_SIZES = getattr(settings, 'INLINE_MEDIA_CUSTOM_SIZES', {})
TEXTAREA_ATTRS = getattr(settings, 'INLINE_MEDIA_TEXTAREA_ATTRS', {})


class ConfTestCase(DjangoTestCase):

    def test_custom_sizes_setting(self):
        self.assertEqual(CUSTOM_SIZES['inline_media.picture']['mini'], 81)
        self.assertEqual(CUSTOM_SIZES['inline_media.picture']['small'], 150)
        self.assertEqual(CUSTOM_SIZES['inline_media.pictureset']['mini'], None)

    def test_textarea_attrs_setting(self):
        self.assertTrue(TEXTAREA_ATTRS.get('default', False))
        self.assertTrue(TEXTAREA_ATTRS['default'].get('style', False))
        self.assertTrue(TEXTAREA_ATTRS.get('tests.ModelTest', False))
        self.assertTrue(TEXTAREA_ATTRS['tests.ModelTest'].get('second_text',
                                                              False))
