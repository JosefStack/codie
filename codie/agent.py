import json

from rich.console import Console

from codie.llm import get_completion, stream_response
from codie.tools.registry import TOOLS
from codie.tools.files import read_file, write_file, edit_file, delete_file, list_files
from codie.tools.search import search_code


console = Console()

MAX_ITERATIONS = 25

TOOL_MAP = {
    "read_file": read_file,
    "write_file": write_file,
    "edit_file": edit_file,
    "delete_file": delete_file,
    "list_files": list_files,
    "search_code": search_code
}

def run_agent(messages: list) -> str:
    iterations = 0

    while iterations < MAX_ITERATIONS:
        iterations += 1

        with console.status("[dim]thinking...[/dim]", spinner="dots"):
            response = get_completion(messages=messages, tools=TOOLS)

        if not response:
            return "Agent terminated due to error"
        message = response.choices[0].message

        if not message.tool_calls:
            streamed_response = stream_response(messages)
            messages.append({
                "role": "assistant",
                "content": streamed_response,
            })
            
            return streamed_response

        messages.append(message)

        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            if tool_name in TOOL_MAP:
                console.print(f"[dim]  ⚙ Tool call: {tool_name}[/dim]")
                with console.status(f"[dim]running...[/dim]", spinner="dots"):
                    result = TOOL_MAP[tool_name](**tool_args)
                console.print(f"[dim]  ✓ done[/dim]")
            else:
                result = f"Error: unknown tool '{tool_name}'."

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })

    return "Error: max iterations reached."
