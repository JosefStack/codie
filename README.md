# Codie

An AI-powered CLI coding agent. Reads, writes, and debugs your code. Like Claude Code, but yours.

```
→ create a REST API with FastAPI and add tests
  ⚙ Tool call: write_file
  ⚙ Tool call: write_file
  ⚙ Tool call: run_command
  ⚙ Tool call: run_debug
Codie: Done. API is running on port 8000, all tests passing.
```

## Features

- **File tools** — read, write, edit, delete files in your project
- **Shell access** — run commands with mode-aware confirmation
- **Code search** — ripgrep-powered search across your codebase
- **Web tools** — search the web and read documentation
- **Debug loop** — automatically runs lint and tests after writing code
- **Project memory** — remembers your stack, conventions, and key files across sessions
- **Token tracking** — see exactly how much each session costs

## Requirements

- Python 3.10+
- A [Groq API key](https://console.groq.com) (free)
- A [Tavily API key](https://tavily.com) (free, 1000 searches/month)
- A [Jina API key](https://jina.ai) (free, 500 RPM)

## Installation

```bash
pip install codie-cli
```

On first run, Codie will walk you through setting up your API keys:

```bash
codie

Welcome to Codie! Let's get you set up.

Groq API key (console.groq.com): ...
Tavily API key (tavily.com): ...
Jina API key (jina.ai, optional): ...
Default mode [review/auto/plan] (enter for review):

Config saved to ~/.codie/config.toml
```

## Usage

```bash
codie                  # start in review mode (default)
codie --mode auto      # start in auto mode
codie --mode plan      # start in plan mode
codie --version        # show version
codie --configure      # update API keys and settings
```

### Modes

| Mode | Behavior |
|------|----------|
| `review` | Confirms each file edit and mutating shell command |
| `auto` | Runs everything without asking (still confirms destructive commands) |
| `plan` | Shows full plan first, user approves once, then executes |

### Slash Commands

| Command | Description |
|---------|-------------|
| `/help` | Show available commands |
| `/mode <mode>` | Change mode mid-session |
| `/cost` | Show token usage and cost for this session |
| `/remember <thing>` | Save something to project memory |
| `/clear` | Clear the screen |
| `/exit` | Exit Codie |

### Project Memory

Codie can maintain a `.codie/AGENT.md` file in your project root. It stores your stack, conventions, important files, and notes — and injects them into every session so you never have to re-explain your project.

```bash
codie
# Setup project memory? [y/n]: y
# Project memory created at .codie/AGENT.md
```

Add `.codie/AGENT.md` to git to share context with your team. Add `.codie/sessions/` to `.gitignore`.

## Configuration

Config is stored at `~/.codie/config.toml`. Run `codie --configure` to update it.

You can also use environment variables:

```bash
export GROQ_API_KEY=...
export TAVILY_API_KEY=...
export JINA_API_KEY=...
```

## License

MIT