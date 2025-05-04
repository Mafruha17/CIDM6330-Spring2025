# Assignment05/ai_services/services.py

import openai
from django.conf import settings

# configure once
openai.api_key = settings.OPENAI_API_KEY
MODEL = settings.OPENAI_MODEL

def summarize_note(note_text: str, language: str = "en") -> str:
    """
    Send clinical note to LLM and get back a three-line patient-friendly summary.
    """
    prompt = (
        f"Summarize the clinical note below in three sentences, "
        f"plain {language}, no jargon:\n\n{note_text}"
    )
    resp = openai.ChatCompletion.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=200,
    )
    return resp.choices[0].message.content.strip()

def detect_device_anomaly(readings: list[float]) -> bool:
    """
    Quick anomaly check: returns True if a sudden drop >20 bpm occurs in the series.
    """
    serialized = ",".join(str(x) for x in readings)
    prompt = (
        "Given this comma-separated list of heart-rate readings, "
        "return 'TRUE' if any sudden drop (>20 bpm) occurs within 5 minutes, else 'FALSE':\n"
        + serialized
    )
    resp = openai.ChatCompletion.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=3,
    )
    return "TRUE" in resp.choices[0].message.content.upper()
