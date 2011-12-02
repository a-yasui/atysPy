# -*- coding: utf-8 -*-
import logging

# 日本語ショートカット一覧
__Jp_Encode_ShortCut_Map__ = dict(
	SHIFT_JIS= 'shift_jisx0213',
	SHIFTJIS = 'shift_jisx0213',
	SJIS     = 'shift_jisx0213',
	EUC_JP   = 'euc_jisx0213',
	EUCJP    = 'euc_jisx0213',
	ISO_2022_JIS = 'iso2022_jp_2004',
	ISO_2022_JP = 'iso2022_jp_2004',
	ISO2022_JP  = 'iso2022_jp_2004',
	ISO2022_JIS = 'iso2022_jp_2004',
	ISO_2022JP  = 'iso2022_jp_2004',
	ISO_2022JIS = 'iso2022_jp_2004',
	ISO2022JP   = 'iso2022_jp_2004',
	ISO2022JIS  = 'iso2022_jp_2004',
	JIS         = 'iso2022_jp_2004',
	UTF8     = 'utf_8',
	UTF_8    = 'utf_8',
)

def getJPEncodingName(enc):
	""" 指定したエンコード名がショートカットに登録されている場合、pythonのエンコード名に変換して返す

	>>> getJPEncodingName('ISO2022_JP')
	'iso2022_jp_2004'
	>>> getJPEncodingName('iso2022_jp_2004')
	'iso2022_jp_2004'
	>>> getJPEncodingName('test')
	'test'
	"""
	e = enc.replace('-','_').upper()
	if e in __Jp_Encode_ShortCut_Map__:
		return __Jp_Encode_ShortCut_Map__[e]
	return enc

def get_jp_encoding_name (msg,char_code = 'utf_8'):
	""" 文字列の文字コードを取得
	EUC-JPの文字列がうまく扱えない不具合あり

	>>> get_jp_encoding_name('あいうえお')
	'utf_8'
	>>> get_jp_encoding_name('\x82\xd9\x82\xb0')
	'shift_jisx0213'
	"""
	check_type = [char_code,
				  'iso-2022-jp',	  'iso2022_jp_1', 'iso2022_jp_2',
				  'iso2022_jp_2004',  'iso2022_jp_3', 'iso2022_jp_ext',
				  'cp932',			  'shift-jis',	  'shift_jis_2004',
				  'shift_jisx0213',   'euc_jp',		  'euc_jis_2004',
				  'euc_jisx0213',
				  'utf_8']
	for enc in check_type:
		try:
			if isinstance(msg, (str,unicode)):
				s = msg.decode(enc).encode('utf_8')
			else:
				s = unicode(msg,enc).encode('utf_8')
		except Exception, e:
			continue
		
		# when cp932 are bery old. change for shift_jisx0213
		if enc == 'cp932':
			return 'shift_jisx0213'
		logging.debug("unilib:get_jp_encoding_name(): Encoding name: %s", enc)
		return enc

	logging.debug("unilib:get_jp_encoding_name(): unknown encoding messages.")
	return ""

# 指定した文字列をデコードした状態で返す
def decode_string(msg):
	""" 指定した文字列をデコードした状態で返す

	>>> decode_string(u'あいうえお')
	u'\u3042\u3044\u3046\u3048\u304a'
	>>> decode_string('\x83\xa0\x83\xa2\x83\xa4\x83\xa6\x83\xa8')
	u'\u3042\u3044\u3046\u3048\u304a'
	"""
	if isinstance(msg, unicode):
		return msg

	try:
		enc = get_jp_encoding_name(msg)
		if enc != "":
			return msg.decode(get_jp_encoding_name(msg))
		return msg.decode('utf_8')
	except Exception, e:
		logging.warn("unilib:decode_string() unknown exception:%s", e)
		return msg

# 指定した文字列をUTF-8に変換させる
def encode_for_utf8 (msg):
	encname = get_jp_encoding_name(msg)
	logging.debug("unilib:encode_for_utf8(): encname: %s", encname)
	if encname == 'utf_8':
		if isinstance(msg, unicode):
			return msg.encode(encname)
		return msg
	elif encname == '':
		return msg
	return decode_string(msg).encode('utf_8')

# 指定したコードに文字列を変換させる
def _m (msg, enc):
	f = encode_for_utf8(msg)
	enc_name = getJPEncodingName(enc)
	
	try :
		return f.decode('utf8').encode(enc_name)
	except :
		try :
			return f.decode(enc_name)
		except :
			return f.encode(enc_name)
			

# Unicodeへ変換させる
def _u (msg):
	return encode_for_utf8(msg)

def _test():
	import doctest
	doctest.testmod()

if __name__ == '__main__':
	_test()

