import typer

app = typer.Typer(help="Generate summaries of the codebase")

@app.command("summarize")
def summarize_project():
    typer.echo("Creating codebase summary now.")