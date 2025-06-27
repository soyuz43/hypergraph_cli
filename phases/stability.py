# phases\stability.py

import networkx as nx
import numpy as np
import spacy
from transformers import AutoTokenizer, AutoModel
import torch

# Load spaCy for parsing
nlp = spacy.load("en_core_web_sm")

# Load BERT tokenizer and model for contextual embeddings
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")
model.eval()


def get_concept_vectors_bert(proposition: str, concepts: list) -> dict:
    """
    Given a sentence and a list of concept strings, returns a mapping from
    each concept to its contextual BERT embedding (as a numpy array).
    Falls back to a random vector if the concept token isn't found.
    """
    # Tokenize and run through the model
    inputs = tokenizer(proposition, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)

    # Last hidden state: (1, seq_len, hidden_size)
    hidden_states = outputs.last_hidden_state.squeeze(0)  # (seq_len, H)
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"].squeeze(0))

    vectors = {}
    for concept in concepts:
        # find all token positions containing the concept text
        matches = [
            i for i, tok in enumerate(tokens)
            if concept.lower() == tok.lower()
            or tok.lower().startswith(concept.lower())
            or concept.lower().startswith(tok.lower())
        ]
        if matches:
            # average the hidden states for all matching tokens
            stack = torch.stack([hidden_states[i] for i in matches], dim=0)
            vec = stack.mean(dim=0).cpu().numpy()
        else:
            # fallback: random vector of the same size
            vec = np.random.rand(model.config.hidden_size)
        vectors[concept] = vec

    return vectors


def analyze_stability(proposition: str) -> str:
    """
    Builds a concept graph from the proposition, diffuses real semantic vectors
    across that graph, and returns a measure of internal coherence.
    """
    # Parse with spaCy
    doc = nlp(proposition)

    # Extract meaningful concepts (nouns, verbs, adjectives)
    concepts = [token.text for token in doc if token.pos_ in {"NOUN", "VERB", "ADJ"}]
    concepts = list(dict.fromkeys(concepts))  # preserve order, deduplicate

    # Build the graph
    G = nx.Graph()
    G.add_nodes_from(concepts)
    for token in doc:
        head = token.head.text
        if head in concepts and token.text in concepts and head != token.text:
            G.add_edge(head, token.text)

    # If graph is too small, skip analysis
    if G.number_of_edges() == 0:
        return "Insufficient structure to analyze. Graph has no meaningful edges."

    # Get real BERT-based embeddings for each concept
    vectors = get_concept_vectors_bert(proposition, concepts)

    # Diffusion update: blend each vector with its neighbors'
    def update_vector(vec, neighbors):
        if not neighbors:
            return vec
        neigh_vecs = [vectors[n] for n in neighbors]
        avg_neigh = np.mean(neigh_vecs, axis=0)
        return 0.5 * vec + 0.5 * avg_neigh

    # Run diffusion for a fixed number of iterations
    for _ in range(10):
        vectors = {
            node: update_vector(vectors[node], list(G.neighbors(node)))
            for node in G.nodes
        }

    # Compute average cosine similarity across edges
    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12)

    similarities = [
        cosine_similarity(vectors[u], vectors[v]) for u, v in G.edges
    ]
    avg_similarity = float(np.mean(similarities))

    # Format the result
    return (
        f"Graph nodes: {G.number_of_nodes()}\n"
        f"Graph edges: {G.number_of_edges()}\n"
        f"Average semantic coherence (cosine): {avg_similarity:.3f}\n"
        f"Concepts: {concepts}\n"
    )

