from django.test import TestCase as DjangoTestCase

from inline_media.conf import settings
from inline_media.utils import remove_tags


class RemoveTagsTestCase(DjangoTestCase):
    def test_remove_tags(self):
        source = '<p>Es war<br>einmal</br>und andere</br>geschichte</p>'
        result = '<p>Es war<br>einmal und andere geschichte</p>'
        self.assertEqual(remove_tags(source, settings.INLINE_MEDIA_REMOVE_TAGS),
                         result)
