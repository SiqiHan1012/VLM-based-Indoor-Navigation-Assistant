import io
from fastapi import APIRouter, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from PIL import Image

from app.core.state import nav_state
from app.core.config import get_timestamp, DEBUG_SAVE, DEBUG_DIR, FPS_DEFAULT
from app.core.prompts import get_nav_prompt
from app.services.vision import pre_veto_from_frame, vconcat_full_and_floor
from app.services.vlm import run_vlm_inference
from app.services.asr import transcribe_audio

router = APIRouter()
templates = Jinja2Templates(directory="app/templates") 

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "fps": FPS_DEFAULT})

@router.get("/current_goal")
def get_current_goal():
    return {"current_goal": nav_state.get_goal()}

@router.post("/asr")
async def process_audio(audio: UploadFile = File(...)):
    b = await audio.read()
    if len(b) < 100: 
        return JSONResponse({"intent": "noop"})
    
    # Debug save logic
    if DEBUG_SAVE:
        import time
        save_path = DEBUG_DIR / f"chunk_{int(time.time())}_{audio.filename or 'audio.bin'}" 
        with open(save_path, "wb") as f:
            f.write(b)

    result = transcribe_audio(b, audio.filename, audio.content_type)
    return JSONResponse(result)

@router.post("/infer")
async def infer_frame(image: UploadFile = File(...), goal: str = Form("")):
    nav_state.frame_counter += 1
    
    # 1. Determine goal
    current_goal = (goal or "").strip()
    if not current_goal:
        current_goal = nav_state.get_goal()

    # 2. Image Processing
    img_bytes = await image.read()
    pil_full = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    
    # Geometric processing & concatenation (Full + Floor)
    pre_veto, feats, floor_crop = pre_veto_from_frame(pil_full)
    dual_pil = vconcat_full_and_floor(pil_full, floor_crop)

    # 3. Build Prompt and Call VLM
    prompt = get_nav_prompt(current_goal)
    raw_text, parsed = run_vlm_inference(dual_pil, prompt) 

    # 4. Result Parsing and Safety Fallback
    next_action = parsed.get("next_action", "stop")
    sectors = parsed.get("sectors", {})
    goal_reached = parsed.get("at_goal", False)
    goal_visible = parsed.get("goal_visible", False)
    
    # Safety Check 1: If goal distance is 'near', always stop
    if str(parsed.get("goal_distance", "")).lower() == "near":
         next_action = "stop"
         goal_reached = True

    # Safety Check 2: If all sectors are blocked, stop
    def is_safe(val): return str(val).lower() == "safe"
    if not (is_safe(sectors.get("left")) or is_safe(sectors.get("center")) or is_safe(sectors.get("right"))):
        if not goal_reached:
            next_action = "stop"

    return JSONResponse({
        "next_action": next_action,
        "sectors": sectors,
        "goal_reached": goal_reached,
        "goal_visible": goal_visible,
        "goal_side": parsed.get("goal_side", "none"),
        "goal_distance": parsed.get("goal_distance", "unknown"),
        "timestamp": get_timestamp(),
        "goal_used": current_goal
    })