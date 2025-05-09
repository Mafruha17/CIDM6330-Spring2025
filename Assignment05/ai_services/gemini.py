import os
from typing import List
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from django.conf import settings

API_KEY = getattr(settings, "GEMINI_API_KEY", None) or os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY missing in environment or settings.py")

genai.configure(api_key=API_KEY)

# ❗ pick one that shows up in list_models():
MODEL_NAME = os.getenv("GEMINI_MODEL", "models/gemini-1.5-flash")

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    generation_config={"temperature": 0.2, "max_output_tokens": 300},
    safety_settings=[
        {"category": HarmCategory.HARM_CATEGORY_HARASSMENT,
         "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE},
        {"category": HarmCategory.HARM_CATEGORY_HATE_SPEECH,
         "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE},
        {"category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
         "threshold": HarmBlockThreshold.BLOCK_NONE},
        {"category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
         "threshold": HarmBlockThreshold.BLOCK_NONE},
    ],
)

def summarize_note(note_text: str, language: str = "en") -> str:
    prompt = (
        f"Summarize the clinical note below in plain {language}. "
        "Exactly three patient‑friendly sentences—no medical jargon:\n\n"
        f"{note_text}"
    )
    return model.generate_content(prompt).text.strip()

def detect_device_anomaly(readings: List[float]) -> bool:
    data = ",".join(map(str, readings))
    prompt = (
        "Analyze this list of heart‑rate readings (comma‑separated):\n"
        f"{data}\n\n"
        "Return TRUE if any drop >20 bpm occurs within 5 minutes, else FALSE."
    )
    return "TRUE" in model.generate_content(prompt).text.upper()
