
Yayoi Plugin
================

bzr のサーバに pull リクエストを送信した時、Sphinxで書かれたドキュメントを自動更新をする。

Apache HTTP Server(2.2.3) + mod_wsgi 3.3.1 + Flask 0.8 + Bazaar 2.5 + Sphinx 1.1

Apache HTTP Server: http://httpd.apache.org/
Bazaar: http://bazaar.canonical.com/en/
Flask: http://flask.pocoo.org/
mod_wsgi: http://code.google.com/p/modwsgi/
Sphinx: http://sphinx.pocoo.org/

Abstract
---------

Bazaar で sphinx のドキュメントを管理し、メインサーバに pull リクエストを送った時に、Sphinxのドキュメントを自動的にビルドする仕組み。


pull リクエストが有った場合、pullされたブランチに設定されている「update_url」のURLにアクセスします。そこでsphinxを走らせてビルドを行います。


Configuration
--------------

1. Apache HTTP Server で Flask が動く状態にしてください。ここには面倒なので書きません
2. WSGIScriptAlias を web.py になるように、設定して下さい
3. Bazaar のプラグインディレクトリ(ex: /usr/lib/python2.6/site-packages/bzrlib/plugins) に、bzr_plugin にある yayoiPushHook を設置して下さい
4. pull されるブランチにある、 .bzr/branch/bazaar.conf に update_url='http://<your host>/_update' を追加して下さい。<your host> は任意変更。
5. web/serveconf.py を設定して下さい。
   
   :SRCDIR: ブランチディレクトリ。Pullされるブランチとは別に、このスクリプト専用にブランチを分けます。
   
   :BUILDDIR: Sphinx が使用するbuildディレクトリ
   
   :TEMPLATE_DIR: webブラウザ上で表示させるテンプレートのディレクトリ。


6. SRCDIR にブランチディレクトリをあらかじめ設置して下さい
7. たぶん、これで動く。よくわからん。

