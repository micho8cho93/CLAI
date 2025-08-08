import typer
from core.visualizer import print_tree_console, create_graphviz_chart

app = typer.Typer(help="Visualize the project's structure " \
                        "with a flowchart")

@app.command("tree")
def tree_console(path: str = '.'):
    """Prints the directory structure as a tree in the terminal"""
    print_tree_console(path)

@app.command("graph")
def graph_image(path: str = '.', output: str = 'flowchart'):
    """Generate a flowchart image of the project structure."""
    create_graphviz_chart(path, output)