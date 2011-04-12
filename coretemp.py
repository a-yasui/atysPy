#!/usr/local/bin/python2.5
# -*- encoding: utf-8 -*-
#
# Parameters supported:
# 
# config
# autoconf
#
# Magic makers:
#%# family=auto
#%# capabilities=autoconf

import commands,os,sys,re

_GRAPH = [('title',    'CPU Temperator'),
	  ('args',     '--base 1000'),
	  ('vlabel',   'access / ${graph_period}'),
	  ('category', 'system')
]

os.environ['PATH'] = ''
sysctl="/sbin/sysctl -a | /usr/bin/grep tempe"

# Check
_temps = commands.getoutput(sysctl)
if _temps == "":
    raise "Please load to coretemp kernel module and the over FreeBSD 7.x/8.x version."
temps = [f.split(":") for f in [e for e in _temps.split("\n")]]

# show config
if len(sys.argv)>1 and sys.argv[1] == 'config':
    for g in _GRAPH:
        print "graph_%s %s" % g

    for fn in temps:
        (dev,cpu,number,temperature) = fn[0].split(".")
        print "cputemperature%s.label Num %s" % (number,number)
        print "cputemperature%s.type GAUGE" % (number)
        print "cputemperature%s.max  100" % (number)
        print "cputemperature%s.min -100" % (number)
    sys.exit(0)
elif len(sys.argv) > 1 and sys.argv[1] == 'autoconf':
    print 'yes'
    sys.exit(0)

for fn in temps:
	(dev,cpu,number,temperature) = fn[0].split(".")
	reg = re.compile(r'\s*(-?[0-9\.]+)C?\s*')
	if reg.match(fn[1]):
		temperature = reg.match(fn[1]).group(1)
	else:
		temperature = fn[1]
	print "cputemperature%s.value %s" % (number, temperature)

