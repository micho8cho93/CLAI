import os
from pathlib import Path
from typing import List, Union

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

# Define included extensions and ignored directories/files
INCLUDED_EXTENSIONS = {
    ".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp", ".h",
    ".hpp", ".rs", ".go", ".php", ".rb", ".swift", ".kt", ".kts",
    ".scala", ".m", ".sh", ".pl", ".pm", ".r", ".lua", ".sql",
    ".json", ".xml", ".yaml", ".yml", ".md"
}
IGNORED_PATTERNS = {
    ".git", ".venv", "venv", "__pycache__", "node_modules", ".env",
    ".gitignore", "dist", "build"
}

def is_ignored(path: Path) -> bool:
    """Check if a path should be ignored."""
    return any(part in IGNORED_PATTERNS for part in path.parts)

def get_code_files(path: Union[str, Path]) -> List[Path]:
    """Get all code files from a path, filtering out ignored files."""
    path = Path(path)
    if path.is_file():
        if path.suffix in INCLUDED_EXTENSIONS and not is_ignored(path):
            return [path]
        return []

    files = []
    for root, _, filenames in os.walk(path):
        root_path = Path(root)
        if is_ignored(root_path):
            continue
        for filename in filenames:
            file_path = root_path / filename
            if file_path.suffix in INCLUDED_EXTENSIONS and not is_ignored(file_path):
                files.append(file_path)
    return files

def generate_markdown_docs(path: Union[str, Path]) -> str:
    """
    Generates markdown documentation for code files using an LLM.
    """
    code_files = get_code_files(path)
    if not code_files:
        return "No code files found to document."

    content = ""
    for file_path in code_files:
        try:
            with file_path.open("r", encoding="utf-8") as f:
                content += f"--- {file_path} ---\n{f.read()}\n\n"
        except Exception as e:
            content += f"--- {file_path} ---\nError reading file: {e}\n\n"

    llm = ChatOllama(model="llama3.2", temperature=0)

    messages = [
        SystemMessage(
            content="You are an expert technical writer. Your task is to generate "
                    "clear and concise markdown documentation for the provided source "
                    "code files. Analyze the code and produce documentation in a "
                    "technical documentation style. Focus on explaining the purpose "
                    "of the code, its components, and how they work together."
        ),
        HumanMessage(content=content),
    ]

    response = llm.invoke(messages)
    return response.content
