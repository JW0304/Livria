# backend/api/management/commands/update_aladin_books.py

import json
import re
from datetime import datetime

from django.core.management.base import BaseCommand

from api.models import Book, Author, Category
from api.services.aladin import fetch_best_sellers_all, fetch_new_items_all
from api.services.author_media_service import (
    get_wikipedia_author_image,
    get_author_info,
)


class Command(BaseCommand):
    help = 'Fetch up to 300 books from Aladin API and save/update them into the local database'

    def handle(self, *args, **options):
        # 1) 베스트셀러 동기화
        cat_bs, _ = Category.objects.get_or_create(name="베스트셀러")
        self.stdout.write(self.style.MIGRATE_HEADING("→ Sync '베스트셀러' (up to 300 items)…"))
        books = fetch_best_sellers_all(total=300, per_page=100)
        self.stdout.write(self.style.NOTICE(f"Fetched {len(books)} Bestseller items"))

        for idx, item in enumerate(books, start=1):
            title = item.get("title", "").strip()
            self.stdout.write(f"[{idx}/{len(books)}] {title} saved.")

            # — 작가 처리
            full_name = item.get("author", "").strip() or "Unknown"
            author, _ = Author.objects.get_or_create(name=full_name)

            # — 출판일 파싱 (두 가지 포멧 지원)
            pub_date = None
            pd = item.get("pubDate", "").strip()
            if pd:
                # 1) YYYYMMDD
                try:
                    pub_date = datetime.strptime(pd, "%Y%m%d").date()
                except ValueError:
                    # 2) ISO YYYY-MM-DD
                    try:
                        pub_date = datetime.fromisoformat(pd).date()
                    except ValueError:
                        pub_date = None

            # — 작가 이미지 & 소개/대표작
            author.image_url = (
                get_wikipedia_author_image(author.name)
                or "/static/images/default_author.png"
            )
            info = get_author_info(author.name)
            author.summary = info.get("author_info", "")
            author.works = json.dumps(info.get("author_works", []), ensure_ascii=False)
            author.save()

            # — 책 저장 (publisher 필드 추가)
            Book.objects.update_or_create(
                isbn=item.get("isbn", ""),
                defaults={
                    "title": title,
                    "author": author,
                    "publisher": item.get("publisher", ""),
                    "cover_url": item.get("cover", ""),
                    "description": item.get("description", ""),
                    "pub_date": pub_date,
                    "category": cat_bs,
                    "global_recommend_count": 0,
                },
            )

        self.stdout.write(self.style.SUCCESS("Bestseller sync complete."))

        # 2) 신간 동기화
        cat_new, _ = Category.objects.get_or_create(name="신간")
        self.stdout.write(self.style.MIGRATE_HEADING("→ Sync '신간' (up to 300 items)…"))
        items = fetch_new_items_all(total=300, per_page=100)
        self.stdout.write(self.style.NOTICE(f"Fetched {len(items)} New items"))

        for idx, item in enumerate(items, start=1):
            title = item.get("title", "").strip()
            self.stdout.write(f"[{idx}/{len(items)}] {title} saved.")

            full_name = item.get("author", "").strip() or "Unknown"
            author, _ = Author.objects.get_or_create(name=full_name)

            pub_date = None
            pd = item.get("pubDate", "").strip()
            if pd:
                try:
                    pub_date = datetime.strptime(pd, "%Y%m%d").date()
                except ValueError:
                    try:
                        pub_date = datetime.fromisoformat(pd).date()
                    except ValueError:
                        pub_date = None

            author.image_url = (
                get_wikipedia_author_image(author.name)
                or "/static/images/default_author.png"
            )
            info = get_author_info(author.name)
            author.summary = info.get("author_info", "")
            author.works = json.dumps(info.get("author_works", []), ensure_ascii=False)
            author.save()

            Book.objects.update_or_create(
                isbn=item.get("isbn", ""),
                defaults={
                    "title": title,
                    "author": author,
                    "publisher": item.get("publisher", ""),
                    "cover_url": item.get("cover", ""),
                    "description": item.get("description", ""),
                    "pub_date": pub_date,
                    "category": cat_new,
                    "global_recommend_count": 0,
                },
            )

        self.stdout.write(self.style.SUCCESS("New items sync complete."))
