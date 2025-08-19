import typer
from pathlib import Path
from core.markdown import generate_markdown_docs

app = typer.Typer(help="Generate READMEs or documentation.")


