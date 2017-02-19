from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class InlineMediaConfig(AppConfig):
    name = 'inline_media'
    verbose_name = _('Inline Media')
