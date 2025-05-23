import re
import json
from typing import List, Optional

import requests
import wikipediaapi
from django.conf import settings
from openai import OpenAI


def _sanitize_author_name(name: str) -> str:
    """
    “홍길동 (지은이), 김철수 (옮긴이)” 형태 → 지은이 파트 우선,
    아니면 첫 파트 괄호 제거
    """
    parts = [p.strip() for p in re.split(r"[;,]", name)]
    for p in parts:
        if "지은이" in p:
            return re.sub(r"\s*\([^)]*\)", "", p).strip()
    return re.sub(r"\s*\([^)]*\)", "", parts[0]).strip()


def get_wikipedia_author_image(author_name: str) -> Optional[str]:
    API = "https://ko.wikipedia.org/w/api.php"
    clean = _sanitize_author_name(author_name)

    def _query_images(title: str) -> Optional[str]:
        params = {
            "action":      "query",
            "format":      "json",
            "prop":        "pageimages",
            "titles":      title,
            "piprop":      "original|thumbnail",
            "pithumbsize": 500,
            "origin":      "*",
        }
        r = requests.get(API, params=params, timeout=5)
        r.raise_for_status()
        pages = r.json().get("query", {}).get("pages", {})
        for p in pages.values():
            if "original" in p:
                return p["original"]["source"]
            if "thumbnail" in p:
                return p["thumbnail"]["source"]
        return None

    # 1) 바로 시도
    img = _query_images(clean)
    if img:
        return img

    # 2) search API 로 실제 타이틀 찾아 재시도
    sr = requests.get(API, params={
        "action":   "query",
        "format":   "json",
        "list":     "search",
        "srsearch": clean,
        "srlimit":  1,
        "origin":   "*",
    }, timeout=5)
    sr.raise_for_status()
    hits = sr.json().get("query", {}).get("search", [])
    if hits:
        return _query_images(hits[0]["title"])

    return None


def get_author_info(author_name: str) -> dict:
    clean = _sanitize_author_name(author_name)

    # 1) wikipediaapi 로 페이지 수집
    wiki = wikipediaapi.Wikipedia(
        user_agent="LivriaBackend/1.0 (contact@livria.example)",
        language="ko"
    )
    page = wiki.page(clean)

    text = page.summary + "\n\n" if page.exists() else f"작가명: {clean}"

    def _dump_sections(secs):
        out = ""
        for s in secs:
            out += s.title + "\n" + s.text + "\n\n"
            out += _dump_sections(s.sections)
        return out

    if page.exists():
        text += _dump_sections(page.sections)

    # 2) OpenAI 로 JSON-only 요청
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    system = (
        "당신은 책 작가 정보를 JSON으로만 응답하는 전문가입니다.\n"
        "절대로 다른 텍스트를 포함하지 말고, 반드시 아래 형식만 반환하세요:\n"
        "{\n"
        '  "author_info": "<간결한 작가 소개>",\n'
        '  "author_works": ["대표작1", "대표작2", "대표작3", "대표작4", "대표작5"]\n'
        "}\n"
        "대표작은 반드시 5가지 이상 포함해야 합니다."
    )
    resp = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": text},
        ],
        max_tokens=512,
        temperature=0.7,
    )

    # 3) JSON 파싱
    try:
        data = json.loads(resp.choices[0].message.content)
        return {
            "author_info": data.get("author_info", ""),
            "author_works": data.get("author_works", []),
        }
    except json.JSONDecodeError:
        return {"author_info": "", "author_works": []}
