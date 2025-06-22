from llm.ollama import run_ollama

def entropic_equilibrium_analysis(proposition: str, lens_context: str = "") -> str:
    prompt = f"""
You are performing an Entropic Equilibrium Analysis.
Determine:

- Whether this proposition functions as a stabilizer or disruptor of cognition
- What forms of perturbation it resists or absorbs
- How institutional, social, or cultural forces maintain or destabilize it

Proposition: {proposition}
"""
    return run_ollama(prompt)
