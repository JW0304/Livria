import requests
from django.conf import settings
import openai

# OpenAI 키 설정
openai.api_key = settings.OPENAI_API_KEY

def fetch_wikipedia_author_info(name: str) -> dict:
    """
    1) 위키피디아 REST API로 author 페이지 summary 조회
    2) 이미지(썸네일) URL, 원문 요약(extract), 페이지 URL 파싱
    3) OpenAI로 간결한 작가 소개글 생성
    """
    # 1) Wikipedia Summary 엔드포인트 호출
    title = name.replace(' ', '_')
    summary_url = f'https://en.wikipedia.org/api/rest_v1/page/summary/{title}'
    res = requests.get(summary_url)
    res.raise_for_status()
    data = res.json()

    extract   = data.get('extract', '')  # 본문 요약
    thumb     = data.get('thumbnail', {}).get('source')
    page_url  = data.get('content_urls', {}) \
                    .get('desktop', {}) \
                    .get('page')

    # 2) OpenAI로 소개글 생성
    prompt = (
        "다음 위키피디아 요약을 바탕으로, 작가소개를 2-3문장 한국어로 작성해 주세요:\n\n"
        f"{extract}"
    )
    resp = openai.ChatCompletion.create(
        model="o4-mini",
        messages=[{"role":"user", "content": prompt}],
        temperature=0.7,
    )
    intro = resp.choices[0].message.content.strip()

    return {
        "wiki_url":  page_url,
        "image_url": thumb,
        "summary":   extract,
        "intro":     intro,
    }
