from llm.ollama import run_ollama

def non_anthropic_reconstruction(proposition: str) -> str:
    prompt = f"""
You are performing a Non-Anthropic Reconstruction.
Reframe the following proposition from an alien, post-human, or multispecies epistemology.
Avoid human-centric assumptions about logic, agency, or intelligence.

Proposition: {proposition}
"""
    return run_ollama(prompt)
