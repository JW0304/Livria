# backend/api/services/aladin.py

import requests
from django.conf import settings


def fetch_aladin_books(query_type: str, max_results: int = 100, start: int = 1, **extra_params):
    """
    Aladin TTB API를 JSON(JS) 포맷으로 호출하고, 'item' 리스트를 반환합니다.
    - query_type: API QueryType (Bestseller, ItemNewAll 등)
    - max_results: 한 번에 가져올 최대 개수 (최대 100)
    - start: 조회 시작 순번
    - extra_params: 추가 API 파라미터 (SearchTarget, CategoryId 등)
    """
    params = {
        'ttbkey':      settings.ALADIN_API_KEY,
        'QueryType':   query_type,
        'MaxResults':  max_results,
        'start':       start,
        'Cover':       'Big',
        'Output':      'js',
        'Version':     '20131101',
    }
    params.update(extra_params)
    response = requests.get(settings.ALADIN_BASE_URL, params=params)
    response.raise_for_status()

    data = response.json()
    # API 오류 처리
    if isinstance(data, dict) and data.get('errorCode'):
        raise RuntimeError(f"Aladin API error {data['errorCode']}: {data.get('errorMessage')}")
    # 'item' 리스트 반환
    if isinstance(data, dict):
        items = data.get('item')
        if isinstance(items, list):
            return items
        # 그 외 리스트 형태 값 반환
        for v in data.values():
            if isinstance(v, list):
                return v
    if isinstance(data, list):
        return data
    return []


def fetch_best_sellers_page(start: int, per_page: int = 100):
    return fetch_aladin_books(
        'Bestseller', max_results=per_page, start=start,
        SearchTarget='Book'
    )


def fetch_best_sellers_all(total: int = 300, per_page: int = 100):
    """
    최대 total 권수만큼, per_page 단위로 나눠 페이지별 호출 후
    중복 ISBN 제거하여 고유 리스트 반환
    """
    aggregated = []
    for offset in range(1, total + 1, per_page):
        aggregated.extend(fetch_best_sellers_page(start=offset, per_page=per_page))
    # 중복 ISBN 제거
    seen = set()
    unique = []
    for book in aggregated:
        isbn = book.get('isbn')
        if isbn and isbn not in seen:
            seen.add(isbn)
            unique.append(book)
    return unique


def fetch_new_items_page(start: int, per_page: int = 100):
    return fetch_aladin_books(
        'ItemNewAll', max_results=per_page, start=start,
        SearchTarget='Book'
    )


def fetch_new_items_all(total: int = 300, per_page: int = 100):
    """
    최대 total 권수만큼, per_page 단위로 나눠 페이지별 호출 후
    중복 ISBN 제거하여 고유 리스트 반환
    """
    aggregated = []
    for offset in range(1, total + 1, per_page):
        aggregated.extend(fetch_new_items_page(start=offset, per_page=per_page))
    seen = set()
    unique = []
    for item in aggregated:
        isbn = item.get('isbn')
        if isbn and isbn not in seen:
            seen.add(isbn)
            unique.append(item)
    return unique
