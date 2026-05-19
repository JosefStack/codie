
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
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file. Use this before editing any file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path" : {
                        "type": "stirng",
                        "description": "Path to the file, relative to CWD."
                    },
                    "start_line": {
                        "type": "integer",
                        "description": "Line to start reading from. Defaults to 1."
                    },
                    "end_line": {
                        "type": "integer",
                        "description": "Line to stop reading at. Defaults to 200."
                    },
                },
                "required": ["path"]
            }
        }
    }, 

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
                "required": []
            }
        }
    }, 

]