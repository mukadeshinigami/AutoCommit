import os 
import json

# Путь к файлу для сохранения состояния (в корне проекта)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_STATE_FILE = os.path.join(_PROJECT_ROOT, ".file_line_counts.json")

def _load_file_counts():
    """Загружает сохраненное состояние количества строк из файла."""
    if os.path.exists(_STATE_FILE):
        try:
            with open(_STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}

def _save_file_counts(file_counts):
    """Сохраняет состояние количества строк в файл."""
    try:
        with open(_STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(file_counts, f, indent=2)
    except OSError as e:
        print(f"Ошибка при сохранении состояния в {_STATE_FILE}: {e}")

_file_line_counts = _load_file_counts()

def check_file_has_new_lines(file_path):
    """
    Проверяет, появились ли новые строки в файле.
    Возвращает True, если появились новые строки, иначе False.
    """
    # Преобразуем путь в абсолютный
    file_path = os.path.abspath(file_path)
    
    if not os.path.exists(file_path):
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            current_line_count = sum(1 for _ in f)
        
        # Если файл проверяется впервые, сохраняем текущее количество строк
        if file_path not in _file_line_counts:
            _file_line_counts[file_path] = current_line_count
            return False  # При первом запуске не считаем файл обновленным
        
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
    # Преобразуем project_path в абсолютный путь
    project_path = os.path.abspath(project_path)
    
    for root, _, files in os.walk(project_path):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.abspath(os.path.join(root, file))
                if check_file_has_new_lines(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            code = f.read()
                            updated_files[file_path] = code
                    except (UnicodeDecodeError, OSError) as e:
                        # Пропускаем файлы, которые не удалось прочитать
                        print(f"Ошибка при чтении файла {file_path}: {e}")
                        continue
    
    # Сохраняем состояние после проверки всех файлов
    _save_file_counts(_file_line_counts)
    return updated_files

# Тестовая строка для проверки обновления состояния
#12
#
#
#
#
#
#
#
#
#
#
#   #
#
#
#
#
#
#   #
#
#
#
#
#
#   