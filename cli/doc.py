import typer

app = typer.Typer(help="Generate READMEs or documentation.")

@app.command("readme")
def readme_create():
    typer.echo("Readme will be generated now.")

@app.command("docs")
def docs_create():
    typer.echo("Documentation will be created now.")