#!/usr/bin/env python
# -*- encoding:utf8 -*-
#
# $Id: save_image.py 81 2009-01-20 06:47:47Z yasui $
import getopt
import sys,os,re
import urllib2
import threading
import logging
from htmllib import HTMLParser
from formatter import NullFormatter
from types import *

_REV = "$Id: save_image.py 81 2009-01-20 06:47:47Z yasui $"
_DEBUG_ = False
_OUTER_HOST_CONTENTS_GET_ = False
_CLIENT = 'Mozilla/5.0'
_BASE_PATH = './'
_VERBOSE = True
_IMAGE_EXT = ['jpeg','jpg','png','gif']
__USING_THREAD_ = False
tagRegex = ['anchorParser',
            'imageParser'];

def MSG(msg):
    if _VERBOSE:
        logging.info(msg)

##
# HTML(XML) Parser class
class siParser (HTMLParser):
    def __init__ (self):
        HTMLParser.__init__(self, NullFormatter())
        self.reg = re.compile(r'.+/(?P<name>.+\.(?:' + "|".join(_IMAGE_EXT) + ')).*$')
        self.links = []
    
    def addLinks(self, url):
        fn = self.reg.match(url)
        if fn:
            if _DEBUG_:
                logging.info("%s save as:%s", url, fn.group('name'))
            self.links.append((url, fn.group('name')))

class anchorParser (siParser):
    
    def anchor_bgn(self, href, name, type): # <a>が見つかった場合の処理
        HTMLParser.anchor_bgn(self, href, name, type)

    def anchor_end(self):      # </a>が見つかった場合の処理
        url = self.anchor
        if url:
            self.addLinks(url)
        self.anchor = None

class imageParser (siParser):
    def __init__ (self):
        HTMLParser.__init__(self, NullFormatter())
        self.links = []
    
    def handle_image(self, source, alt, ismap, align, width, height):
        HTMLParser.handle_image(self, source, alt, ismap, align, width, height)
        self.addLinks(source)

##
# HTTP connection class
class websource:
    def __init__ (self, url = ""):
        if url:
            self.url = url
    
    def getOpener(self):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', _CLIENT)]
        return opener
    
    @staticmethod
    def getContents (self):
        obj = self
        if type(self) == StringType or type(self) == UnicodeType:
            obj = webimage(self)
        
        opener = obj.getOpener()
        try:
            return opener.open(obj.url).read()
        except :
            logging.error("file/url open error: %s", obj.url)
            return None

###
# Saving the local file from web image.
class webimage (websource):
    def __init__ (self, url = ""):
        websource.__init__(self,url)
    
    def _getSaveFileName (self,url, name=''):
        if name != '':
            return _BASE_PATH + '/' + name
        
        name = os.path.basename(url)
        
        # Getting to filename from URL
        def checkFile (f_name, cnt):
            f = re.split(r'\.', f_name)
            (fname, ex) = (".".join(f[0:-1]), f[-1])
            if os.path.exists(_BASE_PATH + '/' + fname + '_' + str(cnt) + "." + ex):
                return checkFile (f_name, cnt+1)
            return _BASE_PATH + '/' + fname + '_' + str(cnt) + "." + ex
    
        if os.path.exists(_BASE_PATH + '/' + name):
            return checkFile(name, 1)
        return _BASE_PATH + '/' + name
    
    def savefile (self, name=''):
        MSG('self url: %s' % (self.url))
        fpath = self._getSaveFileName(self.url, name)
        if _DEBUG_ == True:
            logging.debug("DEBUG:: saving: %s => %s", self.url, fpath)
            return ""
    
        content = self.getContents(self.url)
        try:
            fp = open(fpath, 'w')
            fp.write(content)
            fp.close()
        except:
            logging.error("File is write out error: %s", fpath)

