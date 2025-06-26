import typer
from analyzer import analyze_proposition
from pathlib import Path
import os
import time
from typing import List

app = typer.Typer(help="Hypergraph Epistemology CLI Tool")

def get_next_output_filename(base: str = "analysis", ext: str = "txt", folder: str = "output") -> str:
    """
    Generate a deduplicated filename in the specified folder.
    """
    os.makedirs(folder, exist_ok=True)
    i = 1
    while True:
        filename = f"{base}_{i:03d}.{ext}"
        full_path = os.path.join(folder, filename)
        if not os.path.exists(full_path):
            return full_path
        i += 1

@app.command()
def main(
    proposition: str,
    lenses: List[str] = typer.Option(
        None,
        "--lens",
        "-l",
        help="Epistemological lenses to apply (haraway, barad, foucault, spivak)."
    ),
    markdown: bool = typer.Option(
        False,
        "--markdown",
        help="Output as a markdown file"
    )
):
    """
    Analyze a proposition using the hypergraph epistemology framework,
    optionally applying specified epistemological lenses.
    """
    start_time = time.time()

    # Perform analysis with selected lenses
    result = analyze_proposition(proposition, lenses)
    ext = "md" if markdown else "txt"
    output_path = get_next_output_filename(ext=ext)

    # Format output header
    lens_header = ""
    if lenses:
        lens_header = f"Lenses: {', '.join(lenses)}\n\n"

    if markdown:
        output_text = (
            f"# Proposition Analysis\n\n"
            f"**Proposition:** {proposition}\n\n"
            f"{lens_header}"
            f"## Hypergraph Topology Mapping\n{result['meta_analysis']['Hypergraph Topology Mapping']}\n\n"
            f"## Entropic Equilibrium Analysis\n{result['meta_analysis']['Entropic Equilibrium Analysis']}\n\n"
            f"## Non-Anthropic Reconstruction\n{result['meta_analysis']['Non-Anthropic Reconstruction']}\n\n"
            f"## Mathematical Stability Analysis\n{result['stability']}\n\n"
            f"## Synthesized Output\n{result['output']}\n"
        )
    else:
        output_text = (
            f"Proposition: {proposition}\n\n"
            f"{lens_header}"
            f"Hypergraph Topology Mapping:\n{result['meta_analysis']['Hypergraph Topology Mapping']}\n\n"
            f"Entropic Equilibrium Analysis:\n{result['meta_analysis']['Entropic Equilibrium Analysis']}\n\n"
            f"Non-Anthropic Reconstruction:\n{result['meta_analysis']['Non-Anthropic Reconstruction']}\n\n"
            f"Mathematical Stability Analysis:\n{result['stability']}\n\n"
            f"Synthesized Output:\n{result['output']}\n"
        )

    # Write to file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_text)

    elapsed_time = time.time() - start_time
    typer.secho(f"Analysis written to: {output_path}", fg=typer.colors.GREEN)
    typer.secho(f"Completed in {elapsed_time:.2f} seconds", fg=typer.colors.BLUE)

if __name__ == "__main__":
    app()
