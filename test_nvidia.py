import os 
import time
from dotenv import load_dotenv
from openai import OpenAI

from rich.console import Console
from rich.markdown import Markdown

from codie.utils.tokens import TokenTracker

MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

load_dotenv()
console = Console()

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

def stream_response() -> str:
    full_response = ""

    # with console.status("[dim]thinking...[/dim]", spinner="dots"):
        # not streaming to enable markdown rendering in the terminal. Will have to add real-time markdown parsing for streaming + mardown rendering.
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role":"user","content":"hi"}],
        # stream=True,
        tool_choice="auto",
        temperature=1,
        top_p=0.95,
        stream=False

    )
            
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



stream_response()