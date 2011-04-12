# -*- coding: utf-8 -*-

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

# 指定したエンコード名がショートカットに登録されている場合、
# python上のエンコード名を返す。
def getJPEncodingName(enc):
	e = enc.replace('-','_').upper()
	if e in __Jp_Encode_ShortCut_Map__:
		return __Jp_Encode_ShortCut_Map__[e]
	return enc

# 文字列のコードを取得
def get_jp_encoding_name (msg,char_code = 'utf_8'):
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
				s = msg.decode(enc)
			else:
				s = unicode(msg,enc)
		except :
			continue
		
		# when cp932 are bery old. change for shift_jisx0213
		if enc == 'cp932':
			return 'shift_jisx0213'
		return enc
	return None

# 指定した文字列をデコードした状態で返す
def decode_string(msg):
	try:
		return msg.decode(get_jp_encoding_name(msg))
	except :
		return msg

# 指定した文字列をUTF-8に変換させる
def encode_for_utf8 (msg):
	try :
		return msg.decode(get_jp_encoding_name(msg)).encode('utf_8')
	except :
		return msg.encode('utf_8')

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
