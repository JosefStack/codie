
# -- tool format -- 
# {
#         "type": "function",
#         "function": {
#             "name": None,
#             "description": None,
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     None : {
#                         "type": None,
#                         "description": None
#                     },
#                 },
#                 "required": [None]
#             }
#         }
#     }, 

TOOLS = [
    # read_file
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file. Use this before editing any file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path" : {
                        "type": "string",
                        "description": "Path to the file, relative to CWD."
                    },
                    "line_start": {
                        "type": "integer",
                        "description": "Line to start reading from. Defaults to 1."
                    },
                    "line_end": {
                        "type": "integer",
                        "description": "Line to stop reading at. Parameter name is 'end_line'. Defaults to 200."
                    },
                },
                "required": ["path"]
            }
        }
    }, 

    # write_file for creating new files or writing full content of a file.
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write full content to a file. Use for creating new files only. For existing files, prefer edit_file unless the file is empty.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path" : {
                        "type": "string",
                        "description": "Path to the file, relative to CWD."
                    },
                    "content": {
                        "type": "string",
                        "description": "Full content to write to the file."
                    }
                },
                "required": ["path", "content"]
            }
        }
    }, 

    # edit_file for editing certain lines/content of a file
    {
        "type": "function",
        "function": {
            "name": "edit_file",
            "description": "Edit a file by replacing a specific string with a new string. The old string must be unique in the file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path" : {
                        "type": "string",
                        "description": "Path to the file, relative to CWD."
                    },
                    "old": {
                        "type": "string",
                        "description": "The exact string to replace. Must appear exactly once in the file."
                    },
                    "new": {
                        "type": "string",
                        "description": "The string to replace it with."
                    }
                },
                "required": ["path", "new", "old"]
            }
        }
    }, 

    # delete_file for deleting only files (doesn't delete folders, use shell for that)
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "Delete a file. Use with caution — this is irreversible.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the file, relative to CWD."
                    }
                },
                "required": ["path"]
            }
        }
    },

    # list_files for listing all files and folders in a directory
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files and directories at a given path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path" : {
                        "type": "string",
                        "description": "Directory path to list. Defaults to CWD."
                    },
                },
                # "required": []
            }
        }
    }, 

    # search_code using ripgrep
    {
        "type": "function",
        "function": {
            "name": "search_code",
            "description": "Search for a pattern or word across the codebase using ripgrep. Use this when it's needed to find out the file consisting a pattern or word. Use this before read_file to find which files are relevant.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern" : {
                        "type": "string",
                        "description": "The search pattern or regex."
                    },
                    "file_type": {
                        "type": "string",
                        "description": "Filter by file type e.g. 'py', 'js', 'ts'. Optional. Omit if not needed.",
                    },
                    "path": {
                        "type": "string",
                        "description": "Directory to search in. Defaults to CWD."
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return. Defaults to 50."
                    }
                },
                "required": ["pattern"]
            }
        }
    }, 

    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Run a shell command. Use for installing packages, running scripts, executing tests, checking git status etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cmd": {
                        "type": "string",
                        "description": "The shell command to run."
                    }
                },
                "required": ["cmd"]
            }
        }
    }, 

    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information, documentation, or answers. Use this when you need up-to-date information or can't find the answer in the codebase. The query can be a question or a string of keywords.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query" : {
                        "type": "string",
                        "description": "The search query, which can be a question or keywords."
                    },
                "max_results": {
                        "type": "integer",
                        "description": "Maximum number of search results to return. Defaults to 5."
                    }
                },
                "required": ["query"]
            }
        }
    }, 

    {
        "type": "function",
        "function": {
            "name": "crawl_url",
            "description": "Fetch and read the content of a URL. Use for reading documentation or web pages. Use web_search first to find relevant URLs, then use crawl_url to read their content. If user provides an URL, search it directly without needing web_search.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url" : {
                        "type": "string",
                        "description": "The URL to crawl. Must be the complete URL including https://"
                    },
                },
                "required": ["url"]
            }
        }
    }, 

    {
        "type": "function",
        "function": {
            "name": "run_debug",
            "description": "Run lint and tests to verify code works. Call this after completing any coding task. If no tests exist, write them first before calling this.",
            "parameters": {
                "type": "object",
                "properties": {
                    "stack" : {
                        "type": "string",
                        "description": "Detected stack: python, javascript, typescript, rust, go, etc."
                    },
                    "lint_commands": {
                        "type": "string",
                        "description": "Comma separated lint/typecheck commands e.g. 'ruff check .,mypy .'"
                    },
                    "test_commands": {
                        "type": "string",
                        "description": "Command to run tests e.g. 'pytest', 'npm test', 'cargo test'. Omit if no tests exist."
                    }
                },
                "required": ["stack", "lint_commands"]
            }
        }
    }, 

    {
        "type": "function",
        "function": {
            "name": "append_memory",
            "description": "Append important project information to memory. Use when you discover the stack, conventions, key files, commands, or important decisions. This persists across sessions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content" : {
                        "type": "string",
                        "description": "The information to save. Be concise — a few lines max."
                    },
                },
                "required": ["content"]
            }
        }
    }, 

    {
        "type": "function",
        "function": {
            "name": "write_memory",
            "description": "Overwrite the entire memory file. Use ONLY when memory exceeds 200 lines and needs to be compacted. Summarize the existing memory and write the condensed version.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content" : {
                        "type": "string",
                        "description": "The full compacted memory content. Must be under 200 lines."
                    },
                },
                "required": ["content"]
            }
        }
    }, 
    
    {
        "type": "function",
        "function": {
            "name": "read_memory",
            "description": "Read the current project memory from AGENT.md. Use this before writing or compacting memory to see what's already there.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
]