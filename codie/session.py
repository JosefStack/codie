import os

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from codie.agent import run_agent

from codie.prompts import SYSTEM_PROMPT

from codie.tools.memory.utils import read_memory as _read_memory, memory_exists

from codie.tools.files import list_files
from codie.llm import get_completion
from codie.tools.memory.memory import write_memory

from codie.utils.tokens import TokenTracker

console = Console()

token_tracker = TokenTracker()


SLASH_COMMANDS = {
    "/exit": "Exit Codie", 
    "/quit": "Exit Codie",
    "/help": "Show available commands",
    "/mode": "Show or change mode",
    "/clear": "Clear the screen",
    "/cost": "Show token usage and cost",
    "/model": "Show or change model",
}

def handle_slash_commands(user_input: str, mode: str, token_tracker: TokenTracker) -> str:
    parts = user_input.strip().split()
    command = parts[0]
    args = parts[1:] if len(parts) > 1 else []

    if command in ("/exit", "/quit"):
        console.print("\n[dim]\nGoodbye.[/dim]\n")
        raise SystemExit(0)

    elif command == "/help":
        console.print("\n[bold]Commands:[/bold]")
        for cmd, desc in SLASH_COMMANDS.items():
            console.print(f"  [cyan]{cmd}[/cyan]  {desc}")
        console.print()

    elif command == "/clear":
        console.clear()

    elif command == "/mode":
        if args:
            new_mode = args[0]
            if new_mode not in ("plan", "review", "auto"):
                console.print(f"[red]Invalid mode '{new_mode}'. Choose from: plan, review, auto[/red]")
            else:
                mode = new_mode
                console.print(f"[green]Mode set to '{mode}'[/green]")
        else:
            console.print(f"[dim]Current mode: {mode}[/dim]")

    elif command == "/cost":
        console.print(f"\n[bold]Usage breakdown:[/bold]\n")
        console.print(token_tracker.cost())
        console.print()

    elif command == "/model":
        if args:
            valid_models = [
                "openai/gpt-oss-120b",
                "openai/gpt-oss-20b", 
                "meta-llama/llama-4-scout-17b-16e-instruct",
                "qwen/qwen3-32b",
            ]
            if args[0] not in valid_models:
                console.print(f"[red]Invalid model. Choose from: {', '.join(valid_models)}[/red]")
            else:
                os.environ["CODIE_MODEL"] = args[0]
                console.print(f"[green]Model changed to {args[0]}[/green]")
        else:
            console.print(f"[dim]Current model: [/dim][cyan]{os.environ.get('CODIE_MODEL')}[/cyan]")
    else:
        console.print(f"[red]Unknown command '{command}'. Type /help for available commands.[/red]")

    return mode

def setup_memory() -> None:
    console.print("[dim]Reading project files...[/dim]")
    file_tree = list_files()

    messages = [
        {
            "role": "system",
            "content": "Generate a concise AGENT.md for this project based on the file tree. Include sections: Stack, Commands, Important Files, Conventions, Notes for Agent. Keep it under 50 lines. Return only the markdown content, no explanation."
        },
        {
            "role": "user",
            "content": f"File tree:\n{file_tree}"
        }
    ]

    response = get_completion(messages, tools=[], token_tracker=token_tracker)
    content = response.choices[0].message.content
    write_memory(content)
    console.print("[green]Project memory created at .codie/AGENT.md[/green]")
    
    return content

ASCII_ART = """\
 ██████╗  ██████╗ ██████╗ ██╗███████╗
██╔════╝ ██╔═══██╗██╔══██╗██║██╔════╝
██║      ██║   ██║██║  ██║██║█████╗
██║      ██║   ██║██║  ██║██║██╔══╝
╚██████╗ ╚██████╔╝██████╔╝██║███████╗
 ╚═════╝  ╚═════╝ ╚═════╝ ╚═╝╚══════╝"""

def print_banner(version: str, mode: str) -> None:
    art = Text(ASCII_ART, style="bold cyan", justify="center")
    subtitle = Text(f"\nv{version}  ·  {mode} mode", style="dim", justify="center")
    hint = Text("Type /help for commands, /exit to quit", style="dim", justify="center")
    content = Text.assemble(art, subtitle, "\n", hint)
    panel = Panel(content, border_style="cyan", padding=(1, 4))
    console.print(Align.center(panel))
    console.print()

def start_session(mode: str, version: str):
    print_banner(version, mode)

    memory = ""
    memory_enabled = False

    if memory_exists():
        memory_enabled = True
        memory = _read_memory()
        console.print("[dim]Project memory loaded.[/dim]")
    else:
        answer = input("Setup project memory? [y/n]: ").strip().lower()
        if answer == "y":
            memory_enabled = True
            memory = setup_memory()
            console.print("[dim]Project memory enabled.[/dim]")
        else:
            console.print("[dim]Project memory disabled.[/dim]\n")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT + f"\nCWD: {os.getcwd()}" + (f"\n\n# Project Memory\n{memory}" if memory else "")}
    ]

    



    while True:
        try:
            user_input = input("→ ").strip()

            if not user_input:
                continue

            if user_input.startswith("/"):
                mode = handle_slash_commands(user_input, mode, token_tracker)
                continue
                
            messages.append({
                "role": "user", 
                "content": user_input
            })

            response = run_agent(messages=messages, mode=mode, memory_enabled=memory_enabled, token_tracker=token_tracker)
            messages.append({
                "role": "assistant",
                "content": response
            })

        except KeyboardInterrupt:
            console.print()
            console.print("\n[dim]Goodbye.[/dim]\n")
            break

        except Exception as e:
            error = str(e)
            console.print(f"\n[red]Error: {error}[/red]\n")
            # if "rate_limit" in error.lower():
            #     console.print("\n[red]Rate limit reached. Try again in a moment.[/red]")
            # elif "tool call validation" in error.lower():
            #     console.print("\n[red]Something went wrong with the agent. Try rephrasing.[/red]")
            # else:
            #     console.print("\n[red]Something went wrong. Try again.[/red]")
            continue
