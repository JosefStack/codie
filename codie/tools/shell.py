import subprocess
import shutil
import os

ALWAYS_ALLOW = [
    "ls", "cat", "pwd", "echo", "tree", "head", "tail", "wc", "which",
    "git status", "git log", "git diff", "git branch", "git show",
    "python --version", "node --version", "npm --version", "pip list",
]

ALWAYS_CONFIRM = [
    "rm -rf", "rm -f", "--force", "git push --force", "git reset --hard",
    "git clean", "mkfs", "dd ", "> /dev/",
]

PIPES_AND_REDIRECTS = ["|", ">>", "&&", "||"]

def is_read_only(cmd: str) -> bool:
    cmd_lower = cmd.strip().lower()
    for pattern in ALWAYS_ALLOW:
        if cmd_lower.startswith(pattern):
            return True
    return False

def is_destructive(cmd: str) -> bool:
    cmd_lower = cmd.strip().lower()
    for pattern in ALWAYS_CONFIRM:
        if pattern in cmd_lower:
            return True
    for pattern in PIPES_AND_REDIRECTS:
        if pattern in cmd_lower:
            return True
    return False

def confirm(cmd: str) -> bool:
    try:
        answer = input(f"\n[codie] run: {cmd.strip().lower()}\nAllow? [y/n]: ").strip().lower()
        return answer == "y"
    except KeyboardInterrupt:
        return False
    
def run_command(cmd: str, mode: str = "review") -> str:
    if not cmd.strip():
        return "Error: no command provided."

    if is_destructive(cmd):
        if not confirm(cmd):
            return "Command cancelled by user."
        
    elif is_read_only(cmd):
        pass

    else:
        if mode == "review":
            if not confirm(cmd):
                return "Command cancelled by user."
        elif mode == "plan":
            if not confirm(cmd):
                return "Command cancelled by user."
    
    try:
        result = subprocess.run(
            cmd, 
            shell=True,
            capture_output=True,
            text=True,
            cwd=os.getcwd(),
            timeout=30,
        )

        output = result.stdout
        if result.stderr:
            output += f"\nstderr: {result.stderr}"

        if not output.strip():
            return "Command ran successfully with no output."

        lines = output.strip().splitlines()
        if len(lines) > 200:
            lines = lines[:200]
            output = "\n".join(lines) + "\n... (truncated)"

        return output

    except subprocess.TimeoutExpired:
        return "Error: command timed out after 30 seconds."
    except Exception as e:
        return f"Error running command: {str(e)}"