# api/utils.py
import os
import numpy as np
from openai import OpenAI
from django.conf import settings
from .models import Book

# Upstage(혹은 OpenAI) 임베딩 생성 클라이언트 초기화
_client = OpenAI(
    api_key=os.getenv("UPSTAGE_API_KEY"),
    base_url=os.getenv("UPSTAGE_BASE_URL", "https://api.upstage.ai/v1")
)

def get_upstage_embedding(text: str) -> list[float]:
    """
    주어진 텍스트로 임베딩을 요청하고, 리스트 형태로 반환합니다.
    """
    response = _client.embeddings.create(
        model="embedding-query",
        input=text
    )
    return response.data[0].embedding

def get_similar_books(book_id):
    try:
        book = Book.objects.get(id=book_id)
        # 유사한 책을 가져오는 로직 (예: cosine similarity를 활용한 추천 책 목록)
        similar_books = Book.objects.filter(genre=book.genre).exclude(id=book.id)[:3]  # 예시: 같은 장르의 상위 3개 도서
        return similar_books
    except Book.DoesNotExist:
        raise ValueError("책을 찾을 수 없습니다.")