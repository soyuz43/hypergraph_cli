# Hypergraph Epistemology CLI Tool

A command-line tool for analyzing epistemic propositions through the lens of **hypergraph cognition**, **entropic equilibrium**, and **non-anthropic reconstruction**. This project implements the first step toward an executable dialectical framework for interrogating conceptual structures, exposing implicit biases, and reconstructing statements from alien or posthuman perspectives.

---

## 📐 Conceptual Overview

Each proposition is analyzed in three layers:

1. **Hypergraph Topology Mapping**  
   Identifies hidden assumptions, power structures, and modular epistemic configurations underlying the proposition.

2. **Entropic Equilibrium Analysis**  
   Examines whether the proposition serves as a cognitive stabilizer or disruptor, and how it resists or invites epistemic perturbation.

3. **Non-Anthropic Reconstruction**  
   Reimagines the proposition through alien, posthuman, or multispecies epistemologies—exposing the anthropocentric biases embedded in its structure.

---

## 🚀 Usage

### 1. Clone the repository

```bash
git clone https://github.com/yourname/hypergraph_cli.git
cd hypergraph_cli
````

### 2. Create and activate a virtual environment

```bash
python -m venv hgcli-env
source ./hgcli-env/Scripts/activate    # On Git Bash or WSL
# OR
.\hgcli-env\Scripts\Activate.ps1       # On PowerShell
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Make sure Ollama is running

Install the model if you haven’t yet:

```bash
ollama pull qwen2.5-coder:14b-instruct-q5_K_M
ollama serve
```

### 5. Run the tool

```bash
python main.py "Consciousness is an irreducible phenomenon."
```

---

## 🔧 Project Structure

```
hypergraph_cli/
├── main.py                  # Entry point CLI (typer.run)
├── analyzer.py              # Orchestration layer for the analysis pipeline
├── phases/                  # Each epistemic operation lives here
│   ├── topology.py
│   ├── equilibrium.py
│   └── reconstruction.py
├── llm/                     # Ollama interface
│   └── ollama.py
├── requirements.txt
```

---

## Example Output

```text
Hypergraph Topology Mapping:
This proposition encodes a monist cognitive topology...

Entropic Equilibrium Analysis:
It operates as a stabilizer that resists epistemic entropy...

Non-Anthropic Reconstruction:
From an alien frame, consciousness is a recursive sensory oscillation...

Synthesized Output:
Topology:
...

Equilibrium:
...

Non-Anthropic Perspective:
...
```

---

## 📦 Dependencies

* [Typer](https://typer.tiangolo.com/)
* [Ollama](https://ollama.com/)
* Python 3.10+

---

## ✨ Coming Soon

* Markdown or JSON output formatting
* Support for subcommands (e.g. `summarize`, `reframe`)
* Integration with frontend hypergraph visualizer
* Option to inject your own epistemic regime templates

---

## ⚠️ Disclaimer

This project is experimental and philosophical. It does not produce truth; it surfaces latent structures and tensions in language and ideology.

---


