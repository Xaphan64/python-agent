import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(absolute_path, directory))
        files_list = []

        if os.path.commonpath([absolute_path, target_path]) != absolute_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'
        for file in os.listdir(target_path):
            full_path = os.path.join(target_path, file)
            files_list.append(f'- {file}: file_size={os.path.getsize(full_path)} bytes, is_dir={os.path.isdir(full_path)}')
        return "\n".join(files_list)
    
    except Exception as e:
        return f'Error: {e}'