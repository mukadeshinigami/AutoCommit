"""Модуль для генерации сообщений коммитов с использованием AI."""

from google import genai
from typing import Optional


class CommitMessageGenerator:
    """Класс для генерации сообщений коммитов с помощью AI."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-3-flash-preview"):
        """
        Инициализация CommitMessageGenerator.
        
        Args:
            api_key: API ключ для Google GenAI. Если None, используется значение из окружения.
            model: Название модели для использования.
        """
        self.client = genai.Client(api_key=api_key)
        self.model = model
    
    def generate_commit_message(self, context: str, language: str = "ru") -> str:
        """
        Генерирует сообщение коммита на основе контекста изменений.
        
        Args:
            context: Контекст изменений, подготовленный ChangeAnalyzer.
            language: Язык для сообщения коммита ('ru' или 'en').
        
        Returns:
            Сгенерированное сообщение коммита.
        """
        prompt = self._build_prompt(context, language)
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            commit_message = response.text.strip()
            
            # Очищаем сообщение от возможных кавычек
            commit_message = commit_message.strip('"').strip("'").strip()
            
            return commit_message
        except Exception as e:
            raise CommitGenerationError(f"Ошибка при генерации коммита: {str(e)}")
    
    def _build_prompt(self, context: str, language: str) -> str:
        """
        Формирует промпт для AI на основе контекста.
        
        Args:
            context: Контекст изменений.
            language: Язык для сообщения.
        
        Returns:
            Промпт для AI.
        """
        if language == "ru":
            prompt_template = """Ты помощник для генерации сообщений коммитов Git. 

Проанализируй следующие изменения в коде и создай краткое, но информативное сообщение коммита на русском языке.

Требования к сообщению коммита:
1. Начни с глагола в повелительном наклонении (например: "Добавить", "Исправить", "Обновить")
2. Сообщение должно быть кратким (желательно не более 72 символов)
3. Опиши суть изменений, а не детали реализации
4. Если изменения затрагивают несколько компонентов, используй краткое перечисление

Изменения:
{context}

Сообщение коммита (только текст, без дополнительных объяснений):"""
        else:
            prompt_template = """You are a helper for generating Git commit messages.

Analyze the following code changes and create a brief but informative commit message in English.

Commit message requirements:
1. Start with an imperative verb (e.g., "Add", "Fix", "Update")
2. The message should be brief (preferably no more than 72 characters)
3. Describe the essence of the changes, not implementation details
4. If changes affect multiple components, use a brief enumeration

Changes:
{context}

Commit message (text only, no additional explanations):"""
        
        return prompt_template.format(context=context)


class CommitGenerationError(Exception):
    """Исключение, возникающее при ошибке генерации коммита."""
    pass

