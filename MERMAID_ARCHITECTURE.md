# 図書館管理システム - システム構成図

## システム全体アーキテクチャ

## システム全体アーキテクチャ

### 4層アーキテクチャ構成
図書館管理システムは、明確に分離された**4層アーキテクチャ**で構築されています。

```mermaid
graph TB
    subgraph "🌐 クライアント層"
        User[👤 ユーザー<br/>書籍検索・貸出・返却]
        Admin[👨‍💼 管理者<br/>システム・書籍管理]
        Browser[🌐 Webブラウザ<br/>レスポンシブ対応]
    end

    subgraph "🎨 プレゼンテーション層"
        Web[🌐 Django Web Server<br/>リクエスト処理・レスポンス生成]
        Templates[📄 HTMLテンプレート<br/>Tailwind CSS・動的コンテンツ]
        Static[🎨 静的ファイル<br/>CSS・JavaScript・画像]
    end

    subgraph "⚙️ アプリケーション層"
        Books[📚 Books App<br/>書籍CRUD・検索・在庫管理]
        Loans[📖 Loans App<br/>貸出・返却・予約・履歴] 
        Members[👥 Members App<br/>会員管理・通知]
        Auth[🔐 Django Auth<br/>認証・認可・セッション]
    end

    subgraph "💾 データ層"
        SQLite[(📊 SQLite<br/>開発環境)]
        MySQL[(🗄️ MySQL<br/>本番環境)]
        Media[🖼️ メディアファイル<br/>書籍画像]
    end

    User --> Browser
    Admin --> Browser
    Browser -->|HTTP/HTTPS| Web
    Web --> Templates
    Web --> Static
    Web --> Books
    Web --> Loans
    Web --> Members
    Web --> Auth
    Books --> SQLite
    Loans --> SQLite
    Members --> SQLite
    Auth --> SQLite
    SQLite -.->|デプロイ時| MySQL
    Web --> Media

    classDef clientLayer fill:#e1f5fe
    classDef presentationLayer fill:#f3e5f5
    classDef applicationLayer fill:#e8f5e8
    classDef dataLayer fill:#fff3e0

    class User,Admin,Browser clientLayer
    class Web,Templates,Static presentationLayer
    class Books,Loans,Members,Auth applicationLayer
    class SQLite,MySQL,Media dataLayer
```

### � 各層の概要

| 層 | 役割 | 主要技術 | 特徴 |
|---|---|---|---|
| **🌐 クライアント** | UI・操作入力 | HTML5, CSS3, JS | レスポンシブ対応 |
| **🎨 プレゼンテーション** | 画面制御・表示 | Django Templates, Tailwind | コンポーネント設計 |
| **⚙️ アプリケーション** | ビジネスロジック | Django Apps, Python | MVCパターン |
| **💾 データ** | データ永続化 | SQLite/MySQL, ORM | DB非依存設計 |

### 🔄 基本データフロー

```mermaid
sequenceDiagram
    participant U as ユーザー
    participant W as Web Server
    participant A as アプリ層
    participant D as データ層

    U->>W: HTTP リクエスト
    W->>A: ビジネスロジック実行
    A->>D: データ操作
    D-->>A: データ返却
    A-->>W: 処理結果
    W-->>U: HTML レスポンス
```

### � デプロイメント環境

```mermaid
graph LR
    Dev[� ローカル環境<br/>SQLite + Dev Server] 
    Prod[☁️ PythonAnywhere<br/>MySQL + WSGI Server]
    
    Dev -.->|git push<br/>デプロイ| Prod
```

## Django アプリケーション構成

