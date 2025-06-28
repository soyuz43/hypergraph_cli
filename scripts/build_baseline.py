# build_baseline.py

import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel

# Load BERT base model
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")
model.eval()

# Clean factual propositions
propositions = [
    "Water boils at 100 degrees Celsius.",
    "The Earth orbits the Sun.",
    "The capital of France is Paris.",
    "Humans have 206 bones in their bodies.",
    "The Moon affects ocean tides.",
    "Plants convert sunlight into energy through photosynthesis.",
    "Light travels faster than sound.",
    "A triangle has three sides.",
    "The human heart has four chambers.",
    "Venus is the second planet from the Sun.",
    "Gravity pulls objects toward each other.",
    "The speed of light in a vacuum is approximately 299,792 kilometers per second.",
    "Mount Everest is the tallest mountain on Earth.",
    "DNA carries genetic information.",
    "The Pacific Ocean is the largest ocean on Earth.",
    "Water is composed of two hydrogen atoms and one oxygen atom.",
    "The Great Wall of China is visible from space with aid.",
    "Sound requires a medium to travel through.",
    "A year has 365 days, except in leap years.",
    "The boiling point of water decreases at higher altitudes.",
    "Electricity is the flow of electrons.",
    "Bats are mammals that can fly.",
    "The Sahara is the largest hot desert in the world.",
    "Oxygen is necessary for human respiration.",
    "The brain is the control center of the nervous system.",
    "Jupiter is the largest planet in our solar system.",
    "The Amazon River is one of the longest rivers in the world.",
    "An octagon has eight sides.",
    "Blood circulates through arteries and veins.",
    "Saturn has prominent rings made of ice and rock.",
    "A prism splits light into its component colors.",
    "The sun rises in the east and sets in the west.",
    "Matter can exist in solid, liquid, or gaseous states.",
    "Penguins are birds that cannot fly.",
    "The Eiffel Tower is located in Paris.",
    "Chlorophyll gives plants their green color.",
    "Magnetism and electricity are related forces.",
    "Atoms are the basic units of matter.",
    "Carbon dioxide is a greenhouse gas.",
    "The Statue of Liberty is in New York Harbor.",
    "Rainbows are caused by light refraction in water droplets.",
    "The lungs are essential for breathing.",
    "Dinosaurs went extinct millions of years ago.",
    "The internet is a global network of computers.",
    "A solar eclipse occurs when the Moon blocks the Sun.",
    "Cells are the building blocks of life.",
    "The speed of sound is slower than the speed of light.",
    "Earthquakes are caused by tectonic plate movement.",
    "Butterflies undergo metamorphosis.",
    "Photosynthesis produces oxygen."
]

def get_sentence_vector(sentence: str):
    inputs = tokenizer(sentence, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    vec = outputs.last_hidden_state.mean(dim=1).squeeze(0).cpu().numpy()
    return vec

vectors = [get_sentence_vector(p) for p in propositions]
vectors_np = np.stack(vectors)

# Save
np.save("data/baseline_vectors.npy", vectors_np)
print("✅ Baseline vectors saved to data/baseline_vectors.npy")
