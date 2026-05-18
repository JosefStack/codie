import os 
from dotenv import load_dotenv
from openai import OpenAI

from rich.console import Console


load_dotenv()
console = Console()

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

MODEL = "openai/gpt-oss-120b"

def stream_response(messages: list) -> str:
    full_response = ""

    with console.status("[dim]thinking...[/dim]", spinner="dots"):
        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True,
        )

        first_chunk = next(iter(stream))
    
    console.print("[bold cyan]Codie:[/bold cyan] ", end="")

    first_chunk_content = first_chunk.choices[0].delta.content
    if first_chunk_content:
        # print would work, but using console.print() for consistency
        console.print(first_chunk_content, end="")
        full_response += first_chunk_content
    
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            console.print(content, end="")
            full_response += content
        
    console.print()
    return full_response