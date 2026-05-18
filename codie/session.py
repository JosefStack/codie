import os

from rich.console import Console
from codie.llm import stream_response

from codie.prompts import SYSTEM_PROMPT

console = Console()

SLASH_COMMANDS = {
    "/exit": "Exit Codie", 
    "/quit": "Exit Codie",
    "/help": "Show available commands",
    "/mode": "Show or change mode",
    "/clear": "Clear the screen",
    "/cost": "Show token usage and cost",
}

def handle_slash_commands(user_input: str, mode: str) -> str:
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
        console.print("[dim]No usage tracked yet.[/dim]")

    else:
        console.print(f"[red]Unknown command '{command}'. Type /help for available commands.[/red]")

    return mode


def start_session(mode: str, version: str):
    console.print(f"\n[bold cyan]Codie[/bold cyan] [dim]v{version} - {mode}[/dim]")
    console.print("[dim]Type /help for commands, /exit to quit.[/dim]\n")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT + f"\nCWD: {os.getcwd()}"}
    ]

    while True:
        try:
            user_input = input("→ ").strip()

            if not user_input:
                continue

            if user_input.startswith("/"):
                mode = handle_slash_commands(user_input, mode)
                continue
                
            messages.append({
                "role": "user", 
                "content": user_input
            })

            response = stream_response(messages=messages)
            messages.append({
                "role": "assistant",
                "content": response
            })

        except KeyboardInterrupt:
            console.print()
            console.print("\n[dim]Goodbye.[/dim]\n")
            break