import requests
from django.conf import settings

def fetch_aladin_books(query_type: str, max_results: int = 50, start: int = 1, **extra):
    params = {
        'ttbkey':        settings.ALADIN_API_KEY,
        'QueryType':     query_type,
        'MaxResults':    max_results,
        'start':         start,
        'Cover':         'Big',
        'Output':        'JS',
        'Version':       '20131101',
        'SearchTarget':  'Book',
    }
    params.update(extra)
    resp = requests.get(settings.ALADIN_BASE_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if data.get('errorCode') not in (None, '0'):
        raise RuntimeError(f"Aladin API error {data['errorCode']}: {data.get('errorMessage')}")
    return data.get('item', [])

def fetch_best_sellers_all(total: int = 50, per_page: int = 50):
    agg = []
    for offset in range(1, total+1, per_page):
        agg.extend(fetch_aladin_books('Bestseller', max_results=per_page, start=offset))
    seen = set(); unique = []
    for b in agg:
        isbn = b.get('isbn')
        if isbn and isbn not in seen:
            seen.add(isbn); unique.append(b)
    return unique

def fetch_new_items_all(total: int = 50, per_page: int = 50):
    agg = []
    for offset in range(1, total+1, per_page):
        agg.extend(fetch_aladin_books('ItemNewAll', max_results=per_page, start=offset))
    seen = set(); unique = []
    for b in agg:
        isbn = b.get('isbn')
        if isbn and isbn not in seen:
            seen.add(isbn); unique.append(b)
    return unique

def fetch_editor_picks_all(total: int = 50, per_page: int = 50):
    agg = []
    for offset in range(1, total+1, per_page):
        agg.extend(fetch_aladin_books('BlogBest', max_results=per_page, start=offset))
    seen = set(); unique = []
    for b in agg:
        isbn = b.get('isbn')
        if isbn and isbn not in seen:
            seen.add(isbn); unique.append(b)
    return unique
