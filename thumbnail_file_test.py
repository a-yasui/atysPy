#!/usr/bin/env python
import os
import sys
import logging
logging.basicConfig(level = logging.INFO,
					format = '%(asctime)s %(levelname)s %(message)s')

try:
	import Image
except:
	logging.error('Please install PIL Module.')
	sys.exit(0)

def create_thumbnail (fpath, size_fix = 3):
	logging.warn('fpath: %s', fpath)

	def _create_thumb_ (_fpath, fname, filter_name):
		logging.info('file %s is create type %s', fname, filter_name)
		file_name, ext = os.path.splitext(fname)
		save_path = os.path.join(_fpath, file_name + '_' + filter_name + '.png')
		logging.info('save file path: %s', save_path)

		im = Image.open(os.path.join(_fpath, fname))
		size = (im.size[0] / size_fix, im.size[1] / size_fix)
		im.thumbnail(size, getattr(Image, filter_name, 0))
		im.save(save_path, 'PNG')
	
	full_name = os.path.basename(fpath)
	full_path = os.path.dirname(fpath)
	for flt in ['NEAREST', 'BILINEAR', 'BICUBIC', 'ANTIALIAS']:
		_create_thumb_(full_path, full_name, flt)

if __name__ == '__main__':
	import getopt

	optargs, filelist = getopt.getopt(sys.argv[1:], 's:')
	if not filelist:
		logging.warn('%s [s size fix..] files..', sys.argv[0])
		sys.exit(0)
	
	fix_size = 3
	for opt,optarg in optargs:
		if opt == '-s':
			fix_size = int(optarg)
			if fix_size <= 0:
				logging.error('The fix size over 0.')
				sys.exit(0)
		else:
			logging.warn('%s [s size fix..] files...', sys.argv[0])
			sys.exit(0)
	
	for f in filelist: create_thumbnail(os.path.abspath(f), fix_size)
	
