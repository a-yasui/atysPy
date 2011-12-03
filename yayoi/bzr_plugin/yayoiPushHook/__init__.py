#
# A.yasui push hook test.
#
import logging
from bzrlib import branch
logging.basicConfig(format='%(asctime)s %(module)s[%(lineno)d] [%(levelname)s]: %(message)s',
					filename = '/var/tmp/branch.txt',
					level = logging.WARN)
 
def print_branch(param):
	import os
	logging.info('push request: param: %s', param) #.get_config()
	configs = param.branch.get_config()
	
	build_dir = configs.get_user_option('update_url')
	if not build_dir:
		logging.info('not set update_url')
		return
	
	import urllib
	urllib.urlopen(build_dir)
	

branch.Branch.hooks.install_named_hook('post_change_branch_tip', print_branch, 'print branch')

