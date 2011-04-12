#!/usr/bin/env  python2.5
import dircache
import os
import sys

quiet_flag = False
__DEBUG    = False

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
				   'cp932',			'shift-jis',	'shift_jis_2004',
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

def is_decompile_code (msg):
	import re
	return re.compile(r'^[\-_~\{\}]+').match(msg)

def challenge_encode (msg):
	e = msg.decode(get_jp_encoding_name(msg))
	e = e.encode('ascii').decode('iso-2022-jp')
	return e.encode('utf_8')

def trace (path):

	if not quiet_flag:
		print path
	
	files = dircache.listdir(path)
	for file in files:
		encode     = get_jp_encoding_name(file,'ascii')
		encode_msg = ''

		if encode != 'utf_8':
			newfile = file.decode(encode).encode('utf_8')
			os.rename(path+'/'+file, path+'/'+newfile)
			encode_msg = 'encode for utf_8'
			file = newfile
		
		if not quiet_flag or (quiet_flag and encode_msg != ""):
			print file, " is ", encode , " ", encode_msg
		
		if (os.path.isdir(path+'/'+file)) :
			trace(path+'/'+file)

if __name__ == '__main__':
	_p = '.'
	
	if len(sys.argv)>2:
		quiet_flag = True
		_p = sys.argv[2]
	
	elif len(sys.argv)>1:
		_p = sys.argv[1]
	
	path = os.path.abspath(_p + "/")

	if __DEBUG :
		print "quiet flag:", quiet_flag, " path:",path
	
	if os.path.exists(path) :
		trace(path)
