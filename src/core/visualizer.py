import os
from pathlib import Path
from rich.tree import Tree
from rich.console import Console
from graphviz import Digraph

console = Console()

def print_tree_console(path: str, max_depth: int = 10):
    """Print directory as tree using rich"""
    path = Path(path)
    tree = Tree(f"[bold blue]{path.name}/")

    def add_branch(directory: Path, parent_tree: Tree, current_depth: int):
        if current_depth > max_depth:
            return
        for item in sorted(directory.iterdir()):
            if item.name.startswith('.' or '..') :
                continue #skip hidden files/folders 
            if item.is_dir():
                branch = parent_tree.add(f"[bold magenta]{item.name}/")
                add_branch(item, branch, current_depth + 1)
            else: 
                parent_tree.add(f"{item.name}")

    add_branch(path, tree, 1)
    console.print(tree)


def create_graphviz_chart(path: str, output_name: str):
    """Generates a .png image of the directory structure using Graphviz."""

    path = Path(path)
    graph = Digraph(comment="Project Structure", format="png")

    def add_nodes(directory: Path, parent_id: str):
        for item in sorted(directory.iterdir()):
            if item.name.startswith('.' or '..'):
                continue
            node_id = str(item.relative_to(path))
            label = item.name + '/' if item.is_dir() else item.name
            graph.node(node_id, label=label, shape='box' if item.is_file() else 'folder')

            if parent_id:
                graph.edge(parent_id, node_id)
            if item.is_dir():
                add_nodes(item, node_id)

    root_id = str(path.name)
    graph.node(root_id, label=path.name + '/', shape='folder')
    add_nodes(path, root_id)

    output_path = path / f"{output_name}.png"
    graph.render(filename=output_name, directory=path, cleanup=True)
    console.print(f'[green] Flowchart has been saved to {output_name}')