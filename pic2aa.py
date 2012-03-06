#!/usr/bin/env python
import PIL
from PIL import Image
import os

# 0 => 128
GRAY_MAP = [
	" ",".",":","|","/","(","%","Y","V","O","8","D","@","0","#","$"
]

def change_and_save (src, dst):
	global GRAY_MAP
	im = Image.open(src).convert('L')
	
	print "w %f h %f" % im.size
	w = 60
	h = im.size[1] * 60 / im.size[0]
	im = im.resize((w,h))
	print "w %f h %f" % im.size
	fp = open(dst, 'w')

	for y in range(0, im.size[1]):
		for x in range(0, im.size[0]):
			fn = im.getpixel((x,y))/len(GRAY_MAP)
			fp.write(GRAY_MAP[int(fn)])
		fp.write("\n")
	fp.close()

def main ():
	import sys
	import logging

	if len(sys.argv) != 3:
		logging.error("Error: %s <input file> <out file>", sys.argv[0])
		sys.exit(0)
	
	input  = os.path.abspath(sys.argv[1])
	output = os.path.abspath(sys.argv[2])
	change_and_save(input, output)

if __name__ == '__main__':
	main()

