#!/usr/bin/env python
# -*- coding: utf-8 -*-


def expandString (fn):
	""" http://d.hatena.ne.jp/gnarl/20100921/1285065333

	>>> expandString('hoge')
	'hoge'
	>>> expandString('リンク http://example.com/')
	'リンク <a href="http://example.com/">http://example.com/</a>'
	>>> expandString('目立つ色があるのではなく、他と違う色が目立つ #huroushotoku')
	'目立つ色があるのではなく、他と違う色が目立つ <a href="http://twitter.com/#search?q=%23huroushotoku">#huroushotoku</a>'

	"""



if __name__ == '__main__':
	import doctest
	doctest.testmod()
