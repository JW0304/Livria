# api/management/commands/update_similar_books.py

import os
import numpy as np
from django.core.management.base import BaseCommand
from django.db import transaction
from sklearn.metrics.pairwise import cosine_similarity

from api.models import Book
from api.utils import get_upstage_embedding


class Command(BaseCommand):
    help = '모든 도서에 대해 임베딩을 생성·업데이트하고, 유사도 상위 4권을 similar_books에 저장합니다.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('유사 도서 업데이트 시작...'))

        # 모든 도서 로드
        books = Book.objects.all()

        # 1) 각 도서 임베딩 생성 또는 로드
        for book in books:
            text = f"{book.title} {book.description or ''}"
            if not book.embedding:
                emb = get_upstage_embedding(text)
                book.embedding = emb
                book.save(update_fields=['embedding'])
                self.stdout.write(f'  - [임베딩 생성] "{book.title}"')

        # 2) 각 도서에 대해 유사도 계산 및 similar_books 설정
        embeddings = [np.array(book.embedding).reshape(1, -1) for book in books]
        book_ids = [book.id for book in books]

        # 미리 합쳐두면 빠르지만 메모리가 부족할 수 있으니 순회 방식으로
        for idx, book in enumerate(books):
            base_vec = embeddings[idx]
            sims = []
            for jdx, other in enumerate(books):
                if other.id == book.id:
                    continue
                score = cosine_similarity(base_vec, embeddings[jdx])[0][0]
                sims.append((other.id, score))
            # 유사도 내림차순 정렬 후 상위 4개
            sims.sort(key=lambda x: x[1], reverse=True)
            top_ids = [bid for bid, _ in sims[:4]]

            # DB 업데이트
            with transaction.atomic():
                book.similar_books.set(top_ids)
            self.stdout.write(f'  - [추천 설정] "{book.title}": {top_ids}')

        self.stdout.write(self.style.SUCCESS('유사 도서 업데이트 완료!'))
