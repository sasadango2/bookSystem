from django.core.management.base import BaseCommand
from books.models import Category, Book
from django.contrib.auth.models import User
from members.models import MemberProfile
from datetime import date


class Command(BaseCommand):
    help = 'Create sample data for library system'

    def handle(self, *args, **options):
        # カテゴリの作成
        categories_data = [
            {'name': '小説・文学', 'slug': 'novels'},
            {'name': '技術書', 'slug': 'tech'},
            {'name': 'ビジネス', 'slug': 'business'},
            {'name': 'エッセイ', 'slug': 'essays'},
            {'name': '歴史', 'slug': 'history'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # 書籍の作成
        books_data = [
            {
                'title': 'Pythonプログラミング入門',
                'slug': 'python-programming-intro',
                'author': '山田太郎',
                'isbn': '9784000000001',
                'description': 'Pythonの基礎から応用まで学べる一冊です。',
                'publication_date': date(2023, 1, 15),
                'publisher': 'テック出版',
                'category_slug': 'tech',
                'available_copies': 3,
                'total_copies': 5,
            },
            {
                'title': '夏目漱石短編集',
                'slug': 'natsume-soseki-collection',
                'author': '夏目漱石',
                'isbn': '9784000000002',
                'description': '夏目漱石の代表的な短編小説を集めた作品集です。',
                'publication_date': date(1906, 4, 1),
                'publisher': '古典文学社',
                'category_slug': 'novels',
                'available_copies': 2,
                'total_copies': 3,
            },
            {
                'title': '効率的なビジネス思考術',
                'slug': 'efficient-business-thinking',
                'author': '佐藤花子',
                'isbn': '9784000000003',
                'description': 'ビジネスで成功するための思考法を解説します。',
                'publication_date': date(2022, 8, 10),
                'publisher': 'ビジネス新書',
                'category_slug': 'business',
                'available_copies': 1,
                'total_copies': 2,
            },
            {
                'title': '日本の歴史 近世編',
                'slug': 'japanese-history-kinsei',
                'author': '歴史研究会',
                'isbn': '9784000000004',
                'description': '江戸時代から明治維新までの日本史を詳しく解説。',
                'publication_date': date(2021, 3, 20),
                'publisher': '歴史出版社',
                'category_slug': 'history',
                'available_copies': 0,  # 貸出中
                'total_copies': 2,
            },
            {
                'title': '私の読書日記',
                'slug': 'my-reading-diary',
                'author': '田中美咲',
                'isbn': '9784000000005',
                'description': '一人の読書愛好家が綴る心温まるエッセイ集。',
                'publication_date': date(2023, 6, 5),
                'publisher': 'エッセイ書房',
                'category_slug': 'essays',
                'available_copies': 4,
                'total_copies': 4,
            },
        ]

        for book_data in books_data:
            category = Category.objects.get(slug=book_data['category_slug'])
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults={
                    'title': book_data['title'],
                    'slug': book_data['slug'],
                    'author': book_data['author'],
                    'description': book_data['description'],
                    'publication_date': book_data['publication_date'],
                    'publisher': book_data['publisher'],
                    'category': category,
                    'available_copies': book_data['available_copies'],
                    'total_copies': book_data['total_copies'],
                    'available': True,
                }
            )
            if created:
                self.stdout.write(f'Created book: {book.title}')

        # スーパーユーザーの作成（既に存在しない場合）
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@library.com',
                password='admin123'
            )
            self.stdout.write('Created admin user: admin/admin123')

        # テストユーザーの作成
        test_users = [
            {'username': 'testuser1', 'email': 'test1@example.com', 'first_name': '太郎', 'last_name': '山田'},
            {'username': 'testuser2', 'email': 'test2@example.com', 'first_name': '花子', 'last_name': '佐藤'},
        ]

        for user_data in test_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
                
                # 会員プロファイルの作成
                profile, profile_created = MemberProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'membership_type': 'regular',
                        'member_id': f'M{user.id:08d}',
                        'phone': '090-1234-5678',
                        'address': '東京都渋谷区1-1-1',
                    }
                )
                self.stdout.write(f'Created test user: {user.username}/testpass123')

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write(self.style.SUCCESS('Admin user: admin/admin123'))
        self.stdout.write(self.style.SUCCESS('Test users: testuser1/testpass123, testuser2/testpass123'))
