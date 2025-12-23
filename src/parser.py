import os 

def get_all_code(project_path, extensions):
    all_code = ""
    for root, _, files in os.walk(project_path):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        all_code += f"\n# File: {file_path}\n"
                        all_code += f.read() + "\n"
                except (UnicodeDecodeError, OSError):
                    # Пропускаем файлы, которые не удалось прочитать
                    continue
    return all_code

#a = get_all_code(project_path="./src", extensions=[".py"])
#print(a)