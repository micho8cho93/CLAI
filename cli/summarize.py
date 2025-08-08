import typer
from pathlib import Path
from core.llm import build_structure_prompt, run_llm

app = typer.Typer(help="Generate summaries of the codebase")

@app.command("create")
def create_summary(
    file: Path = typer.Option("structure.json", help="Path to project structure JSON"),
    model_path: str = typer.Option(..., help="Path to local LLM model file"),
):
    """
    Use a local LLM to analyze and summarize the project structure.
    """
    prompt = build_structure_prompt(file)
    typer.echo("Querying the local LLM...")
    response = run_llm(prompt, model_path=model_path)
    typer.echo("\nSummary:\n")
    typer.echo(response)