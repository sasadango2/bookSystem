# 図書館管理システム (Book Management System)

## プロジェクト概要
Djangoを使用した図書館の本貸し出し管理システムです。学校や企業の図書館での利用を想定した、Web ベースの図書管理アプリケーションです。

## 主な機能

### 📚 書籍管理
- 書籍の登録・編集・削除
- カテゴリ別の書籍分類
- ISBN、著者、出版社などの詳細情報管理
- 書籍画像のアップロード
- 在庫数・利用可能数の管理
- 書籍検索機能（タイトル、著者、ISBN、説明文）

### 👥 会員管理
- ユーザー登録・ログイン機能
- 会員プロファイル（学生・管理者区分）
- 貸出上限・貸出期間の設定
- 会員IDの自動生成

### 📖 貸出・返却管理
- 書籍の貸出処理
- 返却処理
- 貸出履歴の管理
- 延滞管理・統計表示
- 返却期限リマインダー

### 🔖 予約機能
- 貸出中書籍の予約
- 予約一覧表示
- 利用可能時の通知機能

### 📊 統計・レポート機能
- 会員別貸出統計
- 貸出中書籍数
- 延滞中書籍数
- 今週返却期限の書籍数

### 🛠 管理機能
- Django管理画面のカスタマイズ
- 書籍・会員の一括管理
- サンプルデータ作成コマンド

## 技術スタック

- **フレームワーク**: Django 5.1.4
- **データベース**: SQLite3 (開発) / MySQL (本番)
- **フロントエンド**: HTML, CSS (Tailwind CSS), JavaScript
- **画像処理**: Pillow
- **デプロイ**: PythonAnywhere

## ファイル構成

```
bookSystem/
├── books/              # 書籍管理アプリ
├── loans/              # 貸出・予約管理アプリ  
├── members/            # 会員管理アプリ
├── templates/          # HTMLテンプレート
├── static/             # 静的ファイル
├── mediafiles/         # アップロード画像
├── booksystem/         # プロジェクト設定
├── manage.py           # Django管理コマンド
├── requirements.txt    # パッケージ依存関係
└── db.sqlite3          # SQLiteデータベース
```

## データモデル

### 📚 Book (書籍)
- カテゴリ、タイトル、著者、ISBN
- 出版日、出版社、説明文
- 総冊数、利用可能冊数
- 書籍画像

### 👤 MemberProfile (会員プロファイル)
- ユーザー情報、会員ID、会員種別
- 貸出上限数、貸出期間
- アクティブ状態、参加日

### 📋 Loan (貸出記録)
- 貸出日、返却期限、返却日
- 貸出状態（貸出中/返却済み/延滞中）
- 延滞判定機能

### 🔖 Reservation (予約)
- 予約日、アクティブ状態
- 通知フラグ

## ローカル開発環境セットアップ

### 1. リポジトリのクローン
```bash
git clone https://github.com/sasadango2/bookSystem.git
cd bookSystem
```

### 2. 仮想環境の作成・有効化 (推奨)
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate     # Windows
```

### 3. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 4. データベースのマイグレーション
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 管理者アカウントの作成
```bash
python manage.py createsuperuser
```

### 6. サンプルデータの作成 (オプション)
```bash
python manage.py create_sample_data
```

### 7. 開発サーバーの起動
```bash
python manage.py runserver
```

### 8. アクセス
- アプリケーション: http://127.0.0.1:8000/
- 管理画面: http://127.0.0.1:8000/admin/

## 使用方法

### 管理者の操作
1. 管理画面から書籍とカテゴリを登録
2. 必要に応じて会員の管理

### 一般ユーザーの操作
1. アカウント登録・ログイン
2. 書籍の検索・閲覧
3. 書籍の貸出・返却
4. 利用履歴の確認
5. 貸出中書籍の予約

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

#### 5. PythonAnywhereの静的ファイル設定

PythonAnywhereのWeb appの設定ページで以下を設定：

**Static files:**
```
URL: /static/
Directory: /home/sta/bookSystem/staticfiles
```

**Media files:**
```
URL: /media/
Directory: /home/sta/bookSystem/mediafiles
```

#### 6. WSGIファイルの設定（オプション - 静的ファイルが表示されない場合）

PythonAnywhereのWSGI設定ファイルを以下のように設定：

```python
import os
import sys
from django.core.wsgi import get_wsgi_application

# プロジェクトディレクトリをパスに追加
path = '/home/sta/bookSystem'
if path not in sys.path:
    sys.path.append(path)

# Django設定モジュールを指定
os.environ['DJANGO_SETTINGS_MODULE'] = 'booksystem.settings_pythonanywhere'

# WSGIアプリケーション
application = get_wsgi_application()
```

## MySQL Strict Mode警告の解決
このプロジェクトは自動的にMySQLのStrict Modeを有効にする設定が含まれているため、MySQL関連の警告は表示されなくなります。

## トラブルシューティング

### 静的ファイルが表示されない場合
```bash
python manage.py collectstatic
```

### データベースリセット
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
python manage.py create_sample_data
```

### MySQLデータベース接続エラー
`settings_pythonanywhere.py`のデータベース設定を確認してください。

## 開発者向け情報

### カスタム管理コマンド
- `create_sample_data`: サンプルデータの作成

### 主要なURL構成
- `/` : ホームページ（書籍一覧）
- `/books/` : 書籍管理
- `/loans/` : 貸出管理
- `/members/` : 会員管理
- `/admin/` : Django管理画面

### 今後の拡張可能性
- 電子書籍対応
- 図書館間貸借機能
- 推薦システム
- API提供
- モバイルアプリ対応

## ライセンス
このプロジェクトはMITライセンスの下で公開されています。

## 参考プロジェクト
https://github.com/PikoCanFly/E-commerce-Site-with-Django-and-TailwindCSS

## 作成者
- GitHub: [sasadango2](https://github.com/sasadango2)
- リポジトリ: [bookSystem](https://github.com/sasadango2/bookSystem)