#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import sys
import urllib
import urllib2
import getopt
import logging

__USAGE__ = """%s [-m method] [-p key:value&key:value,...] url

  -m: method
  -p: paramator
"""

def get_request (url, param):
	f = urllib.urlopen(url + '?' + param)
	print f.read()

def post_request (url, param):
	f = urllib.urlopen(url, param)
	print f.read()



if __name__ == '__main__':
	gn, longarg = getopt.getopt(sys.argv[1:], "m:p:")
	method = None
	methods = {'get': get_request,
			   'post': post_request}
	param = ""

	for (opt, optarg) in gn:
		if opt == '-m' and optarg in methods:
			method = methods[optarg]
		elif opt == '-p':
			param = optarg
		else:
			logging.info(__USAGE__ % (sys.argv[0]))
			sys.exit(0)
	
	if longarg and isinstance(longarg,list) and len(longarg):
		longarg = longarg[0]
	else:
		logging.error(__USAGE__ % (sys.argv[0]))
		sys.exit(0)
	
	method(longarg, param)
	sys.exit(0)

