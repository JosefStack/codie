import typer
from typing import Optional
from codie import __version__

app = typer.Typer(add_completion=False)

def version_callback(value: bool):
    if value:
        typer.echo(f"codie v{__version__}")
        raise typer.Exit()

@app.command()
def main(
    mode: str = typer.Option("review", "--mode", "-m", help="Agent mode: plan, review, auto"), 
    version: Optional[bool] = typer.Option(None, "--version", "-v", callback=version_callback, is_eager=True, help="Show version and exit"),
):
    """Start the Codie coding agent in the current directory."""
    typer.echo("Codie is running!")

    from codie.session import start_session
    start_session(mode, __version__)