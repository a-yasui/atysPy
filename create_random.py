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
"""

_allow_string_ = string.lowercase + string.uppercase + string.digits

_nihongo_string_ = ""

# hankaku
#_nihongo_string_ += "".join([unichr(a) for a in range(0x2E80, 0x2EF3)]) # CJK部首補助
#_nihongo_string_ += "".join([unichr(a) for a in range(0x2F00, 0x2FD5)]) # 康煕部首
_nihongo_string_ += "".join([unichr(a) for a in range(0x3041, 0x3096)]) # 平仮名
_nihongo_string_ += "".join([unichr(a) for a in range(0x30A1, 0x30FA)]) # 片仮名
#_nihongo_string_ += "".join([unichr(a) for a in range(0x3400, 0x4DB5)]) # CJK統合漢字拡張A
#_nihongo_string_ += "".join([unichr(a) for a in range(0x4E00, 0x9FBB)]) # CJK統合漢字
#_nihongo_string_ += "".join([unichr(a) for a in range(0xF900, 0xFA2D)]) # CJK互換漢字
#_nihongo_string_ += "".join([unichr(a) for a in range(0xFA30, 0xFA6A)]) # CJK互換漢字
#_nihongo_string_ += "".join([unichr(a) for a in range(0xFF67, 0xFF9D)]) # 半角・全角形

def randstr (num, isJapanese=False):
	def _n_():
		f = _allow_string_
		if isJapanese:
			f = _nihongo_string_
		fn = random.randint(0, len(f)-1)
		return f[fn]
	fn = "".join([_n_() for i in range(0, num)])
	if isJapanese:
		fn = fn.encode("utf8")
	return fn


if __name__ == '__main__':
	fname = ""
	num = 0
	japanese = False

	gn, longarg = getopt.getopt(sys.argv[1:], "f:n:N")
	for (opt, optarg) in gn:
		if opt == '-f':
			fname = optarg
		elif opt == '-n':
			num = int(optarg)
		elif opt == '-N':
			japanese = True
		else:
			logging.error(__USAGE__ % (sys.argv[0]))
			sys.exit(0)
	
	if fname == '' or num == 0:
		logging.error(__USAGE__ % (sys.argv[0]))
		sys.exit(0)
	
	fhandle = open(fname, 'w')
	for n in range(0, num):
		fhandle.writelines(randstr(32, japanese) + "\n")
	fhandle.close()
	logging.info("save for %s" % (fname))
