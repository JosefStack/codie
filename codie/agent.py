import json

from rich.console import Console

from codie.llm import get_completion, stream_response
from codie.tools.registry import TOOLS
from codie.tools.files import read_file, write_file, edit_file, delete_file, list_files
from codie.tools.search import search_code
from codie.tools.shell import run_command
from codie.tools.web import web_search, crawl_url
from codie.tools.debug import run_debug


console = Console()

MAX_ITERATIONS = 25

TOOL_MAP = {
    "read_file": read_file,
    "write_file": write_file,
    "edit_file": edit_file,
    "delete_file": delete_file,
    "list_files": list_files,
    "search_code": search_code,
    "run_command": run_command,
    "web_search": web_search,
    "crawl_url": crawl_url,
    "run_debug": run_debug,
}

def run_agent(messages: list, mode: str) -> str:
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

        messages.append(
            {
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id" : tc.id,
                        "type": tc.type,
                        "function": {
                            "name" : tc.function.name,
                            "arguments": tc.function.arguments,
                        }
                    } for tc in message.tool_calls
                ]
            }
        )

        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            if tool_name in TOOL_MAP:
                console.print(f"[dim]  ⚙ Tool call: {tool_name}[/dim]")

                if tool_name == "delete_file":
                    result = delete_file(path=tool_args["path"], mode=mode)
                elif tool_name == "run_command":
                    result = run_command(cmd=tool_args["cmd"], mode=mode)
                else:
                    with console.status("[dim]running...[/dim]", spinner="dots"):
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
