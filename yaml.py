#!/usr/bin/env python
import yaml
import sys


for f in sys.argv[1:]:
	print f
	fn = yaml.load_all(open(f))
	print fn
