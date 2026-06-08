import os
from codie.tools.memory.utils import CODIE_DIR, AGENT_MD, MAX_LINES
from codie.tools.memory.utils import get_memory_path, read_memory as _read_memory, get_memory_length, check_memory_overflow

def write_memory(content: str) -> str:
    memory_too_long = check_memory_overflow(content)
    if memory_too_long:
        return memory_too_long
    
    os.makedirs(os.path.join(os.getcwd(), CODIE_DIR), exist_ok=True)
    with open(get_memory_path(), "w", encoding="utf-8") as f:
        f.write(content)
    
    return f"Memory written. ({get_memory_length()} lines)"

def append_memory(content: str) -> str:
    existing = read_memory()    
    new_content = existing.strip() + f"\n{content.strip()}\n"


    memory_too_long = check_memory_overflow(new_content)
    if memory_too_long:
        return memory_too_long

    os.makedirs(os.path.join(os.getcwd(), CODIE_DIR), exist_ok=True)
    with open(get_memory_path(), "w", encoding="utf-8") as f:
        f.write(f"\n{new_content.strip()}\n")

    return f"Memory appended. ({get_memory_length()} lines)"    

def read_memory(**kwargs) -> str:
    return _read_memory()