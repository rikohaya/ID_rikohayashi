import google.generativeai as genai
from backend.config import settings


def configure_gemini():
    genai.configure(api_key=settings.gemini_api_key)


def get_model():
    configure_gemini()
    return genai.GenerativeModel("gemini-1.5-flash")


async def generate_response(messages: list[dict], user_message: str) -> str:
    model = get_model()

    history = []
    for msg in messages:
        role = "user" if msg["role"] == "user" else "model"
        history.append({"role": role, "parts": [msg["content"]]})

    chat = model.start_chat(history=history)

    response = chat.send_message(user_message)
    return response.text


async def generate_title(user_message: str) -> str:
    model = get_model()

    prompt = f"""以下のユーザーメッセージに基づいて、会話のタイトルを10文字以内で生成してください。
タイトルのみを出力してください。

ユーザーメッセージ: {user_message}"""

    response = model.generate_content(prompt)
    title = response.text.strip()
    if len(title) > 20:
        title = title[:20] + "..."
    return title
