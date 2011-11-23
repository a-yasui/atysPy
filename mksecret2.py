#-*- coding: utf8 -*-
# Performance check: https://docs.google.com/spreadsheet/ccc?key=0ArOp8Xgv8r8RdEw3enpNLWdkUDNReDM3bHduOUFkZEE

import random
import time

def create_secret(length):
    return "".join(["%c"%(random.randint(33,126)) for b in range(0, length)])


buff = ""
st = time.time()
for a in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]:
	in_start = time.time()
	fn = create_secret(1024 * a)
	fn = ''
	in_end   = time.time()
	buff += "1024 * %d\t%f" % (a, in_end - in_start) + "\n"
en = time.time()

print buff
#print "full time: %f sec" % (en - st)
