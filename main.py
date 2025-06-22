import typer
from analyzer import analyze_proposition
from pathlib import Path
import os
import time

app = typer.Typer(help="Hypergraph Epistemology CLI Tool")

def get_next_output_filename(base: str = "analysis", ext: str = "txt", folder: str = "output"):
    os.makedirs(folder, exist_ok=True)
    i = 1
    while True:
        filename = f"{base}_{i:03d}.{ext}"
        full_path = os.path.join(folder, filename)
        if not os.path.exists(full_path):
            return full_path
        i += 1

@app.command()
def main(proposition: str, markdown: bool = typer.Option(False, "--markdown", help="Output as a markdown file")):
    """
    Analyze a proposition using the hypergraph epistemology framework.
    """
    start_time = time.time()

    result = analyze_proposition(proposition)
    ext = "md" if markdown else "txt"
    output_path = get_next_output_filename(ext=ext)

    output_text = (
        f"# Proposition Analysis\n\n"
        f"**Proposition:** {proposition}\n\n"
        f"## Hypergraph Topology Mapping\n{result['meta_analysis']['Hypergraph Topology Mapping']}\n\n"
        f"## Entropic Equilibrium Analysis\n{result['meta_analysis']['Entropic Equilibrium Analysis']}\n\n"
        f"## Non-Anthropic Reconstruction\n{result['meta_analysis']['Non-Anthropic Reconstruction']}\n\n"
        f"## Synthesized Output\n{result['output']}\n"
    ) if markdown else (
        f"Proposition: {proposition}\n\n"
        f"Hypergraph Topology Mapping:\n{result['meta_analysis']['Hypergraph Topology Mapping']}\n\n"
        f"Entropic Equilibrium Analysis:\n{result['meta_analysis']['Entropic Equilibrium Analysis']}\n\n"
        f"Non-Anthropic Reconstruction:\n{result['meta_analysis']['Non-Anthropic Reconstruction']}\n\n"
        f"Synthesized Output:\n{result['output']}\n"
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_text)

    elapsed_time = time.time() - start_time
    print(f"Analysis written to: {output_path}")
    print(f"Completed in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    app()
