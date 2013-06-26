#!/usr/bin/env python2.6

import getopt 
import smtplib
import sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

def mail (subject, me, you ,text, html):
	msg = MIMEMultipart('alternative')
	msg['Subject'] = Header(subject.decode("utf-8").encode("iso-2022-jp"), "ISO-2022-JP")
	msg['From'] = me
	msg['To'] = you

	# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(text, 'plain', 'ISO-2022-JP')
	part2 = MIMEText(html, 'html', "utf-8")
	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach(part1)
	msg.attach(part2)
	# Send the message via local SMTP server.
	s = smtplib.SMTP('localhost')
	# sendmail function takes 3 arguments: sender's address, recipient's address
	# and message to send - here it is sent as one string.
	s.sendmail(me, you, msg.as_string())
	s.quit()


if __name__ == "__main__":
	optlist, optarg = getopt.getopt(sys.argv[1:], "s:t:f:H:F:h")
	USAGE = r"""%(command)s [-s subject] [-t tolist] [-f from] [-H htmlfile] [-F textfile]
	sending email.

Options
	-s : Subject. 日本語の場合、ISO-2022-JP に変換して投げる
	-t : Mail list
	-f : From address. ex: -f "FromAddr <test@example.com>"
	-H : HTML File. Must using UTF-8.
	-F : Plain Text File. Must using ISO-2022-JP
	
""" % (dict(command = sys.argv[0]))
	
	toaddrlist = subject = fromaddr = htmlfile = textfile = ""
	for opt, optarg in optlist:
		if   opt == '-h': print USAGE; sys.exit(0)
		elif opt == '-s': subject = optarg;
		elif opt == '-t': toaddrlist = open(optarg, "r").read()
		elif opt == '-f': fromaddr = optarg
		elif opt == '-H': htmlfile = open(optarg, "r").read()
		elif opt == '-F': textfile = open(optarg, "r").read() 

	import re
	for toaddr in re.split(r"[\r\n]+", toaddrlist):
		if toaddr:
			print "From: ", fromaddr, " to ", toaddr,"\n"
			mail (subject, fromaddr, toaddr ,textfile, htmlfile)
	print "finish"
