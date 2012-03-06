#!/usr/bin/env python
# -*- coding: utf_8 -*-
import doctest

def isIPAddress (s):
	r'''
	>>> isIPAddress('1.1.1.1')
	True
	>>> isIPAddress('111.1.1.1')
	True
	>>> isIPAddress('1.1.1.2222')
	False
	'''
	import re
	if not isinstance(s, basestring):
		return False
    
	if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', s):
		return True
	return False

if __name__ == '__main__':
    doctest.testmod()
