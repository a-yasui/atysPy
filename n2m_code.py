#!/usr/bin/env python
#  -*- mode:python; coding:utf-8 -*-
#
# name = get_jp_encoding_name(msg[,char_code])
# name is msg encoding type name.
# This only check the Japanese.
#

def get_jp_encoding_name (msg,char_code = 'iso-2022-jp'):
	import types
	
	enc_name = char_code or 'iso-2022-jp'
	check_type = ['utf_8',
				   enc_name,		'iso2022_jp_1', 'iso2022_jp_2',
				   'iso2022_jp_2004','iso2022_jp_3', 'iso2022_jp_ext',
				   'shift-jis',	  'cp932',		'shift_jis_2004',
				   'shift_jisx0213', 'euc_jp',	   'euc_jis_2004',
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


if __name__ == '__main__':
	import sys
	files	= []
	outcode = 'utf_8'
	if len(sys.argv)>2:
		outcode = sys.argv[1]
		files	= sys.argv[2:]
	else :
		files	= sys.argv[1:]
	
	for file in files:
		handle = open(file, "r")
		for line in handle.readlines():
			print line.decode(get_jp_encoding_name(line)).encode(outcode)
		handle.close()

