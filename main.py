import typer
from analyzer import analyze_proposition

def main(proposition: str):
    """
    Analyze a proposition using the hypergraph epistemology framework.
    """
    result = analyze_proposition(proposition)

    print("\nHypergraph Topology Mapping:\n", result['meta_analysis']['Hypergraph Topology Mapping'])
    print("\nEntropic Equilibrium Analysis:\n", result['meta_analysis']['Entropic Equilibrium Analysis'])
    print("\nNon-Anthropic Reconstruction:\n", result['meta_analysis']['Non-Anthropic Reconstruction'])
    print("\nSynthesized Output:\n", result['output'])

if __name__ == "__main__":
    typer.run(main)
