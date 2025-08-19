import typer
from pathlib import Path
from core.markdown import generate_markdown_docs

app = typer.Typer(help="Generate READMEs or documentation.")

@app.command("docs")
def docs_create(
    path: str = '.',
    output: Path = typer.Option("README.md", help="Output file for the documentation."),
):
    """
    Generate documentation for a file or a directory.
    """
    typer.echo(f"Generating documentation for {path}...")
    markdown_content = generate_markdown_docs(path)
    if output:
        with output.open("w", encoding="utf-8") as f:
            f.write(markdown_content)
        typer.echo(f"Documentation saved to {output}")
    else:
        typer.echo(markdown_content)

