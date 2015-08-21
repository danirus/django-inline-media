import tempfile
from django.core.files.storage import FileSystemStorage
from django.utils.functional import LazyObject


class TestStorage(LazyObject):
    def _setup(self):
        self._wrapped = FileSystemStorage(tempfile.mkdtemp())
