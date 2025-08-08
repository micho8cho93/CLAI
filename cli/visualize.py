import typer

app = typer.Typer(help="Visualize the project's structure " \
                        "with a flowchart")

@app.command("visualize")
def visualize_code():
    typer.echo("Creating a flowchart for codebase visualization.")