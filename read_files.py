def read_files(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content
