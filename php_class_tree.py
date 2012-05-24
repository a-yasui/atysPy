#!/usr/bin/env pypy
# -*- coding: UTF8 -*-

import sys
import os
import os.path
import getopt
import re
import doctest

USAGE = r"""%s [t] [h] [p path]

Create the class relational list for dot format.

Options:

   -t: Test Mode
   -h: Show This.
   -p Path: Php Base file path.
"""


# 再帰的にディレクトリを見て、php ファイルリスト作成
def create_php_file_list (path):
    
    buff = []
    for root, dirs, files in os.walk(path):
#        print "root: %s dirs:%s files:%s" % (root, dirs,files)
        for fname in files:
            if re.match(r".+\.php$", fname):
                buff.append("%s/%s" % (root, fname))
    return buff

# クラス宣言にマッチするか確認
def is_match_kls (line):
    r"""
    
        :result: ('class', klsname, ext_kls_name, implements)
    
    >>> fn = is_match_kls("class test")
    >>> fn.group(2)
    'test'
    >>> fn = is_match_kls("interface test")
    >>> fn.group(2)
    'test'
    >>> fn = is_match_kls("interface test implements testA")
    >>> fn.groupdict()['implements']
    'testA'
    >>> fn = is_match_kls("class test extends testParent implements testA")
    >>> fn.groupdict()['implements']
    'testA'
    >>> fn.groupdict()['extends']
    'testParent'
    """
    
    regexes = [
        r'^\s*((?:class)|(?:interface))\s+(?P<name>[a-zA-Z0-9_]+)\s+(?:extends)?\s*(?P<extends>[a-zA-Z0-9_]*)\s*(?:implements)?\s*(?P<implements>[a-zA-Z0-9_, ]*){?$',
        r'^\s*((?:class)|(?:interface))\s+(?P<name>[a-zA-Z0-9_]+)\s+(?:implements)?\s*(?P<implements>[a-zA-Z0-9_, ]*){?$',
        r'^\s*((?:class)|(?:interface))\s+(?P<name>[a-zA-Z0-9_]+)\s+(?:extends)?\s*(?P<extends>[a-zA-Z0-9_]*){?$',
        r'^\s*((?:class)|(?:interface))\s+(?P<name>[a-zA-Z0-9_]+){?$'
    ]
    
    for regex in regexes:
        kls_line = re.compile(regex)
        fn = kls_line.match(line)
        if fn: return fn
    return None

# クラスを取り出して、一覧にして返す
def get_class_from_path (path):
    r"""
        
        :result: list[dict(kls = kls_name, extends = kls_name, path = filepath, type = class|interface )]
        
        >>> get_class_from_path ("/Users/yasui/sup/ripo/sup3/trunk/apps/api/lib/myUser.class.php")
        [{'implements': [''], 'extends': 'sfBasicSecurityUser', 'path': '/Users/yasui/sup/ripo/sup3/trunk/apps/api/lib/myUser.class.php', 'type': 'class', 'kls': 'myUser'}]
        >>> get_class_from_path ("/Users/yasui/sup/ripo/sup3/trunk/lib/vendor/symfony/lib/plugins/sfPropelPlugin/lib/vendor/phing/tasks/system/condition/OrCondition.php")
        [{'implements': ['Condition'], 'extends': 'ConditionBase', 'path': '/Users/yasui/sup/ripo/sup3/trunk/lib/vendor/symfony/lib/plugins/sfPropelPlugin/lib/vendor/phing/tasks/system/condition/OrCondition.php', 'type': 'class', 'kls': 'OrCondition'}]
        >>> get_class_from_path ("/Users/yasui/sup/ripo/sup3/trunk/lib/vendor/symfony/lib/form/sfFormFieldSchema.class.php")
        [{'implements': ['ArrayAccess', 'Iterator', 'Countable'], 'extends': 'sfFormField', 'path': '/Users/yasui/sup/ripo/sup3/trunk/lib/vendor/symfony/lib/form/sfFormFieldSchema.class.php', 'type': 'class', 'kls': 'sfFormFieldSchema'}]
        
    """
    
    buff = []
    with open (path) as fp:
        for line in fp.readlines():
            kn = is_match_kls(line)
            if kn:
                #print kn.groups()
                buf = dict()
                buf['type'] = kn.group(1)
                
                m = kn.groupdict()
                buf['kls'] = m['name']
                buf['extends'] = m['extends'] if 'extends' in m else ""
                if 'implements' in m:
                    buf['implements'] = [f.rstrip() for f in re.split(r',\s*', m['implements'])]
                buf['path'] = path
                buff.append(buf)
    return buff

def dot_create (dic):
    r"""
        
        :result: (label 配列, 継承矢印, interface実装矢印)
    """
    result = ([],[],[])
    
    if not isinstance(dic, dict):
        return result
    
    style = "solid"
    obj_name = dic['kls']
    if dic['type'] == 'interface':
        style = "dotted"
    result[0].append("  %s [label=\"%s:%s\", style=%s];" % (obj_name, obj_name, dic['path'], style))
    
    if 'extends' in dic:
        result[1].append("%s -> %s;" % (obj_name, dic['extends']))
    if 'implements' in dic:
        for implement in dic['implements']:
            result[2].append("%s -> %s [style=dotted];" % (obj_name, implement))
    return result

def main (path):
    buff = []
    buff = [b for b in [get_class_from_path(pa) for pa in create_php_file_list(path)] if len(b)]
    
    # class     => 実線
    # interface => 破線
    # extends   => 実線
    # implements => 破線
    print "digraph %s {\n" % (path)
    
    ext_marks = []
    for obj in buff:
        for k in obj:
            line, a, b = dot_create(k)
        
        if len(a):
            ext_marks += a
        if len(b):
            ext_marks += b
        
        print "\n".join(line)
    print "%s" % ("\n".join(ext_marks))
    print "}"
#    print "out: %s" %(buff)

if __name__ == '__main__':
    path = os.curdir
    testflg = False
    
    gn, longarg = getopt.getopt(sys.argv[1:], "thp:")
    for (opt, optarg) in gn:
        if opt == '-t':
            testflg = True
        elif opt == '-h':
            print USAGE
            sys.exit(0)
        elif opt == '-p' and os.path.exists(optarg):
            path = optarg
    
    if testflg:
        doctest.testmod()
    else:
        main(path)
    