##
# The controll to process that URL/Image get and save from contents.
class webcontent (websource, threading.Thread):
    def __init__ (self, url = "", tagtype = 0, siFooker = None):
        websource.__init__(self,url)
        self.tagType = tagtype
        self.siFooker = siFooker
        threading.Thread.__init__(self)
    
    def get_jp_encoding_name (msg,char_code = 'utf_8'):
        import types
        
        check_type = [char_code,
                      'iso-2022-jp',      'iso2022_jp_1', 'iso2022_jp_2',
                      'iso2022_jp_2004',  'iso2022_jp_3', 'iso2022_jp_ext',
                      'cp932',            'shift-jis',    'shift_jis_2004',
                      'shift_jisx0213',   'euc_jp',       'euc_jis_2004',
                      'euc_jisx0213']
        for enc in check_type:
            try:
                if isinstance(msg, types.StringType):
                    s = msg.decode(enc)
                else:
                    s = unicode(msg,enc)
            except :
                continue
            return enc
        return None
    
    def getImageFromURL(self):
        if self.tagType < 0 or self.tagType >= len(tagRegex):
            self.tagType = 0
            MSG("The tag type is change to 0")
    
        str = websource.getContents(self.url)
    
        str_code = self.get_jp_encoding_name(str)
        if str_code and str_code != 'utf_8':
            str = str.decode(str_code).encode('utf_8')
        str = re.sub(r'>',">\n",str)
    
        MSG("get contents from %s length:%d defaultcode:%s" % (self.url,len(str),str_code))

        def getHOST (url):
            host_re = re.compile(r'http://([^/]+)/')
            return host_re.findall(url)[0]
    
        parser = globals()[tagRegex[tagType]]()
        parser.feed(str)
        parser.close()
        
        for image_url, image_name in parser.links:
            if not re.match(r'^http://', image_url):
                image_url = 'http://%s/%s' % (getHOST(self.url), image_url)
            
            if _OUTER_HOST_CONTENTS_GET_ == True:
                if not (getHOST(self.url) == getHOST(image_url)):
                    continue   
            imgobj = self.siFooker(image_url)
            imgobj.savefile(image_name)

    def run(self):
        self.getImageFromURL()

## 
# Process is not threading.
def gonnaFork ():
    pid = 0
    try:
        pid = os.fork()
    except OSError:
        logging.error("fork error #1 faild.")
        sys.exit(1)
    if pid == 0:
        # Child is running over.
        pass
    else:
        MSG("Born the child.")
        sys.exit(1)


##
# Running Process
def runProcess(fork=False, usingThread=False,
               opt=dict(urllist=[],tagType=0,compless='',siFooker=None)):
    if fork:
        gonnaFork()
    
    if usingThread:
        for th in [webcontent(url, opt['tagType'], opt['siFooker'])
                   for url in opt['urllist']]:
            th.run()
    else:
        for url in opt['urllist']:
            obj = webcontent(url, opt['tagType'], opt['siFooker']).getImageFromURL()


if __name__ == '__main__':
    usage = """usage: %s [hqTF] [-t <tag type>] [-p <save_directory>] url

This program is getting to image from web contents for save to local.
When if double to filename, this is append to '_[\d]' for it.

===== HELP Arguments =========
    -h  show this.

===== Support Arguments ======
    -q  Quiet. Default is verbose.
    -t  get to tag type. The param are ['link', 'img']. default is 'link'
        link: These are image from a tag.
        img:  These are image tag in contents.
    -T  Using thread. default is False
    -F  The process is running for background. default is False.
    -O  The others server image get flag. default is False.
        When false it is not get to others server image.

===== Save Option ============
    -p  save directory path. Default is './'

===== Developer Option =======
    -D  Put on to Debug flug.
        This is *NOT* to save for local.

    Version: %s""" % (sys.argv[0], _REV)
   
    optlist = urllist = None
    try :
        optlist,urllist = getopt.getopt(sys.argv[1:],'DOhqFTp:t:')
        if not urllist:
            print (usage)
            sys.exit(1)
    except getopt.GetoptError:
        print usage
        sys.exit(1)

    tagType = 0 # 'link' = 0, 'img' = 1
    isFork = False
    for opt,optarg in optlist:
        if opt == '-h':
            print usage
            sys.exit(0)
        elif opt == '-q':
            _VERBOSE = False
        elif opt == '-p':
            if not os.path.exists(optarg):
                logging.error("%s is not found", optarg)
                print usage
                sys.exit(1)

            _BASE_PATH = optarg
        elif opt == '-t':
            if optarg == 'link':
                tagType = 0
            elif optarg == 'img':
                tagType = 1

        elif opt == '-F':
            # Fork
            isFork = True
        
        elif opt == '-T':
            __USING_THREAD_ = True
        elif opt == '-D':
            _DEBUG_ = True
        
        elif opt == '-O':
            _OUTER_HOST_CONTENTS_GET_ = True
        
        else :
            logging.error("unknown option: %s", optarg)
            print usage
            sys.exit(1)

    # running main process
    runProcess(isFork, __USING_THREAD_,
        dict(urllist=urllist,tagType=tagType, siFooker=webimage))
