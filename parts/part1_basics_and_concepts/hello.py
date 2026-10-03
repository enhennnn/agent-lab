import os

from dotenv import load_dotenv
from openai import OpenAI

DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"

# 载入DEEPSEEK_API_KEY
def load_api_key() -> str | None:
    load_dotenv()
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key:
        return None
    return key


def main() -> int:
    api_key = load_api_key()
    if not api_key:
        print("未找到 DEEPSEEK_API_KEY，请先在项目根目录的 .env 中填写。")
        return 1

    client = OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)

    response = client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "请只回复两个字：正常"},
        ],
    )

    content = response.choices[0].message.content
    print(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())