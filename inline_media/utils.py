#-*- coding: utf-8 -*-

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
