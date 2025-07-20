# PythonAnywhere用のWSGI設定サンプル
# このファイルをPythonAnywhereのWSGI設定の参考にしてください

import os
import sys
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from django.contrib.staticfiles.handlers import StaticFilesHandler

# プロジェクトディレクトリをパスに追加
path = '/home/sta/bookSystem'
if path not in sys.path:
    sys.path.append(path)

# Django設定モジュールを指定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booksystem.settings_pythonanywhere')

# 本番環境でも静的ファイルを配信するためのWSGIアプリケーション
class PythonAnywhereStaticFilesHandler(StaticFilesHandler):
    """
    PythonAnywhere用の静的ファイルハンドラー
    本番環境でもDjangoが静的ファイルを配信できるようにする
    """
    def __init__(self, application):
        self.application = application
        super().__init__(application)

# WSGIアプリケーションを作成
application = get_wsgi_application()

# 静的ファイル配信を有効にする
if not settings.DEBUG:
    application = PythonAnywhereStaticFilesHandler(application)
