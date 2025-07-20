# 本貸し出しシステムの作成

## プロジェクト概要
Djangoを使用した図書館の本貸し出し管理システムです。

## 機能
- 書籍管理
- 会員管理  
- 貸出・返却管理
- 予約機能

## ローカル開発環境セットアップ

### 1. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 2. データベースのマイグレーション
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. 開発サーバーの起動
```bash
python manage.py runserver
```

## PythonAnywhereでのデプロイ

### 方法1: 環境変数を使用する方法

#### 1. MySQLデータベースの作成
PythonAnywhereのDashboardでMySQLデータベースを作成してください。

#### 2. 環境変数の設定
PythonAnywhereのWeb appの設定ページで以下の環境変数を設定してください：

```
MYSQL_DATABASE=sta$default
MYSQL_USER=sta  
MYSQL_PASSWORD=happy2025
MYSQL_HOST=sta.mysql.pythonanywhere-services.com
DEBUG=False
```

#### 3. パッケージのインストール
```bash
pip3.10 install --user -r requirements.txt
```

#### 4. データベースのマイグレーション
```bash
python manage.py migrate
```

### 方法2: 専用設定ファイルを使用する方法（推奨）

#### 1. WSGI設定の変更
PythonAnywhereのWSGI設定ファイルで以下のように変更：

```python
import os
import sys

# プロジェクトディレクトリをパスに追加
path = '/home/sta/bookSystem'
if path not in sys.path:
    sys.path.append(path)

# Django設定モジュールを指定（PythonAnywhere専用設定を使用）
os.environ['DJANGO_SETTINGS_MODULE'] = 'booksystem.settings_pythonanywhere'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

#### 2. パッケージのインストール
```bash
pip3.10 install --user -r requirements.txt
```

#### 3. データベースのマイグレーション
```bash
cd /home/sta/bookSystem
python manage.py migrate --settings=booksystem.settings_pythonanywhere
```

#### 4. 静的ファイルの収集
```bash
python manage.py collectstatic --settings=booksystem.settings_pythonanywhere
```

## MySQL Strict Mode警告の解決
このプロジェクトは自動的にMySQLのStrict Modeを有効にする設定が含まれているため、MySQL関連の警告は表示されなくなります。

## 参考プロジェクト
https://github.com/PikoCanFly/E-commerce-Site-with-Django-and-TailwindCSS