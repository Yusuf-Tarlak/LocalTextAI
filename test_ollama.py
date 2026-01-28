import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1"

def ask(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=180)
    r.raise_for_status()
    return r.json()["response"].strip()

def analyze_text(text: str) -> dict:
    prompt = f"""
Sadece JSON döndür. Başka hiçbir şey yazma.

Bu formatta olsun:
{{
  "summary": "string",
  "bullet_points": ["string", "string"],
  "sentiment": "positive|negative|neutral",
  "topics": ["string", "string"]
}}

Metin:
\"\"\"{text}\"\"\"
"""
    raw = ask(prompt)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"error": "Json Parse edilemedi", "raw_model_output": raw}

if __name__ == "__main__":
    print("Metni yapıştır, bitince Enter'a bas. (Boş bırakıp Enter -> çıkış)\n")
    text = input("Metin: ").strip()

    if not text:
        print("çıkış...")
    else:
        result = analyze_text(text)
        print("\n--- sonuç (json ile) ---")
        print(json.dumps(result, ensure_ascii=False, indent=2))
