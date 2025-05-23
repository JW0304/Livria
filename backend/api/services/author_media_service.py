import os
import json
import re
from typing import List, Optional

import requests
from django.conf import settings
from openai import OpenAI
from pydantic import BaseModel

# — 작가 프로필 이미지 가져오기 (Wikipedia API 활용)
def get_wikipedia_author_image(full_name: str) -> Optional[str]:
    # "(지은이)", "(옮긴이)" 등 괄호 내용 제거
    search_name = re.sub(r'\s*\(.*?\)', '', full_name).strip()

    url = "https://ko.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "pageimages",
        "titles": search_name,
        "piprop": "original",
        "origin": "*",
    }

    try:
        resp = requests.get(url, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            if "original" in page:
                return page["original"]["source"]
    except Exception:
        pass

    return None

# — Pydantic 모델 정의
class AuthorInfoJson(BaseModel):
    author_info: str
    author_works: List[str]

# — GPT로부터 작가 정보 받아오기
def get_author_info(full_name: str) -> dict:
    # "(지은이)" 등 제거
    search_name = re.sub(r'\s*\(.*?\)', '', full_name).strip()

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "당신은 책 작가 정보를 요약/추출해주는 전문가입니다."},
            {"role": "user", "content": search_name},
        ],
        response_format=AuthorInfoJson,
    )

    raw = response.choices[0].message.content

    # BaseModel 인스턴스면 model_dump, 문자열이면 json.loads
    if isinstance(raw, BaseModel):
        return raw.model_dump()
    elif isinstance(raw, str):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {}
    else:
        return {}
