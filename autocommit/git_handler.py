"""Модуль для работы с Git репозиторием."""

import subprocess
from pathlib import Path
from typing import Optional, List, Dict


class GitHandler:
    """Класс для работы с Git репозиторием."""
    
    def __init__(self, repo_path: Optional[Path] = None):
        """
        Инициализация GitHandler.
        
        Args:
            repo_path: Путь к репозиторию. Если None, используется текущая директория.
        """
        self.repo_path = repo_path or Path.cwd()
        self._check_git_repo()
    
    def _check_git_repo(self) -> None:
        """Проверяет, что путь является Git репозиторием."""
        result = self._run_command(["git", "rev-parse", "--git-dir"], check=False)
        if result.returncode != 0:
            raise NotAGitRepositoryError(f"{self.repo_path} не является Git репозиторием")
    
    def _run_command(self, cmd: List[str], check: bool = True) -> subprocess.CompletedProcess:
        """Выполняет Git команду."""
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=check
        )
        return result
    
    def get_status(self) -> Dict[str, List[str]]:
        """
        Получает статус репозитория.
        
        Returns:
            Словарь с ключами: 'modified', 'added', 'deleted', 'renamed', 'untracked'
        """
        result = self._run_command(["git", "status", "--porcelain"])
        lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
        
        status = {
            'modified': [],
            'added': [],
            'deleted': [],
            'renamed': [],
            'untracked': []
        }
        
        for line in lines:
            if not line:
                continue
            status_code = line[:2]
            filename = line[3:]
            
            if status_code.startswith('??'):
                status['untracked'].append(filename)
            elif status_code[0] == 'D':
                status['deleted'].append(filename)
            elif status_code[0] == 'A':
                status['added'].append(filename)
            elif status_code[0] == 'R':
                status['renamed'].append(filename)
            elif status_code[0] in ['M', ' ']:
                if status_code[1] == 'M':
                    status['modified'].append(filename)
        
        return status
    
    def get_diff(self, staged: bool = False) -> str:
        """
        Получает diff изменений.
        
        Args:
            staged: Если True, возвращает diff для staged изменений, иначе для unstaged.
        
        Returns:
            Diff в виде строки.
        """
        if staged:
            result = self._run_command(["git", "diff", "--cached"])
        else:
            result = self._run_command(["git", "diff"])
        return result.stdout
    
    def get_diff_stat(self) -> str:
        """
        Получает статистику изменений.
        
        Returns:
            Статистика изменений.
        """
        result = self._run_command(["git", "diff", "--stat", "--cached"])
        if not result.stdout.strip():
            result = self._run_command(["git", "diff", "--stat"])
        return result.stdout
    
    def stage_all(self) -> None:
        """Добавляет все изменения в staging area."""
        self._run_command(["git", "add", "."])
    
    def create_commit(self, message: str) -> None:
        """
        Создает коммит с указанным сообщением.
        
        Args:
            message: Сообщение коммита.
        """
        self._run_command(["git", "commit", "-m", message])
    
    def has_changes(self) -> bool:
        """
        Проверяет, есть ли изменения в репозитории.
        
        Returns:
            True, если есть изменения, иначе False.
        """
        status = self.get_status()
        total_changes = sum(len(files) for files in status.values())
        return total_changes > 0


class NotAGitRepositoryError(Exception):
    """Исключение, возникающее когда путь не является Git репозиторием."""
    pass

