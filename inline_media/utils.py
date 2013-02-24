#-*- coding: utf-8 -*-

from inline_media.conf import settings

def unescape_inline(value):
    def unescape(s):
        s = s.replace("&quot;", '"')
        s = s.replace("&lt;", "<")
        s = s.replace("&gt;", ">")
        return s

    init = 0
    newval = u''

    while True:
        istarts = value.find(u'&lt;inline', init)
        if istarts == -1:
            break
        iends = value.find(u'&gt;', istarts) + 4
        newval += value[init:istarts]
        newval += unescape(value[istarts:iends])
        init = iends

    newval += value[init:]
    return newval


def get_css_classes_for_app_model(inline_type):
    if not settings.INLINE_MEDIA_CUSTOM_SIZES.get(inline_type, False):
        return []
    css_classes = []
    custom_sizes = settings.INLINE_MEDIA_CUSTOM_SIZES[inline_type]
    for k in ['mini', 'small', 'medium', 'large']:
        v = custom_sizes.get(k, None)
        if v:
            css_classes.append('inline_%s_left' % k)
            css_classes.append('inline_%s_right' % k)
    v = custom_sizes.get('full', None)
    if v:
        css_classes.append('inline_full_left')
        css_classes.append('inline_full_center')
        css_classes.append('inline_full_right')
    return css_classes
