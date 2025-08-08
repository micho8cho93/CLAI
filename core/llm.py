from pathlib import Path
from llama_cpp import Llama
import json

def build_structure_prompt(structure_path: Path) -> str:
    with structure_path.open("r", encoding="utf-8") as f:
        structure = json.load(f)
    
    prompt = (
        "You are a codebase analysis assistant. Given the following project structure in JSON format, "
        "provide:\n\n"
        "1. A brief summary of what the project might be.\n"
        "2. A list of the main components (e.g., API, frontend, utilities).\n"
        "3. Any concerns or unusual patterns.\n\n"
        "Project Structure:\n"
        f"{json.dumps(structure, indent=2)}"
    )
    return prompt


def run_llm(prompt: str, model_path: str = "model.gguf"):
    llm = Llama(model_path=model_path)
    output = llm(prompt, max_tokens=512, stop=["\n\n"])
    return output["choices"][0]["text"]
