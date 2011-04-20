#!/usr/bin/env python
import sys
try:
	import yaml
except Exception, e:
	print "%s" % e

for f in sys.argv[1:]:
	fn = yaml.load_all(open(f))
	for k in fn:
		print k
