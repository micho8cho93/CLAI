from pathlib import Path
import json

def json_project_dict(path: Path, max_depth: int = None, depth: int = 0) -> dict:
    if max_depth is not None and depth > max_depth:
        return {}   
    
    structure = {}
    for entry in sorted(path.iterdir()):
        if entry.name.startswith('.' or '..'): #skip hidden files/folders
            continue
        if entry.is_dir():
            structure[entry.name] = json_project_dict(entry, max_depth, depth + 1)
        else:
            structure[entry.name] = None
    return structure


def export_as_json(output_path: Path, root_path: Path = Path.cwd(), max_depth: int = None):
    structure = json_project_dict(root_path, max_depth=max_depth)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(structure, f, indent=2)