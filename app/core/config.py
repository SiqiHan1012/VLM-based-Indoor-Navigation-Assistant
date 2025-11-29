import os
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent.parent

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE = os.getenv("OPENAI_BASE", "https://api.openai.com/v1")
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")

ASR_MODEL = os.getenv("ASR_MODEL", "whisper-1")
VLM_MODEL = os.getenv("VLM_MODEL", "qwen3-vl-plus")

TZ_NAME = os.getenv("TZ_NAME", "America/Toronto")
DEBUG_SAVE = os.getenv("DEBUG_SAVE", "False").lower() in ("true", "1")
DEBUG_DIR = BASE_DIR / "debug_audio" 
DEBUG_DIR.mkdir(parents=True, exist_ok=True)
FPS_DEFAULT = int(os.getenv("CLIENT_FPS", "1"))

try:
    from zoneinfo import ZoneInfo
except ImportError:
    import pytz
    class ZoneInfo:
        def __init__(self, name): self._tz = pytz.timezone(name)
        def __call__(self): return self._tz

def get_timestamp():
    tz = ZoneInfo(TZ_NAME) if callable(getattr(ZoneInfo, "__call__", None)) is None else ZoneInfo(TZ_NAME)

    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S") + " ET"
