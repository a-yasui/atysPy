#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import feedparser
import getopt

_CLIENT_ = 'MOZILLA/5.0'
def getOpener():
    op = urllib2.build_opener()
    op.addheaders = [('User-agent',_CLIENT_)]
    return op

def nests(nest=1):
    if nest <= 0:
        return ""
    return "".join(["\t" for e in range(0,nest)])

def dumpPyObj (obj, nest=0):
    if isinstance(obj, (tuple, list)):
        for e in obj:
            print '%s[' % (nests(nest))
            dumpPyObj(e,nest+1)
            print '%s],' % (nests(nest))

    elif isinstance(obj, dict):
        for k in obj:
            if isinstance(obj[k], (tuple, list, dict)):
                print '%s"%s":{' % (nests(nest),k)
                dumpPyObj(obj[k], nest+1)
                print '%s}' % (nests(nest))
            else:
                print '%s"%s": "%s"' % (nests(nest), k, obj[k])
        

if __name__ == '__main__':
    usage = """usage: %s [h] url
    this program change to json data structure for tree

    -h: help
""" % (sys.argv[0])

    optlist,urllist = getopt.getopt(sys.argv[1:],"h")
    if not urllist:
        print usage
        sys.exit(1)
    
    for opt,optarg in optlist:
        if opt == '-h':
            print usage
            sys.exit(0)
        else:
            print usage
            sys.exit(1)

    for url in urllist:
        rss = feedparser.parse(url)
#        print rss
        dumpPyObj(rss, 1)

