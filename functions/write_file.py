import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a specified Python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the working directory",              
            ),
            "content": types.Schema(
                type=types.Type.STRING,                
                description="The text content to write to the file",
            )
        }, 
        required=["file_path", "content"]
    ),
)

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(absolute_path, file_path))

        if os.path.commonpath([absolute_path, target_path]) != absolute_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        with open(target_path, "w") as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'