```mermaid
graph LR
    subgraph "📚 Books App"
        BookViews[📋 Views]
        BookModels[🗂️ Models]
        BookTemplates[📄 Templates]
        BookAdmin[⚙️ Admin]
    end

    subgraph "📖 Loans App"
        LoanViews[📋 Views]
        LoanModels[🗂️ Models]
        LoanTemplates[📄 Templates]
        LoanAdmin[⚙️ Admin]
    end

    subgraph "👥 Members App"
        MemberViews[📋 Views]
        MemberModels[🗂️ Models]
        MemberTemplates[📄 Templates]
        MemberAdmin[⚙️ Admin]
    end

    BookViews --> BookModels
    BookViews --> BookTemplates
    BookModels --> BookAdmin

    LoanViews --> LoanModels
    LoanViews --> LoanTemplates
    LoanModels --> LoanAdmin

    MemberViews --> MemberModels
    MemberViews --> MemberTemplates
    MemberModels --> MemberAdmin

    LoanModels --> BookModels
    MemberModels --> LoanModels
```

## データベース関係図 (ERD)

```mermaid
erDiagram
    User ||--o{ MemberProfile : has
    User ||--o{ Loan : makes
    User ||--o{ Reservation : makes
    User ||--o{ LibraryNotification : receives

    Book ||--o{ Loan : borrowed_in
    Book ||--o{ Reservation : reserved_in
    Book }o--|| Category : belongs_to

    MemberProfile {
        string membership_type
        string member_id
        string phone
        text address
        date join_date
        boolean is_active
        int max_loans
        int loan_period_days
        text notes
    }

    Book {
        string title
        string slug
        string author
        string isbn
        text description
        date publication_date
        string publisher
        int available_copies
        int total_copies
        boolean available
        datetime created
        datetime updated
        image image
    }

    Category {
        string name
        string slug
    }

    Loan {
        datetime loan_date
        date due_date
        datetime return_date
        string status
        text notes
    }

    Reservation {
        datetime reservation_date
        boolean is_active
        boolean notified
    }

    LibraryNotification {
        string notification_type
        string title
        text message
        datetime created_at
        boolean is_read
    }
```

## URL ルーティング構成

```mermaid
graph TD
    Root[/ Root URL] --> BooksApp[📚 Books App]
    Root --> LoansApp[📖 Loans App /loans/]
    Root --> MembersApp[👥 Members App /members/]
    Root --> AdminApp[⚙️ Admin /admin/]
    Root --> AuthApp[🔐 Auth /accounts/]

    BooksApp --> BookList[📋 書籍一覧 /]
    BooksApp --> BookCategory[📂 カテゴリ別 /<slug>/]
    BooksApp --> BookDetail[📖 書籍詳細 /book/<id>/<slug>/]
    BooksApp --> BookSearch[🔍 検索 /search/]

    LoansApp --> LoanList[📋 貸出中 /]
    LoansApp --> BorrowBook[📚 貸出 /borrow/<id>/]
    LoansApp --> ReturnBook[🔄 返却 /return/<id>/]
    LoansApp --> ReserveBook[🔖 予約 /reserve/<id>/]
    LoansApp --> ReservationList[📋 予約一覧 /reservations/]
    LoansApp --> LoanHistory[📊 履歴 /history/]

    MembersApp --> MemberProfile[👤 プロファイル /profile/]
    MembersApp --> MemberRegister[✍️ 登録 /register/]
    MembersApp --> NotificationList[📬 通知 /notifications/]

    AuthApp --> Login[🔐 ログイン /login/]
    AuthApp --> Logout[👋 ログアウト /logout/]
```

## ビジネスロジックフロー

