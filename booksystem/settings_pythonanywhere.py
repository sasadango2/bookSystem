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
STATIC_ROOT = '/home/sta/bookSystem/staticfiles'
MEDIA_ROOT = '/home/sta/bookSystem/mediafiles'
