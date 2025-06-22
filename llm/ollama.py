import ollama

OLLAMA_MODEL = "qwen2.5-coder:3b-instruct-q8_0"

def run_ollama(prompt: str) -> str:
    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content'].strip()
    except Exception as e:
        return f"[ERROR] Ollama request failed: {e}"
