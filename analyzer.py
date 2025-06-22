from phases.topology import hypergraph_topology_mapping
from phases.equilibrium import entropic_equilibrium_analysis
from phases.reconstruction import non_anthropic_reconstruction

def analyze_proposition(proposition: str) -> dict:
    htm = hypergraph_topology_mapping(proposition)
    eee = entropic_equilibrium_analysis(proposition)
    nar = non_anthropic_reconstruction(proposition)

    final_output = synthesize_output(htm, eee, nar)

    return {
        "original": proposition,
        "output": final_output,
        "meta_analysis": {
            "Hypergraph Topology Mapping": htm,
            "Entropic Equilibrium Analysis": eee,
            "Non-Anthropic Reconstruction": nar
        }
    }

def synthesize_output(htm: str, eee: str, nar: str) -> str:
    return (
        f"Topology:\n{htm.strip()}\n\n"
        f"Equilibrium:\n{eee.strip()}\n\n"
        f"Non-Anthropic Perspective:\n{nar.strip()}"
    )
