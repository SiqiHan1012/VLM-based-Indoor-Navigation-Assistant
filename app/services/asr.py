import requests
import re
from app.core.config import OPENAI_API_KEY, OPENAI_BASE, ASR_MODEL
from app.core.state import nav_state

def transcribe_audio(audio_bytes: bytes, filename: str, content_type: str) -> dict:
    if not OPENAI_API_KEY: 
        return {"intent": "noop", "transcript": ""}

    # 1. Prepare file format (Simplified: assumes WAV if suggested)
    name = (filename or "chunk.bin").lower()
    if name.endswith(".wav") or "wav" in content_type:
        up_name, up_ct = "chunk.wav", "audio/wav"
    else:
        # Fallback for WebM/Opus, using content_type if available
        up_name, up_ct = "chunk.bin", content_type or "application/octet-stream"

    try:
        # 2. Call OpenAI Whisper API
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        files = {"file": (up_name, audio_bytes, up_ct)} 
        data = {"model": ASR_MODEL, "language": "en", "response_format": "json"}

        r = requests.post(f"{OPENAI_BASE}/audio/transcriptions",
                          headers=headers, files=files, data=data, timeout=10)
        r.raise_for_status()
        transcript = r.json().get("text", "").strip()
        
        # 3. Intent Parsing
        return parse_intent(transcript)

    except Exception as e:
        print(f"[ASR Error] {e}")
        return {"intent": "noop", "transcript": ""}

def parse_intent(text: str) -> dict:
    tlow = text.lower()
    current_goal = nav_state.get_goal()

    # Command control logic
    if re.search(r"\b(start|begin|go)\b", tlow):
        return {"intent": "start", "transcript": text, "current_goal": current_goal}
    if re.search(r"\b(stop|halt|pause|end)\b", tlow):
        return {"intent": "stop", "transcript": text, "current_goal": current_goal}

    # Set goal logic: Match "direct" command
    m = re.match(r"^\s*(please\s+)?direct\b(.*)$", tlow)
    if m:
        rest = text[m.start(2):m.end(2)].strip(" .,:;-")
        tokens = rest.split()
        drop = 0
        tokens_lower = [t.lower() for t in tokens]
        if len(tokens_lower) >= 2 and tokens_lower[0] == "me" and tokens_lower[1] in ("to", "toward", "towards"):
            drop = 2
        elif len(tokens_lower) >= 1 and tokens_lower[0] == "me":
            drop = 1
        
        goal_spoken = " ".join(tokens[drop:]).strip(" .,:;-")
        if len(goal_spoken) >= 3:
            nav_state.set_goal(goal_spoken)
            return {"intent": "set_goal", "goal": goal_spoken, "transcript": text}

    return {"intent": "noop", "transcript": text, "current_goal": current_goal}