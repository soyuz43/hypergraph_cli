import ollama

OLLAMA_MODEL = "qwen2.5-coder:7b-instruct-q6_K"

def run_ollama(prompt: str, lens_context: str = "") -> str:
    """
    Sends a prompt to the local Ollama instance and returns the model's response.
    Optionally prepends an epistemological lens context to the prompt.
    """
    try:
        full_prompt = f"{lens_context.strip()}\n\n{prompt.strip()}".strip()
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": full_prompt}],
            stream=False
        )
        return response['message']['content']
    except Exception as e:
        return f"[ERROR] Ollama request failed: {e}"
