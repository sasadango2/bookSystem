# PythonAnywhere専用のMySQL設定
# このファイルをPythonAnywhereでのみ使用してください

import os
from .settings import *

# PythonAnywhere MySQL設定を強制適用
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sta$default',
        'USER': 'sta',
        'PASSWORD': 'happy2025',
        'HOST': 'sta.mysql.pythonanywhere-services.com',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION',
            'charset': 'utf8mb4',
            'use_unicode': True,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'",
        },
    }
}

# 本番環境設定
DEBUG = False
ALLOWED_HOSTS = ['sta.pythonanywhere.com', 'www.sta.pythonanywhere.com']

# 静的ファイル設定
STATIC_URL = '/static/'
STATIC_ROOT = '/home/sta/bookSystem/staticfiles'

# メディアファイル設定
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/sta/bookSystem/mediafiles'

# 静的ファイルディレクトリを上書き（本番環境では空にする）
STATICFILES_DIRS = []

# 静的ファイルファインダー
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# 本番環境用の追加設定
USE_TZ = True
USE_I18N = True

# セキュリティ設定
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# ログイン・ログアウト後のリダイレクト設定
LOGIN_REDIRECT_URL = '/'  # ログイン後はホームページ（書籍一覧）へ
LOGOUT_REDIRECT_URL = '/'  # ログアウト後もホームページへ
LOGIN_URL = '/accounts/login/'  # ログインが必要な場合のリダイレクト先
