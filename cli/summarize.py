import typer
from pathlib import Path
from core.llm import run_llm

app = typer.Typer(help="Generate summaries of the codebase")

@app.command("summary")
def create_summary(
    file: Path = typer.Option("structure.json", help="Path to project structure JSON"),
):
    """
    Use a local LLM to analyze and summarize the project structure.
    """
    if not file.exists():
        typer.echo(f"Error: File {file} does not exist.", err=True)
        raise typer.Exit(1)
    
    typer.echo("Querying the local LLM...")
    try:
        response = run_llm(structure_path=file)
        typer.echo("\nSummary:\n")
        typer.echo(response)
    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)

if __name__ == "__main__":
    app()