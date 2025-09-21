import typer
import time
from pathlib import Path
from typing import Set, Iterator
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from core.llm import run_llm

class CodebaseMonitor(FileSystemEventHandler):
    def __init__(self, llm_analyzer, ignore_patterns: Set[str] = None, debounce_seconds: float = 2.0):
        self.llm_analyzer = llm_analyzer
        self.ignore_patterns = ignore_patterns or {
            '.git', '__pycache__', '.pyc', '.log', '.tmp', 
            'node_modules', '.env', '.DS_Store', '.vscode', '.idea'
        }
        self.debounce_seconds = debounce_seconds
        self.pending_changes = {}
        self.last_analysis = {}
        
    def should_ignore(self, file_path: str) -> bool:
        """Check if file should be ignored based on patterns"""
        path_obj = Path(file_path)
        
        # Ignore directories and files matching patterns
        for pattern in self.ignore_patterns:
            if pattern in str(path_obj) or path_obj.suffix == pattern:
                return True
                
        # Only monitor code files
        code_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h', 
                        '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala', 
                        '.sql', '.yaml', '.yml', '.json', '.xml', '.html', '.css', '.scss'}
        
        return path_obj.suffix.lower() not in code_extensions
    
    def on_modified(self, event):
        if event.is_directory:
            return
            
        if self.should_ignore(event.src_path):
            return
            
        self.handle_file_change(event.src_path, "modified")
    
    def on_created(self, event):
        if event.is_directory:
            return
            
        if self.should_ignore(event.src_path):
            return
            
        self.handle_file_change(event.src_path, "created")
    
    def handle_file_change(self, file_path: str, change_type: str):
        """Handle file changes with debouncing"""
        current_time = time.time()
        
        # Debounce rapid changes to same file
        if file_path in self.pending_changes:
            if current_time - self.pending_changes[file_path]['time'] < self.debounce_seconds:
                self.pending_changes[file_path]['time'] = current_time
                return
        
        self.pending_changes[file_path] = {
            'time': current_time,
            'type': change_type
        }
        
        # Schedule analysis after debounce period
        typer.echo(f"📝 Detected {change_type}: {file_path}")
        
        # Simple debounce - in production, you might want a more sophisticated approach
        time.sleep(self.debounce_seconds)
        
        # Check if this is still the latest change
        if (file_path in self.pending_changes and 
            current_time >= self.pending_changes[file_path]['time'] - 0.1):  # Small tolerance
            
            self.analyze_change(file_path, change_type)
            del self.pending_changes[file_path]
    
    def analyze_change(self, file_path: str, change_type: str):
        """Analyze the changed file with LLM"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            typer.echo(f"\n🔍 [{timestamp}] Analyzing {change_type} file: {Path(file_path).name}")
            
            # Get file content and analyze
            analysis = self.llm_analyzer.analyze_file_change(file_path, change_type)
            
            typer.echo("📊 Analysis Result:")
            typer.echo("-" * 50)
            full_response = ""
            for chunk in analysis:
                typer.echo(chunk, nl=False)
                full_response += chunk
            typer.echo()  # for the final newline
            typer.echo("-" * 50)
            typer.echo("✅ Monitoring continues...\n")
            
        except Exception as e:
            typer.echo(f"❌ Error analyzing {file_path}: {str(e)}")

class LLMAnalyzer:
    def __init__(self, model_name: str = "llama3.2"):
        from core.llm import ChatOllama
        from langchain_core.messages import HumanMessage, SystemMessage
        
        self.llm = ChatOllama(model=model_name, temperature=0.1)
        self.SystemMessage = SystemMessage
        self.HumanMessage = HumanMessage
        
    def analyze_file_change(self, file_path: str, change_type: str) -> Iterator[str]:
        """Analyze a specific file change"""
        try:
            # Read file content
            path_obj = Path(file_path)
            if not path_obj.exists():
                yield f"File {file_path} no longer exists."
                return
                
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Limit content size to avoid token limits
            if len(content) > 4000:
                content = content[:4000] + "\n... (truncated)"
            
            messages = [
                self.SystemMessage(content="""You are a code analysis assistant monitoring a codebase. 
                Analyze file changes and provide concise insights about:
                1. What changed or was added
                2. Potential impact on the codebase
                3. Any concerns or suggestions
                Keep responses brief but informative."""),
                
                self.HumanMessage(content=f"""A file was {change_type}:
                File: {path_obj.name}
                Path: {file_path}
                
                Content:
                {content}
                
                Please analyze this change and provide insights.""")
            ]
            
            response = self.llm.stream(messages)
            for chunk in response:
                yield chunk.content
            
            
        except Exception as e:
            yield f"Error analyzing file: {str(e)}"