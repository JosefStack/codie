import os
import tomllib
import tomli_w
from pathlib import Path
from rich.console import Console

console = Console()

CODIE_HOME = Path.home() / ".codie"
CONFIG_PATH = CODIE_HOME / "config.toml"

def config_exists() -> bool:
    return CONFIG_PATH.exists()

def load_config() -> None:
    if not config_exists():
        return False
    
    with open(CONFIG_PATH, "rb") as f:
        config = tomllib.load(f)
    
    keys = config.get("api_keys", {})
    if keys.get("GROQ"):
        os.environ["GROQ_API_KEY"] = keys["GROQ"]
    else: 
        return False
    
    if keys.get("tavily"):
        os.environ["TAVILY_API_KEY"] = keys["tavily"]   
    if keys.get("jina"):
        os.environ["JINA_API_KEY"] = keys["jina"]
    
    settings = config.get("settings", {})
    if settings.get("model"):
        os.environ["CODIE_MODEL"] = settings["model"]

    return True

def save_config(groq: str, model: str, tavily: str, jina: str , mode: str) -> None:
    CODIE_HOME.mkdir(exist_ok=True)
    
    config = {
        "api_keys": {
            "GROQ": groq,
            "tavily": tavily,
            "jina": jina,
        },
        "settings": {
            "model": model,
            "default_mode": mode,
        }
    }

    with open(CONFIG_PATH, "wb") as f:
        tomli_w.dump(config, f)

def configure(force: bool = False) -> str:
    configured = load_config()
    if configured and not force:
        console.print(f"[dim]Config loaded from {CONFIG_PATH}[/dim]\n")
        config = tomllib.load(open(CONFIG_PATH, "rb"))
        return config.get("settings", {}).get("default_mode", "review")
    
    console.print("\n[bold cyan]Welcome to Codie![/bold cyan] Let's get you set up.\n")
    
    groq = input("GROQ API key (groq.com): ").strip()
    tavily = input("Tavily API key (tavily.com): ").strip()
    jina = input("Jina API key (jina.ai, optional): ").strip()
    mode = input("Default mode [review/auto/plan] (enter for review): ").strip() or "review"
    
    if mode not in ("review", "auto", "plan"):
        mode = "review"

    console.print("\n[bold]Available models:[/bold]")
    console.print("  1. [cyan][bold]GPT OSS 120B[/bold][/cyan] [dim](openai/gpt-oss-120b)[/dim]")
    console.print("  2. [cyan][bold]GPT OSS 20B[/bold][/cyan] [dim](openai/gpt-oss-20b)[/dim]")
    console.print("  3. [cyan][bold]Llama 4 Scout[/bold][/cyan] [dim](meta-llama/llama-4-scout-17b-16e-instruct)[/dim]")
    console.print("  4. [cyan][bold]Qwen 3 32B[/bold][/cyan] [dim](qwen/qwen3-32b)[/dim]")

    choice = input("Choose model [1-4] (default: 1): ").strip() or "1"
    models = {
        "1": "openai/gpt-oss-120b",
        "2": "openai/gpt-oss-20b",
        "3": "meta-llama/llama-4-scout-17b-16e-instruct",
        "4": "qwen/qwen3-32b",
    }
    model = models.get(choice, "openai/gpt-oss-120b")
    
    save_config(groq, model, tavily, jina, mode)
    load_config()  # Load the config to set environment variables immediately
    console.print(f"\n[green]Config saved to {CONFIG_PATH}[/green]\n")
    
    return mode