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


async def estimate_target_population(target_description: str, media: str) -> dict:
    """AIを使ってターゲットの推定人口を算出"""
    model = get_model()

    prompt = f"""あなたは日本のマーケティングリサーチの専門家です。
以下のターゲット層について、日本国内の推定人口を算出してください。

ターゲット: {target_description}
広告媒体: {media}

以下の形式で回答してください（JSON形式で出力）:
{{
    "estimated_population": <推定人口（整数、単位：人）>,
    "reasoning": "<推定根拠を2-3文で説明>",
    "confidence": "<high/medium/low>"
}}

推定のポイント：
- 日本の総人口は約1億2500万人
- 年齢層別・性別の人口統計を考慮
- ターゲットの条件（年齢、性別、興味関心、行動特性など）を掛け合わせて推定
- {media}の利用率も考慮に入れる

JSON形式のみを出力してください。"""

    response = model.generate_content(prompt)
    response_text = response.text.strip()

    # JSONをパース
    import json
    import re

    # コードブロックを除去
    json_match = re.search(r'\{[^{}]*\}', response_text, re.DOTALL)
    if json_match:
        response_text = json_match.group()

    try:
        result = json.loads(response_text)
        return {
            "estimated_population": int(result.get("estimated_population", 0)),
            "reasoning": result.get("reasoning", "推定根拠なし"),
            "confidence": result.get("confidence", "medium"),
        }
    except json.JSONDecodeError:
        # パース失敗時のフォールバック
        return {
            "estimated_population": 1000000,
            "reasoning": "AIからの応答をパースできませんでした。デフォルト値を使用しています。",
            "confidence": "low",
        }
