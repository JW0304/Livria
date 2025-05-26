import os
from openai import OpenAI

# Upstage API 클라이언트 초기화
client = OpenAI(
    api_key=os.getenv("UPSTAGE_API_KEY"),
    base_url="https://api.upstage.ai/v1"
)

def get_upstage_embedding(text: str) -> list[float]:
    """
    주어진 텍스트에 대해 Upstage API로 임베딩을 생성하여 반환합니다.

    Args:
        text (str): 임베딩을 생성할 문자열.

    Returns:
        list[float]: 생성된 임베딩 벡터.
    """
    response = client.embeddings.create(
        input=text,
        model="embedding-query"
    )
    # 응답 데이터 구조: {'data': [{'embedding': [...]}], ...}
    return response.data[0].embedding
