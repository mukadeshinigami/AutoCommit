import os 

_file_line_counts = {}

def check_file_has_new_lines(file_path):
    """
    Проверяет, появились ли новые строки в файле.
    Возвращает True, если появились новые строки, иначе False.
    """
    if not os.path.exists(file_path):
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            current_line_count = sum(1 for _ in f)
        
        # Если файл проверяется впервые, сохраняем текущее количество строк
        if file_path not in _file_line_counts:
            _file_line_counts[file_path] = current_line_count
            return True
        
        # Сравниваем с предыдущим количеством строк
        previous_line_count = _file_line_counts[file_path]
        if current_line_count > previous_line_count:
            _file_line_counts[file_path] = current_line_count
            return True
        
        return False
    except (UnicodeDecodeError, OSError):
        return False

def read_file_if_updated(project_path, extensions):
    """
    Читает файлы только если в них появились новые строки.
    Возвращает словарь {путь_к_файлу: содержимое} или пустой словарь, если новых строк нет.
    """
    updated_files = {}
    for root, _, files in os.walk(project_path):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                if check_file_has_new_lines(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            code = f.read()
                            updated_files[file_path] = code
                    except (UnicodeDecodeError, OSError) as e:
                        # Пропускаем файлы, которые не удалось прочитать
                        print(f"Ошибка при чтении файла {file_path}: {e}")
                        continue
    return updated_files


# Дополнительные строки для тестирования

a = read_file_if_updated(project_path="./src", extensions=[".py"])
if a:
    print(f"Найдено {len(a)} обновленных файлов:")
    for file_path, content in a.items():

        print(content)
else:
    print("Нет обновленных файлов")