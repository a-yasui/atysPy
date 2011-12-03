#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import random
import string
import getopt
import logging

__USAGE__ = """%s -f savefilename -n numberOfLine

  -f: write out file name.
  -n: number of line.
  -j: Japanese Truest
  -N: Number of length. default 16

  kanji options:
  busyu: CJK 部首補助
  kouki: 康煕部首
  hira: ひらがな
  kana: カタカナ
  kanji_integraA: CJK統合漢字拡張A
  kanji_integra: CJK統合漢字
  kanji_ic: CJK互換漢字
  hanzen: 半角・全角形
"""

_allow_string_ = string.lowercase + string.uppercase + string.digits

_nihongo_string_ = ""

# hankaku
_hankaku = dict(
	busyu = "".join([unichr(a) for a in range(0x2E80, 0x2EF3)]),           # CJK部首補助
	kouki = "".join([unichr(a) for a in range(0x2F00, 0x2FD5)]),           # 康煕部首
	hira = "".join([unichr(a) for a in range(0x3041, 0x3096)]),            # ひらがな
	kana = "".join([unichr(a) for a in range(0x30A1, 0x30FA)]),            # カタカナ
	kanji_integraA = "".join([unichr(a) for a in range(0x3400, 0x4DB5)]),  # CJK統合漢字拡張A
	kanji_integra  = "".join([unichr(a) for a in range(0x4E00, 0x9FBB)]),  # CJK統合漢字
	kanji_ic       = "".join([unichr(a) for a in range(0xF900, 0xFA2D)]) +
					 "".join([unichr(a) for a in range(0xFA30, 0xFA6A)]),  # CJK互換漢字
	hanzen = "".join([unichr(a) for a in range(0xFF67, 0xFF9D)])           # 半角・全角形
)

def randstr (num, isJapanese=""):
	def _n_():
		f = _allow_string_
		if isJapanese:
			f = isJapanese
		fn = random.randint(0, len(f)-1)
		return f[fn]
	fn = "".join([_n_() for i in range(0, num)])
	if isJapanese:
		fn = fn.encode("utf8")
	return fn

def result_jap (choise_keys):
	keys = _hankaku.keys()

	if not len(choise_keys):
		return "".join([_hankaku['hira'], _hankaku['kana']])

	buff = []
	for k in choise_keys:
		if k in _hankaku:
			buff.append(_hankaku[k])
	return "".join(buff)


if __name__ == '__main__':
	fname = ""
	num = 0
	japanese = ""
	number_length = 16

	gn, longarg = getopt.getopt(sys.argv[1:], "f:n:N:j:h")
	for (opt, optarg) in gn:
		if opt == '-f':
			fname = optarg
		elif opt == '-n':
			num = int(optarg)
		elif opt == '-j':
			japanese = True
		elif opt == '-N':
			number_length = long(optarg)
		else:
			logging.error(__USAGE__ % (sys.argv[0]))
			sys.exit(0)
	
	if fname == '' or num == 0:
		logging.error(__USAGE__ % (sys.argv[0]))
		sys.exit(0)
	
	japanese = result_jap(longarg)
	fhandle = open(fname, 'w')
	for n in range(0, num):
		fhandle.writelines(randstr(number_length, japanese) + "\n")
	fhandle.close()
	logging.info("save for %s" % (fname))

