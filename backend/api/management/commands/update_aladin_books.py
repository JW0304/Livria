import re
from django.core.management.base import BaseCommand
from datetime import datetime
from api.services.aladin import fetch_best_sellers_all, fetch_new_items_all
from api.services.author_media_service import (
    get_wikipedia_author_image,
    get_author_info
)
from api.models import Book, Author, Category

class Command(BaseCommand):
    help = 'Fetch up to 300 books and sync both Book/Author info to DB'

    def handle(self, *args, **options):
        for category_name, fetch_fn in [
            ('베스트셀러', fetch_best_sellers_all),
            ('신간',        fetch_new_items_all),
        ]:
            cat, _ = Category.objects.get_or_create(name=category_name)
            books = fetch_fn(total=300, per_page=100)
            self.stdout.write(self.style.MIGRATE_HEADING(
                f"Syncing {category_name} ({len(books)} items)…"
            ))

            for item in books:
                raw_author = item.get('author') or ''
                # Author 생성 or 조회
                author_name = re.sub(r'\s*\([^)]*\)', '', raw_author).split(';')[0].strip()
                author, created = Author.objects.get_or_create(name=author_name)

                # Author 필드 채우기
                if not author.image_url:
                    author.image_url = get_wikipedia_author_image(raw_author)
                if not author.summary:
                    info = get_author_info(raw_author)
                    author.summary = info.get("author_info", "")
                    author.works   = info.get("author_works", [])
                author.save()

                # Book 생성/업데이트
                ps = item.get('pubDate','')
                pub_date = None
                if ps and len(ps)==8:
                    try:
                        pub_date = datetime.strptime(ps, "%Y%m%d").date()
                    except:
                        pass

                Book.objects.update_or_create(
                    isbn=item.get('isbn',''),
                    defaults={
                        'title':                  item.get('title',''),
                        'publisher':              item.get('publisher',''),
                        'cover_url':              item.get('cover',''),
                        'description':            item.get('description',''),
                        'pub_date':               pub_date,
                        'category':               cat,
                        'author':                 author,
                        'global_recommend_count': 0,
                    }
                )

            self.stdout.write(self.style.SUCCESS(
                f"{category_name} sync complete."
            ))
