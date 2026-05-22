import shutil   
import subprocess
import os


def search_code(pattern: str, file_type: str = None, path: str = None, max_results: int = 50) -> str:
    if not shutil.which("rg"):
        return f"Error: ripgrep not installed. Run `pip install ripgrep`."
    
    cmd = ["rg", pattern, "--line-number", "--no-heading"]

    if file_type:
        cmd += ["--type", file_type]

    if max_results:
        cmd += ["--max-count", str(max_results)]

    search_path = os.path.join(os.getcwd(), path) if path else os.getcwd()
    cmd.append(search_path)

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 1:
        return f"No matches found for {pattern}"
    
    if result.returncode != 0:
        return f"Error: {result.stderr}"
    
    return result.stdout

