import typer
from pathlib import Path
from core.visualizer import print_tree_console, create_graphviz_chart
from core.json import export_as_json

app = typer.Typer(help="Visualize the project's structure " \
                        "with a flowchart")

@app.command("tree")
def tree_console(path: str = '.', 
                max_depth: int = typer.Option(10, help="How deep into the folder structure to go"),
    ):
    """Prints the directory structure as a tree in the terminal"""
    print_tree_console(path)

@app.command("graph")
def graph_image(path: str = '.', output: str = 'flowchart'):
    """Generate a flowchart image of the project structure."""
    create_graphviz_chart(path, output)

@app.command("json")
def create_json(
    export_json: bool = typer.Option(False, "--export-json", help="Export project structure to JSON."),
    output_file: Path = typer.Option("structure.json", help="Path to output JSON file."),
    max_depth: int = typer.Option(None, help="Maximum depth to traverse."),
):
    """
    Visualize or export the project directory structure.
    """
    if export_json:
        typer.echo(f"Exporting structure to {output_file}...")
        export_as_json(output_path=output_file, max_depth=max_depth)
        typer.echo("Export complete.")
    else:
        typer.echo("Make sure to add --export-json if you want to create a json file.")
        # reuse the Tree display logic from earlier phase