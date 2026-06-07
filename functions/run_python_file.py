import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(absolute_path, file_path))

        if os.path.commonpath([absolute_path, target_path]) != absolute_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
            
        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path]

        if args:
            command.extend(args)
        
        result = subprocess.run(
        command,
        cwd=absolute_path,
        capture_output=True,
        text=True,
        timeout=30,
        )

        output = []

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        
        if not result.stdout and not result.stderr:
            output.append(f'No output produced')

        if result.stdout:
            output.append(f'STDOUT:\n{result.stdout}')

        if result.stderr:
            output.append(f'STDERR:\n{result.stderr}')

        return "\n".join(output)
    
    except Exception as e:
        return f"Error: executing Python file: {e}"