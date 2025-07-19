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

### 1. MySQLデータベースの作成
PythonAnywhereのDashboardでMySQLデータベースを作成してください。

### 2. 環境変数の設定
PythonAnywhereのWeb appの設定ページで以下の環境変数を設定してください：

```
MYSQL_DATABASE=yourusername$bookSystem
MYSQL_USER=yourusername  
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=yourusername.mysql.pythonanywhere-services.com
DEBUG=False
```

### 3. パッケージのインストール
```bash
pip3.10 install --user -r requirements.txt
```

### 4. データベースのマイグレーション
```bash
python manage.py migrate
```

### 5. 静的ファイルの収集
```bash
python manage.py collectstatic
```

## MySQL Strict Mode警告の解決
このプロジェクトは自動的にMySQLのStrict Modeを有効にする設定が含まれているため、MySQL関連の警告は表示されなくなります。

## 参考プロジェクト
https://github.com/PikoCanFly/E-commerce-Site-with-Django-and-TailwindCSS