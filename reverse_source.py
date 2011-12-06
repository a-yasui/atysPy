#!/usr/bin/env python
# -*- coding: UTF_8 -*-

import sys
import os

def in_line_show (words, ptr=0, nest = 1):
	nest_word = "".join([' ' for i in range(0, nest * 4)])
	buff      = nest_word

	while ptr <= len(words):
		if not 0 <= ptr < len(words):
			return (buff, ptr)
		word = words[ptr]
		ptr += 1

		if word == ';':
			buff += ";\n" + nest_word
		elif word == '\n':
			buff += "\n"
		elif word == '{':
			buff += "\n" + nest_word + "{\n"
			_buff, ptr = in_line_show(words, ptr, nest + 1)
			buff += _buff + nest_word
		elif word == '}':
			nest_word = "".join([' ' for i in range(0, (nest - 1) * 4)])
			buff += "\n" + nest_word + "}\n"
			return (buff, ptr)
		else:
			buff += word
	# end while
	return (buff, ptr)

if __name__ == '__main__':
	file = sys.argv[1]
	buff = open(file, 'r').read()
	
	buff, ptr = in_line_show(buff)
	
	fp = open(file, 'w')
	fp.write(buff)
	fp.close()
