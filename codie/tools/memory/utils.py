import os

CODIE_DIR = ".codie"
AGENT_MD = ".codie/AGENT.md"
MAX_LINES = 200

def get_memory_path() -> str:
    return os.path.join(os.getcwd(), AGENT_MD)

def memory_exists() -> bool:
    return os.path.exists(get_memory_path())

def read_memory() -> str:
    if not memory_exists():
        return ""
    with open(get_memory_path(), "r", encoding="utf-8") as f:
        return f.read()

def get_memory_length() -> int:   
    content = read_memory()
    return len(content.strip().split("\n"))

def check_memory_overflow(content) -> str:
    if len(content.strip().split("\n")) > MAX_LINES:
        return f"Error: Memory exceeds maximum length of {MAX_LINES} lines. Current length is {get_memory_length()} lines."
    else: 
        return ""

