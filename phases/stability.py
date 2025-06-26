import networkx as nx
import numpy as np
import spacy

nlp = spacy.load("en_core_web_sm")

def analyze_stability(proposition: str) -> str:
    doc = nlp(proposition)

    # Extract meaningful concepts (nouns, verbs, key adjectives)
    concepts = [token.text for token in doc if token.pos_ in {"NOUN", "VERB", "ADJ"}]
    concepts = list(set(concepts))  # Deduplicate

    # Initialize graph
    G = nx.Graph()
    G.add_nodes_from(concepts)

    # Add edges based on syntactic dependencies
    for token in doc:
        if token.head.text in concepts and token.text in concepts and token.head != token:
            G.add_edge(token.head.text, token.text)

    # If graph is too small, skip analysis
    if G.number_of_edges() == 0:
        return "Insufficient structure to analyze. Graph has no meaningful edges."

    # Assign synthetic semantic vectors
    vectors = {node: np.random.rand(5) for node in G.nodes}

    def update_vector(vec, neighbors):
        if not neighbors:
            return vec
        avg_neighbor_vec = np.mean([vectors[n] for n in neighbors], axis=0)
        return 0.5 * vec + 0.5 * avg_neighbor_vec  # Weighted blend

    # Evolve over time
    for _ in range(10):
        vectors = {node: update_vector(vec, list(G.neighbors(node))) for node, vec in vectors.items()}

    # Measure final coherence as average edge similarity
    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    similarities = [cosine_similarity(vectors[u], vectors[v]) for u, v in G.edges]
    avg_similarity = np.mean(similarities)

    return (
        f"Graph nodes: {len(G.nodes)}\n"
        f"Graph edges: {len(G.edges)}\n"
        f"Average semantic coherence (cosine): {avg_similarity:.3f}\n"
        f"Concepts: {concepts}\n"
    )
