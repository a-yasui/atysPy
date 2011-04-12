#!/usr/bin/env python
#
# -*- encoding:UTF-8 -*-
# $Id: check_disk.py 79 2008-12-28 08:09:40Z yasui $
#
import getopt, os, dircache, re, sys

_REV   = '$Id: check_disk.py 79 2008-12-28 08:09:40Z yasui $'
_USAGE = '''usage: check_disk [dHh] [point]
    this program is sort to filesize or directory size.
    If you wanna sort by file size in directory, add option -d.

    Options
        -d:    Directory sort. default is file sort.
        -H:    Hide directory is skip. default is *NOT* skipping.
        -h:    Show this.
'''

_DIR_SORT = False
_HIDE_IN  = True
_HIDE_RE  = re.compile(r'^\.')
_ROOT_PT  = os.path.abspath(os.path.dirname(__file__))
_BIT_UNIT = ['B', 'K', 'M', "G", 'T', 'P', 'E','Z','Y']
_BIG_BUFFER = []
_DEBUG = True

def carp (*argv):
    if _DEBUG:
        print argv

def cb (size, cnt=0):
    if size == 0:
        return "0" + _BIT_UNIT[cnt]
    n = size/1024
    if n < 0.1:
        return "%d%s" %(size,_BIT_UNIT[cnt])
    return cb(n,cnt+1) 

#
# return value: [[size,path]...]
def getDirInfo (path):
    #
    # return value: (num, [[size, path], ...])
    def _indir (p):
        if _HIDE_RE.match(p) and not _HIDE_IN:
            carp("%s is hidden. skip" %p)
            return (0, [])
        
        selfSize = 0
        buff     = []
        list     = []
    
        try:
            list = dircache.listdir(p)
        except :
            pass
        for f in list:
            if _HIDE_IN and _HIDE_RE.match(f):
                pass
            else:
                if os.path.isdir(p+'/'+f):
                    n = _indir(p+'/'+f)
                    buff += [[n[0], p+'/'+f]]
                    buff += n[1]
                    selfSize += n[0]
                else:
                    selfSize += os.path.getsize(p+'/'+f)
                    if not _DIR_SORT :
                        buff += [[ os.path.getsize(p+'/'+f), p+'/'+f]]
        return (selfSize, buff)
    buff = []
    n = _indir(path)
    buff = [[n[0],_ROOT_PT]]
    buff += n[1]
    return buff

def bufferSort (buff):
    buff.sort(cmp)
    buff.reverse()
    return buff

def main (argv):
    import types

    _ROOT_PT  = os.path.abspath(os.path.dirname(__file__))
    optlist,point = getopt.getopt(argv[1:],"dHh")
    if point and isinstance(point[0], types.StringType) and os.path.isdir(point[0]):
        _ROOT_PT = os.path.abspath(point[0])
    
    for opt,arg in optlist:
        if opt == '-d':
            _DIR_SORT = True
        elif opt == '-H':
            _HIDE_IN = False
        else:
            print _USAGE
            sys.exit(1)
    
    for e in bufferSort(getDirInfo(_ROOT_PT)):
        print "%s: %s" % (e[1], cb(e[0]))

if __name__ == '__main__':
    main(sys.argv)
