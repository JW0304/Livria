# api/management/commands/build_recommendations.py
from django.core.management.base import BaseCommand
from api.models import Book
from api.utils import get_upstage_embedding
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Command(BaseCommand):
    help = "모든 도서에 대해 임베딩을 생성하고, 유사도 상위 3권을 recommended_books에 저장"

    def handle(self, *args, **options):
        books = list(Book.objects.all())
        self.stdout.write(f"총 {len(books)}권의 도서 처리 시작")

        # 1) 임베딩 생성 (없으면 생성)
        for b in books:
            if not b.embedding:
                text = f"{b.title} {b.description}"
                emb = get_upstage_embedding(text)
                b.embedding = emb
                b.save(update_fields=["embedding"])
                self.stdout.write(f"  [임베딩 생성] {b.id} {b.title}")

        # 2) 유사도 계산 및 추천 목록 갱신
        embeddings = np.array([b.embedding for b in books])
        sim_matrix = cosine_similarity(embeddings)  # N×N

        for idx, b in enumerate(books):
            # 자기 자신 제외, 유사도 내림차순 정렬
            scores = list(enumerate(sim_matrix[idx]))
            scores = [s for s in scores if s[0] != idx]
            scores.sort(key=lambda x: x[1], reverse=True)
            top3_idxs = [i for i, _ in scores[:3]]

            # M2M 초기화 및 세이브
            b.recommended_books.clear()
            for ti in top3_idxs:
                b.recommended_books.add(books[ti])
            b.save()
            self.stdout.write(f"  [추천 갱신] {b.id} → {[books[i].id for i in top3_idxs]}")

        self.stdout.write(self.style.SUCCESS("✅ 추천 도서 빌드 완료"))
