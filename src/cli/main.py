import typer
from cli import monitor, doc, visualize, summarize

app = typer.Typer(help="CLAI is a CLI AI assistant to "
                        "that helps developers summarize and visualize codebases,"
                        "create technical documentation, "
                        "and monitor & report real-time changes to your codebase."
                        "Our advice is to use CLAI to help you better understand and communicate"
                        "about codebases and monitor changes made by other CLI AI tools.")


app.add_typer(monitor.app)
app.add_typer(doc.app,)
app.add_typer(summarize.app)
app.add_typer(visualize.app)


if __name__ == "__main__":
    app()