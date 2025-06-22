from llm.ollama import run_ollama

def hypergraph_topology_mapping(proposition: str) -> str:
    prompt = f"""
You are performing a Hypergraph Topology Mapping.
Analyze the following proposition by identifying:

- Hidden assumptions
- Cognitive modules and regimes involved
- Power relations embedded in the structure
- Metaphysical or structural commitments

Proposition: {proposition}
"""
    return run_ollama(prompt)
