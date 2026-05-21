
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


]