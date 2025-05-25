# api/services/music_service.py

import torch

# ── patch: torch.get_default_device 없으면 CPU 기본 반환 ──
if not hasattr(torch, "get_default_device"):
    torch.get_default_device = lambda: torch.device("cpu")

from audiocraft.models import MusicGen

# 사용할 모델 이름 (small, medium, large)
MODEL_NAME = "facebook/musicgen-small"

# 태그별 세부 프롬프트 (악기·스타일 포함)
PROMPT_MAP = {
    "슬픔과 외로움":       "A slow, melancholic solo piano melody evoking deep sadness and loneliness.",
    "사랑과 그리움":       "A gentle acoustic guitar tune expressing love and longing.",
    "위로와 평안":         "Soft strings and ambient pads bringing comfort and peace.",
    "에너지와 고조":       "Upbeat electronic dance track with driving drums and rising energy.",
    "몽환적이고 감성적인": "Dreamy synth textures with ethereal vocals and emotional atmosphere."
}

_model_instance = None

def get_musicgen_model():
    global _model_instance
    if _model_instance is None:
        # CPU 환경에서 로드 (device 지정)
        model = MusicGen.get_pretrained(MODEL_NAME, device="cpu")
        # 30초까지 생성하도록 설정
        model.set_generation_params(duration=30.0)
        _model_instance = model
    return _model_instance

def generate_music_tensor(tag: str):
    """
    주어진 태그명으로부터 프롬프트를 뽑아 음악 Tensor를 생성합니다.
    """
    model = get_musicgen_model()
    prompt = PROMPT_MAP.get(tag)
    if prompt is None:
        raise ValueError(f"지원되지 않는 태그: {tag}")
    wav_list = model.generate([prompt])
    return wav_list[0]
