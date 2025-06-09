import os, json, re, requests
from django.conf import settings
from openai import OpenAI

def get_wikipedia_author_image(full_name: str) -> str:
    name = re.sub(r'\s*\(.*?\)', '', full_name).strip()
    url = "https://ko.wikipedia.org/w/api.php"
    params = {
        "action":"query","format":"json","prop":"pageimages",
        "titles":name,"piprop":"original","origin":"*",
    }
    try:
        r = requests.get(url, params=params, timeout=5)
        pages = r.json().get("query", {}).get("pages", {})
        for p in pages.values():
            if "original" in p:
                return p["original"]["source"]
    except:
        pass
    return settings.STATIC_URL + "images/default_author.png"

def get_author_info(full_name: str) -> dict:
    name = re.sub(r'\s*\(.*?\)', '', full_name).strip()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    system  = (
        "작가 정보를 JSON으로만 출력하세요:\n"
        '{ "author_info": "...", "author_works": ["...", ...] }'
    )
    messages = [
        {"role":"system", "content": system},
        {"role":"user",   "content": name},
    ]
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.5,
        max_tokens=512,
    )
    try:
        return json.loads(resp.choices[0].message.content)
    except:
        return {"author_info": "", "author_works": []}
