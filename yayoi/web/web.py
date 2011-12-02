#!/usr/bin/env python2.6
# -*- coding: utf8 -*-
#### sphinx part. same as build.py

import sphinx
from sphinx.websupport import WebSupport
from sphinx.websupport.errors import DocumentNotFoundError
import serveconf
import logging
import os,sys

support = WebSupport(serveconf.SRCDIR, serveconf.BUILDDIR)

#### flask part 

from flask import Flask, render_template, abort, g, request, jsonify, redirect, url_for
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)
app.debug = True # デバッグ用フラグ
app.jinja_env = Environment(loader = FileSystemLoader(os.path.abspath(serveconf.TEMPLATE_DIR)+'/'),
                            extensions=['jinja2.ext.i18n'])
app.root_path = serveconf.BUILDDIR


# Via bzrlib.tests
class StringIOWrapper(object):
	"""A wrapper around cStringIO which just adds an encoding attribute.

	Internally we can check sys.stdout to see what the output encoding
	should be. However, cStringIO has no encoding attribute that we can
	set. So we wrap it instead.
	"""
	encoding='ascii'
	_cstring = None
	def __init__(self, s=None):
		from cStringIO import StringIO
		if s is not None:
			self.__dict__['_cstring'] = StringIO(s)
		else:
			self.__dict__['_cstring'] = StringIO()

	def __getattr__(self, name, getattr=getattr):
		return getattr(self.__dict__['_cstring'], name)
	def __setattr__(self, name, val):
		if name == 'encoding':
			self.__dict__['encoding'] = val
		else:
			return setattr(self._cstring, name, val)


@app.route('/static/<path:docname>')
def staticdir (docname):
	logging.warn('access: %s', docname)
	staticfile = os.path.abspath(os.path.join(serveconf.BUILDDIR, docname))
	if os.path.exists(staticfile):
		return open(staticfile, 'r').read()
	abort(404)

@app.route('/_update')
def update_checj ():
	try:
		import bzrlib.builtins
		pull_req = bzrlib.builtins.cmd_pull()
		pull_req.outf = StringIOWrapper()
		pull_req.run(directory=serveconf.SRCDIR, overwrite=True)
		support.build()
	except Exception, e:
		logging.error('update exception: %s', e)

	return redirect(url_for('index'))

@app.route('/<path:docname>')
@app.route('/<path:docname>/')
@app.route('/')
def index(docname='index'):
	try:
		document = support.get_document(docname)
	except DocumentNotFoundError:
		abort(404)
	return render_template('doc.html', document=document)

application = app
if __name__ == "__main__":
	app.run()
