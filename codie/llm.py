import os 
import time
from dotenv import load_dotenv
from openai import OpenAI

from rich.console import Console
from rich.markdown import Markdown

from codie.utils.tokens import TokenTracker

load_dotenv()
console = Console()

client = OpenAI(
    api_key=os.environ.get("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1",
)

MODEL = "openai/gpt-oss-120b"

def stream_response(messages: list, token_tracker: TokenTracker) -> str:
    full_response = ""

    with console.status("[dim]thinking...[/dim]", spinner="dots"):
        # not streaming to enable markdown rendering in the terminal. Will have to add real-time markdown parsing for streaming + mardown rendering.
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            # stream=True,
            tool_choice="auto",

        )
        token_tracker.add(response.usage)
            
    # console.print("[bold cyan]Codie:[/bold cyan] ", end="")

    # for chunk in stream:
    #     content = chunk.choices[0].delta.content
    #     if content:
    #         console.print(content, end="")
    #         full_response += content

    # console.print()

    full_response = response.choices[0].message.content
    console.print("[bold cyan]Codie:[/bold cyan]")
    console.print(Markdown(full_response))
    return full_response


def get_completion(messages: list, tools: list, token_tracker: TokenTracker) -> object:
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=tools,
                tool_choice="auto",
            )
            token_tracker.add(response.usage)
            
            return response
        
        except Exception as e:
            if "rate_limit" in str(e).lower():
                if attempt < 2:
                    console.print("\n[red]Rate limit reached. Try again in a moment.[/red]")
                    time.sleep(10)
                elif attempt == 2:
                    console.print("\n[red]Rate limit reached. Try again after limit resets.[/red]")
                    return None
            else:
                console.print(f"\n[red]Something went wrong: {str(e)}[/red]")
                return None