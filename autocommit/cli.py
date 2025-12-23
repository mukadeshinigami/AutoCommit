"""CLI интерфейс для AutoCommit."""

import argparse
import sys
from pathlib import Path
from typing import Optional

from autocommit.git_handler import GitHandler, NotAGitRepositoryError
from autocommit.analyzer import ChangeAnalyzer
from autocommit.generator import CommitMessageGenerator, CommitGenerationError
from autocommit.config import Config


def main(args: Optional[list] = None) -> int:
    """
    Главная функция CLI.
    
    Args:
        args: Аргументы командной строки. Если None, используются sys.argv.
    
    Returns:
        Код выхода (0 - успех, ненулевое значение - ошибка).
    """
    parser = argparse.ArgumentParser(
        description="Автоматическая генерация коммитов с использованием AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  autocommit                    # Генерировать коммит для текущих изменений
  autocommit --lang en          # Генерировать коммит на английском
  autocommit --stage            # Добавить все файлы в staging перед коммитом
  autocommit --no-commit        # Только показать сообщение, не создавать коммит
        """
    )
    
    parser.add_argument(
        "--repo-path",
        type=Path,
        default=None,
        help="Путь к Git репозиторию (по умолчанию: текущая директория)"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help=f"Модель AI для использования (по умолчанию: {Config.DEFAULT_MODEL})"
    )
    
    parser.add_argument(
        "--lang",
        "--language",
        type=str,
        choices=["ru", "en"],
        default=None,
        help="Язык для сообщения коммита (по умолчанию: ru)"
    )
    
    parser.add_argument(
        "--stage",
        action="store_true",
        help="Добавить все изменения в staging перед анализом"
    )
    
    parser.add_argument(
        "--no-commit",
        action="store_true",
        help="Только показать сообщение коммита, не создавать коммит"
    )
    
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="API ключ для Google GenAI (можно также установить через GOOGLE_API_KEY или GEMINI_API_KEY)"
    )
    
    parsed_args = parser.parse_args(args)
    
    # Загружаем конфигурацию
    config = Config()
    
    # Переопределяем значения из аргументов
    api_key = parsed_args.api_key or config.get_api_key()
    model = parsed_args.model or config.model
    language = parsed_args.lang or config.language
    
    if not api_key:
        print("Ошибка: API ключ не найден. Установите GOOGLE_API_KEY или GEMINI_API_KEY, или используйте --api-key", file=sys.stderr)
        return 1
    
    try:
        # Инициализация компонентов
        git_handler = GitHandler(repo_path=parsed_args.repo_path)
        analyzer = ChangeAnalyzer(git_handler)
        generator = CommitMessageGenerator(api_key=api_key, model=model)
        
        # Проверка наличия изменений
        if not git_handler.has_changes():
            print("Нет изменений для коммита.")
            return 0
        
        # Добавление в staging, если требуется
        if parsed_args.stage:
            print("Добавление изменений в staging...")
            git_handler.stage_all()
        
        # Анализ изменений
        print("Анализ изменений...")
        analysis = analyzer.analyze_changes()
        context = analyzer.prepare_context_for_ai(analysis)
        
        # Генерация сообщения коммита
        print("Генерация сообщения коммита...")
        commit_message = generator.generate_commit_message(context, language=language)
        
        print(f"\nПредложенное сообщение коммита:\n{commit_message}\n")
        
        # Создание коммита, если не указано --no-commit
        if not parsed_args.no_commit:
            confirm = input("Создать коммит с этим сообщением? (y/n): ").strip().lower()
            if confirm in ['y', 'yes', 'д', 'да']:
                git_handler.stage_all()  # Убеждаемся, что все изменения в staging
                git_handler.create_commit(commit_message)
                print("Коммит успешно создан!")
            else:
                print("Коммит отменен.")
                return 0
        
        return 0
        
    except NotAGitRepositoryError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 1
    except CommitGenerationError as e:
        print(f"Ошибка при генерации коммита: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

