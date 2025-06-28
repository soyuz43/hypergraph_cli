# phases/stability.py

import os
import networkx as nx
import numpy as np
import spacy
from transformers import AutoTokenizer, AutoModel
import torch
from phases.mahalanobis import train_mahalanobis_model, compute_mahalanobis_distance

# Load spaCy for parsing
nlp = spacy.load("en_core_web_sm")

# Load BERT tokenizer and model for contextual embeddings
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")
model.eval()

# === 🔧 Configurable path for baseline ===
BASELINE_PATH = "data/baseline_vectors.npy"

# === 📥 Lazy-load + patch Mahalanobis model ===
if not os.path.exists(BASELINE_PATH):
    raise FileNotFoundError(
        f"Missing baseline vector file at {BASELINE_PATH}. Run `build_baseline.py` first."
    )

REFERENCE_VECTORS = np.load(BASELINE_PATH)
REFERENCE_MAHAL_MODEL = train_mahalanobis_model(REFERENCE_VECTORS)


def get_concept_vectors_bert(proposition: str, concepts: list) -> dict:
    inputs = tokenizer(proposition, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    hidden_states = outputs.last_hidden_state.squeeze(0)
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"].squeeze(0))

    vectors = {}
    for concept in concepts:
        matches = [
            i for i, tok in enumerate(tokens)
            if concept.lower() == tok.lower()
            or tok.lower().startswith(concept.lower())
            or concept.lower().startswith(tok.lower())
        ]
        if matches:
            stack = torch.stack([hidden_states[i] for i in matches], dim=0)
            vec = stack.mean(dim=0).cpu().numpy()
        else:
            vec = np.random.rand(model.config.hidden_size)
        vectors[concept] = vec
    return vectors


def analyze_stability(proposition: str) -> str:
    doc = nlp(proposition)
    concepts = [token.text for token in doc if token.pos_ in {"NOUN", "VERB", "ADJ"}]
    concepts = list(dict.fromkeys(concepts))

    G = nx.Graph()
    G.add_nodes_from(concepts)
    for token in doc:
        head = token.head.text
        if head in concepts and token.text in concepts and head != token.text:
            G.add_edge(head, token.text)

    if G.number_of_edges() == 0:
        return "Insufficient structure to analyze. Graph has no meaningful edges."

    vectors = get_concept_vectors_bert(proposition, concepts)

    def update_vector(vec, neighbors):
        if not neighbors:
            return vec
        neigh_vecs = [vectors[n] for n in neighbors]
        avg_neigh = np.mean(neigh_vecs, axis=0)
        return 0.5 * vec + 0.5 * avg_neigh

    for _ in range(10):
        vectors = {
            node: update_vector(vectors[node], list(G.neighbors(node)))
            for node in G.nodes
        }

    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12)

    internal_similarities = [
        cosine_similarity(vectors[u], vectors[v]) for u, v in G.edges
    ]
    avg_internal_cosine = float(np.mean(internal_similarities))

    # Per-concept Mahalanobis and contrastive cosine
    mahal_scores = {
        concept: compute_mahalanobis_distance(REFERENCE_MAHAL_MODEL, vec)
        for concept, vec in vectors.items()
    }
    contrastive_scores = {
        concept: float(np.mean([cosine_similarity(vec, ref) for ref in REFERENCE_VECTORS]))
        for concept, vec in vectors.items()
    }

    avg_mahalanobis = float(np.mean(list(mahal_scores.values())))
    avg_contrastive_cosine = float(np.mean(list(contrastive_scores.values())))

    lines = [
        f"Graph nodes: {G.number_of_nodes()}",
        f"Graph edges: {G.number_of_edges()}",
        f"Average internal coherence (cosine): {avg_internal_cosine:.3f}",
        f"Average contrast-to-baseline (cosine): {avg_contrastive_cosine:.3f}",
        f"Average Mahalanobis dispersion (vs. baseline): {avg_mahalanobis:.3f}",
        f"Concepts: {concepts}",
        "",
        "Detailed concept-level Mahalanobis and cosine similarity scores relative to baseline:",
    ]

    for concept in concepts:
        maha = mahal_scores.get(concept, 0.0)
        contrast = contrastive_scores.get(concept, 0.0)
        lines.append(f"  {concept:15} | Mahalanobis: {maha:.3f} | Contrast Cosine: {contrast:.3f}")

    return "\n".join(lines)
