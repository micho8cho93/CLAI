import typer

app = typer.Typer(help="Monitor the project for changes.")

@app.command("start")
def start_monitoring():
    typer.echo("Monitoring commencing...")

@app.command("stop")
def stop_monitoring():
    typer.echo("Monitoring terminated.")