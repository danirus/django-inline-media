# Automatic thumbnail format for Sorl - see:
# http://gregbrown.co.nz/code/sorl-thumbnail-auto-format/
# Source cloned from: https://gist.github.com/1052476

from sorl.thumbnail.conf import settings
from sorl.thumbnail.base import ThumbnailBackend


FORMAT_DICT = {
    'png': 'PNG',
    'jpeg': 'JPEG',
    'jpg': 'JPEG',
}


class AutoFormatBackend(ThumbnailBackend):
    def get_thumbnail(self, file_, geometry_string, **options):
        """
        Sets the format option (if not explicitly set) to the same format as the
        original file.
        """
        if not options.get('format'):
            ext = str(file_).split('.')[-1].lower()
            options['format'] = FORMAT_DICT.get(ext, settings.THUMBNAIL_FORMAT)

        return super(AutoFormatBackend, self).\
            get_thumbnail(file_, geometry_string, **options)
