#!/usr/bin/env python

from pit import Pit

data = dict(username='local', password='test')

Pit.DIRECTORY = '/tmp'

def set():
	Pit.set('test1', dict(data=data))

def get():
	return Pit.get('test1')

if __name__ == '__main__':
	import sys
	if len(sys.argv) != 2:
		print "%s [get/set]" % (sys.argv[0])
		sys.exit(0)
	
	fn = sys.argv[1]
	if   fn == 'set': set()
	elif fn == 'get': print "%s" % get()
