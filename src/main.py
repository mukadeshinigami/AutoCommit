import os
from google import genai
from parser import read_file_if_updated

# Получаем API ключ из переменной окружения
api_key = os.getenv("GOOGLE_AI_API_KEY")
if not api_key:
    raise ValueError("Необходимо установить переменную окружения GOOGLE_AI_API_KEY")

client = genai.Client(api_key=api_key)
updated_files = read_file_if_updated(project_path="./src", extensions=[".py"])

# Если нет обновленных файлов, просто выводим "none" без вызова API
if not updated_files:
    print("none")
    exit(0)

# Формируем содержимое для промпта из обновленных файлов
files_content = "\n\n".join([
    f"File: {os.path.basename(file_path)}\n```\n{content}\n```"
    for file_path, content in updated_files.items()
])

prompt = f"""Analyze the code changes below and generate a git commit message.

Code changes:
{files_content}

Generate a commit message following these rules:
- One line, maximum 72 characters
- Format: <type>: <description>
- Types: feat (new feature), fix (bug fix), refactor (code improvement), docs (documentation), style (formatting)
- Use imperative mood: "Add feature" not "Added feature"
- Be concise and specific

Important: DO NOT return "none" or "no changes". Always generate a commit message based on the code changes provided above.

Commit message:"""

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=prompt
)

# Получаем и очищаем ответ
commit_msg = response.text.strip()

# Проверяем, что ответ не "none" (на случай, если модель все равно вернула)
if commit_msg.lower() == "none" or not commit_msg:
    print(f"Error: Model returned invalid response: '{commit_msg}'. Please try again.")
    exit(1)

# Выводим команды git в нужном формате
print("git add .")
print(f'git commit -m "{commit_msg}"')
print("git push")
#
#
#
#