```mermaid
flowchart TD
    Start([システム開始]) --> UserCheck{ユーザー認証}
    
    UserCheck -->|未認証| LoginPage[ログインページ]
    UserCheck -->|認証済み| Dashboard[ダッシュボード]
    
    LoginPage --> Register[会員登録]
    LoginPage --> Login[ログイン]
    Register --> CreateProfile[プロファイル作成]
    Login --> Dashboard
    CreateProfile --> Dashboard
    
    Dashboard --> BookSearch[書籍検索]
    Dashboard --> LoanManagement[貸出管理]
    Dashboard --> Profile[プロファイル管理]
    
    BookSearch --> BookDetail[書籍詳細]
    BookDetail --> CheckAvailability{利用可能？}
    CheckAvailability -->|Yes| BorrowBook[貸出処理]
    CheckAvailability -->|No| ReserveBook[予約処理]
    
    BorrowBook --> UpdateInventory[在庫更新]
    BorrowBook --> CreateLoanRecord[貸出記録作成]
    
    LoanManagement --> ViewLoans[貸出中書籍]
    LoanManagement --> ReturnProcess[返却処理]
    LoanManagement --> ViewHistory[履歴確認]
    
    ReturnProcess --> UpdateLoanStatus[貸出状況更新]
    ReturnProcess --> RestoreInventory[在庫復元]
    
    Profile --> EditProfile[プロファイル編集]
    Profile --> ViewNotifications[通知確認]
```

## セキュリティ & 認証フロー

```mermaid
sequenceDiagram
    participant U as ユーザー
    participant B as ブラウザ
    participant D as Django
    participant DB as データベース
    participant A as 認証システム

    U->>B: ログイン要求
    B->>D: POST /accounts/login/
    D->>A: 認証チェック
    A->>DB: ユーザー情報確認
    DB-->>A: ユーザーデータ
    A-->>D: 認証結果
    
    alt 認証成功
        D->>DB: セッション作成
        D-->>B: セッションCookie + リダイレクト
        B-->>U: ダッシュボード表示
    else 認証失敗
        D-->>B: エラーメッセージ
        B-->>U: ログインページ（エラー表示）
    end

    Note over U,A: 以降のリクエストはセッション認証
    
    U->>B: 保護されたページアクセス
    B->>D: セッションCookie付きリクエスト
    D->>A: セッション検証
    
    alt セッション有効
        D->>DB: データ取得
        DB-->>D: データ返却
        D-->>B: ページレンダリング
        B-->>U: ページ表示
    else セッション無効
        D-->>B: ログインページへリダイレクト
        B-->>U: ログインページ表示
    end
```

## デプロイメント構成

```mermaid
graph TB
    subgraph "開発環境"
        DevCode[💻 ローカルコード]
        DevDB[(SQLite)]
        DevServer[Django Dev Server]
    end

    subgraph "バージョン管理"
        GitHub[📚 GitHub Repository]
    end

    subgraph "本番環境 (PythonAnywhere)"
        ProdCode[☁️ 本番コード]
        ProdDB[(MySQL)]
        ProdServer[WSGI Server]
        StaticFiles[静的ファイル]
        MediaFiles[メディアファイル]
    end

    DevCode --> GitHub
    GitHub --> ProdCode
    DevDB -.-> ProdDB
    DevServer -.-> ProdServer
    
    ProdCode --> ProdServer
    ProdServer --> ProdDB
    ProdServer --> StaticFiles
    ProdServer --> MediaFiles
```

## 技術スタック

```mermaid
graph LR
    subgraph "フロントエンド"
        HTML[HTML5]
        CSS[Tailwind CSS]
        JS[JavaScript]
    end

    subgraph "バックエンド"
        Django[Django 5.1.4]
        Python[Python 3.x]
    end

    subgraph "データベース"
        SQLite[SQLite3]
        MySQL[MySQL]
    end

    subgraph "その他"
        Pillow[Pillow]
        WSGI[WSGI]
    end

    HTML --> Django
    CSS --> Django
    JS --> Django
    Django --> Python
    Django --> SQLite
    Django --> MySQL
    Django --> Pillow
    Django --> WSGI
```

## システムの主要機能

```mermaid
mindmap
  root((図書館システム))
    書籍管理
      書籍登録
      カテゴリ管理
      在庫管理
      検索機能
    会員管理
      会員登録
      プロファイル管理
      権限管理
      通知機能
    貸出管理
      貸出処理
      返却処理
      履歴管理
      延滞管理
    予約機能
      予約登録
      利用可能通知
      予約キャンセル
    管理機能
      Django Admin
      統計レポート
      システム設定
```
