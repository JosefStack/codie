import os

def read_file(path: str, start_line: int = 1, end_line: int = 200) -> str:
    full_path = os.path.join(os.getcwd(), path)

    if not os.path.exists(full_path):
        return f"Error: file '{path} not found."
    
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        selected = lines[start_line - 1 : end_line]

        if not selected:
            return f"Error: File range {start_line}-{end_line} is out of bounds. File has {len(lines)} lines."
        
        result = ""
        for i, line in enumerate(selected, start=start_line):
            results += f"Line {i}: {line}"
        
        return result

    except Exception as e:
        return f"Error reading file: {str(e)}"


def write_file(path: str, content: str) -> str:
    full_path = os.path.join(os.getcwd(), path)

    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f"Written to '{path}."


    except Exception as e:
        return f"Error writing file: {str(e)}"
    

def edit_file(path: str, old: str, new: str) -> str:
    full_path = os.path.join(os.getcwd(), path)

    if not os.path.exists(full_path):
        return f"Error: file '{path}' not found."

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        count = content.count(old)
        
        if count == 0:
            return f"Error: string not found in '{path}'."
        
        if count > 1:
            return f"Error: string appears {count} times in '{path}'. Make it more specific."
        
        new_content = content.replace(old, new)
        
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        
        return f"Edited '{path}'."

    except Exception as e:
        return f"Error editing file: {str(e)}"
    

def list_files(path: str = None) -> str:
    full_path = os.path.join(os.getcwd(), path) if path else os.getcwd()
    
    if not os.path.exists(full_path):
        return f"Error: path '{path}' not found."
    
    try: 
        result = ""
        for entry in sorted(os.scandir(full_path), key= lambda e: (not e.is_dir(), e.name)):
            if entry.is_dir():
                result += f"📁 {entry.name}/\n"
            else:
                result += f"📄 {entry.name}\n"
        
        return result if result else "Empty directory."
        
    except Exception as e:
        return f"Error listing files: {str(e)}"

