# backend/api/management/commands/update_aladin_books.py

import json
import re
from datetime import datetime
from django.core.management.base import BaseCommand
from api.models import Book, Author, Category, Genre
from api.services.aladin import (
    fetch_best_sellers_all,
    fetch_new_items_all,
    fetch_editor_picks_all,
)
from api.services.author_media_service import (
    get_wikipedia_author_image,
    get_author_info,
)

# 7개 장르 매핑
GENRE_MAP = {
    "소설/시/희곡": ["소설", "시", "희곡"],
    "경제/경영":     ["경제", "경영"],
    "자기계발":     ["자기계발", "성장", "자기"],
    "인문/교양":     ["인문", "교양", "철학", "역사"],
    "취미/실용":     ["취미", "실용", "요리", "공예"],
    "어린이/청소년": ["어린이", "청소년", "아동"],
    "과학":         ["과학", "공학", "자연"],
}

def classify_genre(raw_cat: str) -> str:
    for genre, keywords in GENRE_MAP.items():
        for kw in keywords:
            if kw in (raw_cat or ""):
                return genre
    return "인문/교양"

class Command(BaseCommand):
    help = 'Aladin API에서 도서 동기화'

    def handle(self, *args, **opts):
        # 1) 장르 테이블 기본값 생성
        for g in GENRE_MAP.keys():
            Genre.objects.get_or_create(name=g)

        # 2) 동기화 대상 소스
        sources = [
            ("베스트셀러",  fetch_best_sellers_all),
            ("신간",        fetch_new_items_all),
            ("블로거 추천", fetch_editor_picks_all),
        ]

        DEFAULT_SUMMARY = "이 도서의 작가 정보가 아직 등록되지 않았습니다."

        for label, fn in sources:
            cat, _ = Category.objects.get_or_create(name=label)
            self.stdout.write(f"→ Sync '{label}' (최대 50)…")
            items = fn(total=50, per_page=50)

            for idx, item in enumerate(items, start=1):
                # — 제목 정리
                raw_title = item.get("title", "").strip()
                title = re.split(r"\s*-\s*", raw_title, 1)[0]
                title = re.sub(r"\s*\(.*?\)$", "", title).strip() or raw_title
                self.stdout.write(f"[{idx}/{len(items)}] {title}")

                # — 출간일 파싱
                pd_raw = item.get("pubDate", "") or ""
                pd_digits = "".join(ch for ch in pd_raw if ch.isdigit())
                pub_date = None
                if len(pd_digits) >= 8:
                    try:
                        pub_date = datetime.strptime(pd_digits[:8], "%Y%m%d").date()
                    except ValueError:
                        pub_date = None

                # — 작가 처리
                name = item.get("author", "").strip() or "Unknown"
                author, created = Author.objects.get_or_create(name=name)

                # ---- summary 처리 (빈 문자열 or 기본 메시지인 경우만 재시도)
                need_update = (not author.summary) or (author.summary == DEFAULT_SUMMARY)
                if need_update:
                    info = get_author_info(name)
                    ai = info.get("author_info", "")
                    if isinstance(ai, str) and ai.strip():
                        author.summary = ai.strip()
                    else:
                        author.summary = DEFAULT_SUMMARY
                    author.works = info.get("author_works", [])

                # ---- 이미지 처리
                if not author.image_url:
                    author.image_url = get_wikipedia_author_image(name)

                author.save()

                # — 장르 분류
                raw_catname = item.get("categoryName", "")
                gen_name = classify_genre(raw_catname)
                genre, _ = Genre.objects.get_or_create(name=gen_name)

                # — 설명(description) 기본 문구 처리
                desc = (item.get("description") or "").strip()
                if not desc:
                    desc = "아직 설명이 등록되지 않은 도서입니다."

                # — Book upsert
                Book.objects.update_or_create(
                    isbn=item.get("isbn", ""),
                    defaults={
                        "title":                  title,
                        "author":                 author,
                        "publisher":              item.get("publisher", "").strip(),
                        "cover_url":              item.get("cover", "").strip(),
                        "description":            desc,
                        "pub_date":               pub_date,
                        "category":               cat,
                        "genre":                  genre,
                        "global_recommend_count": 0,
                    }
                )

            self.stdout.write(self.style.SUCCESS(f"✓ '{label}' 완료"))
