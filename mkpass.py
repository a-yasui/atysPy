#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,os
import re
import random
import string
import getopt

strings = string.lowercase + string.uppercase + string.digits


def randomstr(length):
	global strings
	return ''.join([random.choice(strings) for x in xrange(length)])

if __name__ == '__main__':
	optlist, length = getopt.getopt(sys.argv[1:], "sh")
	
	USAGE = r"""%(command)s [-s] [-h] length
Options

	-s: Salt string. this use all shown stirng.
	-h: show this.

""" % (dict(command = sys.argv[0]))
	
	for opt, optarg in optlist:
		if opt == '-h':
			print USAGE
			sys.exit(0)
		elif opt == '-s':
			strings = "".join([chr(i) for i in range(0x21,0x7e)])
	
	if not length:
		print USAGE
		sys.exit(1)
	
	print randomstr(int(length[0]))

