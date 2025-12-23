"""Модуль конфигурации."""

import os
from typing import Optional
from pathlib import Path


class Config:
    """Класс для управления конфигурацией приложения."""
    
    # Настройки AI
    DEFAULT_MODEL = "gemini-3-flash-preview"
    DEFAULT_LANGUAGE = "ru"
    
    # Пути
    CONFIG_DIR = Path.home() / ".autocommit"
    CONFIG_FILE = CONFIG_DIR / "config.yaml"
    
    def __init__(self):
        """Инициализация конфигурации."""
        self.model = os.getenv("AUTOCOMMIT_MODEL", self.DEFAULT_MODEL)
        self.language = os.getenv("AUTOCOMMIT_LANGUAGE", self.DEFAULT_LANGUAGE)
        self.api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        self.auto_stage = os.getenv("AUTOCOMMIT_AUTO_STAGE", "false").lower() == "true"
        self.auto_commit = os.getenv("AUTOCOMMIT_AUTO_COMMIT", "false").lower() == "true"
    
    def get_api_key(self) -> Optional[str]:
        """
        Получает API ключ.
        
        Returns:
            API ключ или None, если не установлен.
        """
        return self.api_key
    
    def validate(self) -> bool:
        """
        Проверяет, что конфигурация валидна.
        
        Returns:
            True, если конфигурация валидна, иначе False.
        """
        if not self.api_key:
            return False
        return True

