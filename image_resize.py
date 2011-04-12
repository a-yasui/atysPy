#!/usr/bin/env python
# -*- coding:utf-8 -*-

import getopt
import os
import sys
import logging

from unilib import util as uniUtil

import Image

IMAGE_SIZE = (405, 540) # w,h
VERBOSE = True


class imageResize (object):
    def __init__ (self, resize):
        self._resize = resize
    
    def resizeImageFromPath(self, fromPath, toPath, types='jpg'):
        import re
        if re.match(r'^\.[jJpPeEgG]{3,4}', types):
            types = 'jpeg'
        elif re.match(r'^\.[pPnNgG]{3}', types):
            types = 'png'
        else:
            logging.warn('%s is unknown type.' , (types))
            return False
    
        im = Image.open(fromPath)
        newimg = im.resize(self._resize, Image.ANTIALIAS)
        if VERBOSE:
            logging.info("%s resize:%s", (uniUtil.decode_string(toPath),
                                            self._resize))
        newimg.save(toPath, types)
        if VERBOSE:
            logging.info("%s savging type:%s", (uniUtil.decode_string(toPath),
                                                    types))
        return True
        

if __name__ == '__main__':
    usage = """usage: %s [hs] [-t jpg/png] [-w width] [-h height] file1..
    -h show this.
    -s sillent (default is verbose)
    -w width. Resize of width pixel.
    -h height. Resize of height pixel.
    -t Save Type jpg/png. default is same as a source image.
""" % (sys.argv[0])
    type = ''

    optlist, filelist = getopt.getopt(sys.argv[1:], 'hsw:h:')
    if not filelist:
        print usage
        sys.exit(0)
    
    for opt,optarg in optlist:
        if opt == '-s':
            VERBOSE = False
        
        elif opt == '-h':
            print usage
            sys.exit(0)
        
        elif opt == '-t':
	    if optarg in ['jpg', 'png']:
		type = optarg

        elif opt == '-w': IMAGE_SIZE[0] = int(optarg)
        elif opt == '-h': IMAGE_SIZE[1] = int(optarg)
        
        else:
            print usage
            sys.exit(0)
    
    # do runing
    resizeObj = imageResize(IMAGE_SIZE)
    
    for files in filelist:
        files = os.path.abspath(files)
        
        if not (os.path.exists(files) and os.path.isfile(files)):
            logging.warning("%s is not file.", uniUtil.decode_string(files))
            continue
        
        # resize for new file
        filename, ext = os.path.splitext(os.path.basename(files))
        filename += '_thumb'
        newfile = os.path.sep.join([os.path.dirname(files), filename+ext])
        
	if type != '':
	    ext = type
        resizeObj.resizeImageFromPath(files, newfile, ext)

