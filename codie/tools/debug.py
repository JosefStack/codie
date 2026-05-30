from codie.tools.shell import run_command

def run_debug(stack: str, lint_commands: str, test_commands: str = None) -> str:
    results = []

    # lint
    cmds = [cmd.strip() for cmd in lint_commands.split(",")]    
    for cmd in cmds:
        output = run_command(cmd, mode="auto")
        has_error = any(word in output.lower() for word in ["error", "fail", "traceback", "not found"])

        if has_error:
            results.append(f"✗ {cmd} failed:\n{output}")
        else:
            results.append(f"✓ {cmd} passed")

    # tests
    if not test_commands:
        results.append("⚠ No test commands provided. Skipping tests.")
    else:
        cmds = [c.strip() for c in test_commands.split(",")]
        for cmd in cmds:
            output = run_command(cmd, mode="auto")
            has_error = any(word in output.lower() for word in ["error", "failed", "failure"])
            if has_error:
                results.append(f"✗ {cmd} failed:\n{output}")
            else:
                results.append(f"✓ {cmd} passed")
    
    return "\n".join(results)