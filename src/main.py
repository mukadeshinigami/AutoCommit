import os
from google import genai
from parser import read_file_if_updated

# Получаем API ключ из переменной окружения
api_key = os.getenv("GOOGLE_AI_API_KEY")
if not api_key:
    raise ValueError("Необходимо установить переменную окружения GOOGLE_AI_API_KEY")

client = genai.Client(api_key=api_key)
commit_message = read_file_if_updated(project_path="./src", extensions=[".py"])

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=f"Напиши commit message для следующего изменения в формате, ответ должен быть в виде 1 строки : git -m commit\"{commit_message}\"",
)
a='123'

print(response.text)
