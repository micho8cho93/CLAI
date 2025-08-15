import typer
import time
from pathlib import Path
from typing import Optional
from watchdog.observers import Observer
from core.update_monitor import CodebaseMonitor, LLMAnalyzer


app = typer.Typer(help="Generate summaries of the codebase")

@app.command("monitor")
def start_monitoring(
    path: Path = typer.Option(".", help="Path to monitor (default: current directory)"),
    model: str = typer.Option("llama3.2", help="LLM model to use"),
    ignore: Optional[str] = typer.Option(None, help="Comma-separated patterns to ignore"),
    debounce: Optional[float] = typer.Option(2.0, help="Seconds to wait before analyzing changes"),
):
    """
    Start monitoring the codebase for changes and analyze them with LLM.
    """
    if not path.exists():
        typer.echo(f"Error: Path {path} does not exist.", err=True)
        raise typer.Exit(1)
    
    # Parse ignore patterns
    ignore_patterns = set()
    if ignore:
        ignore_patterns.update(pattern.strip() for pattern in ignore.split(','))
    
    typer.echo(f"🚀 Starting codebase monitoring...")
    typer.echo(f"📁 Monitoring path: {path.absolute()}")
    typer.echo(f"🤖 Using model: {model}")
    typer.echo(f"⏱️  Debounce time: {debounce}s")
    typer.echo(f"🚫 Ignoring: {ignore_patterns}")
    typer.echo("\n⚠️  Press Ctrl+C to stop monitoring\n")
    
    try:
        # Initialize components
        analyzer = LLMAnalyzer(model_name=model)
        event_handler = CodebaseMonitor(
            llm_analyzer=analyzer,
            ignore_patterns=ignore_patterns,
            debounce_seconds=debounce
        )
        
        # Set up file system observer
        observer = Observer()
        observer.schedule(event_handler, str(path), recursive=True)
        observer.start()
        
        typer.echo("✅ Monitoring started! Waiting for file changes...")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            typer.echo("\n🛑 Stopping monitor...")
            observer.stop()
        
        observer.join()
        typer.echo("✅ Monitor stopped successfully.")
        
    except Exception as e:
        typer.echo(f"❌ Error starting monitor: {str(e)}", err=True)
        raise typer.Exit(1)

if __name__ == "__main__":
    app()