"""Модуль для анализа изменений в репозитории."""

from typing import Dict, List
from autocommit.git_handler import GitHandler


class ChangeAnalyzer:
    """Класс для анализа изменений в Git репозитории."""
    
    def __init__(self, git_handler: GitHandler):
        """
        Инициализация ChangeAnalyzer.
        
        Args:
            git_handler: Экземпляр GitHandler для работы с Git.
        """
        self.git_handler = git_handler
    
    def analyze_changes(self) -> Dict[str, any]:
        """
        Анализирует изменения в репозитории и формирует контекст для генерации коммита.
        
        Returns:
            Словарь с информацией об изменениях:
            - 'status': статус файлов
            - 'diff': diff изменений
            - 'diff_stat': статистика изменений
            - 'summary': краткое описание изменений
        """
        status = self.git_handler.get_status()
        diff = self.git_handler.get_diff(staged=True)
        if not diff:
            diff = self.git_handler.get_diff(staged=False)
        diff_stat = self.git_handler.get_diff_stat()
        
        summary = self._generate_summary(status, diff_stat)
        
        return {
            'status': status,
            'diff': diff,
            'diff_stat': diff_stat,
            'summary': summary
        }
    
    def _generate_summary(self, status: Dict[str, List[str]], diff_stat: str) -> str:
        """
        Генерирует краткое описание изменений.
        
        Args:
            status: Статус файлов из GitHandler.get_status()
            diff_stat: Статистика изменений.
        
        Returns:
            Краткое описание изменений.
        """
        parts = []
        
        if status['added']:
            parts.append(f"Добавлено файлов: {len(status['added'])}")
        if status['modified']:
            parts.append(f"Изменено файлов: {len(status['modified'])}")
        if status['deleted']:
            parts.append(f"Удалено файлов: {len(status['deleted'])}")
        if status['renamed']:
            parts.append(f"Переименовано файлов: {len(status['renamed'])}")
        if status['untracked']:
            parts.append(f"Новых файлов: {len(status['untracked'])}")
        
        summary = ", ".join(parts) if parts else "Нет изменений"
        
        # Добавляем информацию о типах файлов
        all_files = (
            status['added'] + status['modified'] + 
            status['deleted'] + status['renamed'] + status['untracked']
        )
        file_types = self._analyze_file_types(all_files)
        if file_types:
            summary += f" | Типы файлов: {', '.join(file_types)}"
        
        return summary
    
    def _analyze_file_types(self, files: List[str]) -> List[str]:
        """
        Анализирует типы измененных файлов.
        
        Args:
            files: Список путей к файлам.
        
        Returns:
            Список уникальных расширений файлов.
        """
        extensions = set()
        for file in files:
            if '.' in file:
                ext = file.split('.')[-1].lower()
                extensions.add(ext)
        return sorted(list(extensions))
    
    def prepare_context_for_ai(self, analysis: Dict[str, any]) -> str:
        """
        Подготавливает контекст для AI генератора коммита.
        
        Args:
            analysis: Результат analyze_changes().
        
        Returns:
            Форматированный контекст для AI.
        """
        context_parts = []
        
        # Добавляем краткое описание
        context_parts.append(f"Краткое описание изменений:\n{analysis['summary']}\n")
        
        # Добавляем статистику
        if analysis['diff_stat']:
            context_parts.append(f"Статистика изменений:\n{analysis['diff_stat']}\n")
        
        # Добавляем diff (ограничиваем размер для экономии токенов)
        diff = analysis['diff']
        if diff:
            # Ограничиваем diff до 5000 символов, чтобы не превышать лимиты AI
            max_diff_length = 5000
            if len(diff) > max_diff_length:
                diff = diff[:max_diff_length] + "\n... (diff обрезан)"
            context_parts.append(f"Изменения в коде:\n{diff}")
        
        return "\n".join(context_parts)

