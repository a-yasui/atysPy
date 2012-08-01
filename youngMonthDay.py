#!/usr/bin/env pypy
# -*- coding: utf_8 -*-

import datetime

def getYoungMonthWeekDay (start, end):
	weekday = [k for k in u'月火水木金土日']
	result = {}
	for year in range(start, end):
		result[year] = {}
		for month in range(1,12):
			k = datetime.date(year, month, 1)
			result[year][month] = weekday[k.weekday()]
	return result

if __name__ == '__main__':
	import sys
	
	_USAGE = u""" %s <start year> <end year>

	Get weekday for start year to end year.
"""

	if len(sys.argv) != 3:
		print _USAGE % sys.argv[0]
	
	st = int(sys.argv[1])
	en = int(sys.argv[2])

	result = getYoungMonthWeekDay(st, en)
	
	sums = dict(zip([k for k in u"月火水木金土日"], [0 for i in range(12)]))

	for year in result:
		print "%12s" % year
		print "  %s " % (" ".join(["%s: %s" % (month, result[year][month]) for month in result[year]]))
		print "\n"
		for month in result[year]:
			sums[result[year][month]] += 1
	print "\n"
	print "sum (weekday(%d ~ %d)) => %s" % (st, en, " ".join(["%s:%d" % (month, sums[month]) for month in sums]))


