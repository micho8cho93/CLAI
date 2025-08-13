from pathlib import Path
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
import json

def run_llm(structure_path: Path):
    """
    Run LLM analysis on the project structure
    """
    llm = ChatOllama(
        model="llama3.2",
        temperature=0
    )
    
    # Load the structure file
    with structure_path.open("r", encoding="utf-8") as f:
        structure = json.load(f)

    # Create messages using LangChain message types
    messages = [
        SystemMessage(content="You are a helpful assistant analyzing project structures."),
        HumanMessage(content=f"Analyze the following project structure JSON:\n{json.dumps(structure, indent=2)}"
                    "\n\nPlease provide:\n1. A brief summary of what the project might be.\n2. A list of main components.\n3. Any concerns or unusual patterns.")
    ]

    # Invoke the model and return the content
    response = llm.invoke(messages)
    return response.content