#!/usr/bin/env python
# -*- coding: utf-8 -*-

def expandString (fn):
    r""" http://d.hatena.ne.jp/gnarl/20100921/1285065333

    >>> expandString(u'hoge')
    u'hoge'
    >>> expandString(u'@todesking fuck')
    u'<a href="http://twitter.com/todesking/">@todesking</a> fuck'
    >>> expandString(u'\xe3\x83\xaa\xe3\x83\xb3\xe3\x82\xaf http://example.com/')
    u'\xe3\x83\xaa\xe3\x83\xb3\xe3\x82\xaf <a href="http://example.com/">http://example.com/</a>'
    >>> expandString(u'test hash #huroushotoku')
    u'test hash <a href="http://twitter.com/#search?q=%23huroushotoku">#huroushotoku</a>'

    """
    import re
    import string

    if not isinstance(fn, basestring):
        return ""

    if isinstance(fn, str) and not isinstance(fn, unicode):
        fn = fn.decode('utf_8')
    
    def link_check (k):
        match_str = string.digits + string.lowercase + string.uppercase + '_-%#&?=.,/'
        ptr = 0
        buff = k
        if k[0:4] == 'http':
            ptr = 5 if k[4] == 's' else 4
            if k[ptr:ptr+3] == '://':
                ptr = ptr+4
                while ptr < len(k):
                    if k[ptr] in match_str:
                        ptr += 1
                    else:
                        buff = k[0:ptr]
                        buff = '<a href="'+buff+'">'+buff+'</a>'
                        break
                else:
                    buff = k[0:ptr]
                    buff = '<a href="'+buff+'">'+buff+'</a>'
            else:
                return (0, buff)
        else:
            pass # This is not match to `http'
        return (ptr, buff)
    
    def tw_at_link_check (k):
        match_str = string.digits + string.lowercase + string.uppercase + '_-'
        ptr = 0
        buff = k
        if k[0] == '@':
            ptr += 1
            while ptr < len(k):
                if k[ptr] in match_str:
                    ptr += 1
                else:
                    user = k[0:ptr]
                    buff = '<a href="http://twitter.com/'+user[1:]+'/">'+user+'</a>'
                    break
            else:
                user = k[0:ptr]
                buff = '<a href="http://twitter.com/'+user[1:]+'/">'+user+'</a>'
        return (ptr, buff)

    def search_link_check (k):
        match_str = string.digits + string.lowercase + string.uppercase + '_-'
        ptr = 0
        buff = k
        if k[0] == '#':
            ptr += 1
            while ptr < len(k):
                if k[ptr] in match_str:
                    ptr += 1
                else:
                    search = k[0:ptr]
                    buff = '<a href="http://twitter.com/#search?q=%23'+ search[1:] +'">'+ search +'</a>'
                    break
            else:
                search = k[0:ptr]
                buff = '<a href="http://twitter.com/#search?q=%23'+ search[1:] +'">'+ search +'</a>'
        return (ptr, buff)
        
    
    buff = ""
    ptr = 0
    buff_mode = 0
    buff_modes = [dict(name='link', fnc = link_check),
                  dict(name='at call', fnc = tw_at_link_check),
                  dict(name='hash search', fnc=search_link_check)]
    while ptr < len(fn):
        for k in buff_modes:
            _b = fn[ptr:]
            (result_ptr, buffer) = k['fnc'](_b)
            if result_ptr > 0:
                ptr += result_ptr
                buff += buffer
                break
        else:
            buff += fn[ptr]
            ptr  += 1
    return buff

if __name__ == '__main__':
    import doctest
    doctest.testmod()
