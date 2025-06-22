from phases.topology import hypergraph_topology_mapping
from phases.equilibrium import entropic_equilibrium_analysis
from phases.reconstruction import non_anthropic_reconstruction

# Define available lenses here
EPISTEMOLOGICAL_LENSES = {
    "haraway": "Lens: Donna Haraway's Situated Knowledges.\nEmphasize partiality, embodiment, and positionality in knowledge production. Avoid god-trick objectivity.",
    "barad": "Lens: Karen Barad's Intra-action.\nFocus on how agencies emerge through relational entanglements. Reject atomistic separability.",
    "foucault": "Lens: Michel Foucault's Knowledge-Power.\nAnalyze discourse as structured by regimes of power. Investigate what is rendered sayable or unsayable.",
    "spivak": "Lens: Gayatri Spivak's Subaltern.\nAttend to the silenced, displaced, or structurally unvoiced. Examine epistemic violence.",
    "none": ""  # Default case
}

def analyze_proposition(proposition: str, lenses: list[str] = None) -> dict:
    if lenses is None:
        lenses = ["none"]

    # Combine selected lenses into a single context block
    lens_context = "\n\n".join(
        EPISTEMOLOGICAL_LENSES.get(lens.lower(), "") for lens in lenses
    ).strip()

    htm = hypergraph_topology_mapping(proposition, lens_context)
    eee = entropic_equilibrium_analysis(proposition, lens_context)
    nar = non_anthropic_reconstruction(proposition, lens_context)

    final_output = synthesize_output(htm, eee, nar)

    return {
        "original": proposition,
        "lenses": lenses,
        "output": final_output,
        "meta_analysis": {
            "Hypergraph Topology Mapping": htm,
            "Entropic Equilibrium Analysis": eee,
            "Non-Anthropic Reconstruction": nar
        }
    }

def synthesize_output(htm: str, eee: str, nar: str) -> str:
    return (
        f"--- Topology ---\n{htm.strip()}\n\n"
        f"--- Equilibrium ---\n{eee.strip()}\n\n"
        f"--- Non-Anthropic Perspective ---\n{nar.strip()}"
    )
