import os
import sys
sys.path.insert(0, '..')
sys.path.insert(0, '../..')
os.environ["DJANGO_SETTINGS_MODULE"] = "demo.settings"

import django
django.setup()

from django.core.files.images import ImageFile

from inline_media.models import Picture


picdir = os.path.join(os.path.curdir, os.path.pardir, 'sample-pics')
picture_data = [
    {'id': 23, 'name': 'muc-winter-2005-05.jpg'},
    {'id': 22, 'name': 'muc-winter-2005-04.jpg'},
    {'id': 21, 'name': 'muc-winter-2005-03.jpg'},
    {'id': 20, 'name': 'muc-winter-2005-02.jpg'},
    {'id': 19, 'name': 'muc-winter-2005-01.jpg'},
    {'id': 18, 'name': 'for-slider-02.jpg'},
    {'id': 17, 'name': 'for-slider-05.jpg'},
    {'id': 16, 'name': 'for-slider-06.jpg'},
    {'id': 15, 'name': 'for-slider-01.jpg'},
    {'id': 14, 'name': 'for-slider-04.jpg'},
    {'id': 13, 'name': 'for-slider-03.jpg'},
    {'id': 12, 'name': 'redhat-logo.jpg'},
    {'id': 11, 'name': 'windows8_original.jpg'},
    {'id': 10, 'name': 'open-suse-logo.png'},
    {'id': 9, 'name': 'slackware_logo.jpg'},
    {'id': 8, 'name': 'logo-ubuntu.jpg'},
    {'id': 7, 'name': 'mac-logo.jpg'},
    {'id': 6, 'name': 'debian-logo.jpg'},
    {'id': 5, 'name': 'gentoo-logo.jpg'},
    {'id': 4, 'name': 'freebsd-logo.png'},
    {'id': 3, 'name': 'fedora-logo.png'},
    {'id': 2, 'name': 'django-logo-negative.png'},
    {'id': 1, 'name': 'python-logo-master-v3-TM.png'},
]


def add_pictures():
    for picdic in picture_data:
        pic = Picture.objects.get(pk=picdic['id'])
        with open(os.path.join(picdir, picdic['name']), 'rb') as f:
            image = ImageFile(f)
            pic.picture.save(picdic['name'], image, True)


if __name__ == '__main__':
    add_pictures()
