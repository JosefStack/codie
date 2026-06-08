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
    if keys.get("groq"):
        os.environ["GROQ_API_KEY"] = keys["groq"]
    else: 
        return False
    
    if keys.get("tavily"):
        os.environ["TAVILY_API_KEY"] = keys["tavily"]   
    if keys.get("jina"):
        os.environ["JINA_API_KEY"] = keys["jina"]

    return True

def save_config(groq: str, tavily: str, jina: str , mode: str) -> None:
    CODIE_HOME.mkdir(exist_ok=True)
    
    config = {
        "api_keys": {
            "groq": groq,
            "tavily": tavily,
            "jina": jina,
        },
        "settings": {
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
    
    groq = input("Groq API key (console.groq.com): ").strip()
    tavily = input("Tavily API key (tavily.com): ").strip()
    jina = input("Jina API key (jina.ai, optional): ").strip()
    mode = input("Default mode [review/auto/plan] (enter for review): ").strip() or "review"
    
    if mode not in ("review", "auto", "plan"):
        mode = "review"
    
    save_config(groq, tavily, jina, mode)
    console.print(f"\n[green]Config saved to {CONFIG_PATH}[/green]\n")
    
    return mode