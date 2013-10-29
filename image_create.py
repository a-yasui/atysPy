#!/usr/bin/env python

import PIL
import PIL.Image
from PIL import ImageFile

ImageFile.MAXBLOCK = 2**20

def create (w, h, filename, dpi=74):
	r"""
	:param: w Width at mm
	:param: h Height at mm
	:param: filename Save file name
	:param: dpi Dot per inch. default: 74
	"""

	# w:mm => w:pixel
	mmToPixel = lambda x: int(float(x)* float(dpi) / 25.4)
	w = mmToPixel(w)
	h = mmToPixel(h)

	print "creating.. [{1}, {2}] / {3} for {0}".format(filename, w, h, dpi)
	im = PIL.Image.new("CMYK", (w, h))
	print "Save.. [{1}, {2}] / {3} for {0}".format(filename, w, h, dpi)
	im.save(filename, "JPEG", dpi=(dpi,dpi), quality=10, optimize=True, progressive=True, unit=1)
	print "done [{1}, {2}] / {3} for {0}".format(filename, w, h, dpi)

if __name__ == '__main__':
	import sys

	arg = sys.argv[1:]
	if len(arg) != 4:
		print "{0} width(mm) height(mm) dpi file".format(sys.argv[0])
		sys.exit(0)
	
	create(int(arg[0]), int(arg[1]), arg[3], int(arg[2]))

