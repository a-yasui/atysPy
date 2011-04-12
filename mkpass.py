#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,os
import re
import random
import string

def randomstr(length):
	stri = string.lowercase + string.uppercase + string.digits
	return ''.join([random.choice(stri) for x in xrange(length)])

if __name__ == '__main__':
	if len(sys.argv) > 1:
		length = sys.argv[1]
		if re.match(r'^\d+$', length):
			print randomstr(int(length))
	else:
		print "%s length" % (sys.argv[0])

