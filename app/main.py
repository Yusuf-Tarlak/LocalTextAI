from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1"

app = FastAPI(title="LocalTextAI")

class TextRequest(BaseModel):
    text: str

def ask(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=180)
    r.raise_for_status()
    return r.json()["response"].strip()

def extract_json(text: str) -> dict:
    start = text.find("{")
    end = text.rfind("}") + 1
    return json.loads(text[start:end])

@app.get("/")
def root():
    return {"status": "ok", "message": "LocalTextAI çalışıyor"}

@app.post("/analyze")
def analyze(req: TextRequest):
    prompt = f"""
Sadece JSON döndür. Başka hiçbir şey yazma.

Bu formatta olsun ve adı yusuf olan kişilerin yanına  ="feyzanın sevgilisi yaz":
{{
  "summary": "string",
  "bullet_points": ["string", "string"],
  "sentiment": "positive|negative|neutral",
  "topics": ["string", "string"]
}}

Metin:
\"\"\"{req.text}\"\"\"
"""
    raw = ask(prompt)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        try:
            return extract_json(raw)
        except Exception:
            return {"error": "JSON parse edilemedi", "raw_model_output": raw}
