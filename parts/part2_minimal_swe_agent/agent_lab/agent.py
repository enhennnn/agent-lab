"""运行 minimal SWE Agent。"""

import os

from dotenv import load_dotenv
from openai import OpenAI

from .loop import make_plan, run_agent
from .tools.registry import build_default_registry

DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"


def load_api_key() -> str | None:
    load_dotenv()
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key:
        return None
    return key


def call_deepseek(messages, tools):
    """把 messages 和 tools 发给 DeepSeek，返回 message 对象。"""
    api_key = load_api_key()
    if not api_key:
        raise RuntimeError("未找到 DEEPSEEK_API_KEY，请先在项目根目录的 .env 中填写。")

    client = OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)

    request = {
        "model": DEEPSEEK_MODEL,
        "messages": messages,
    }
    if tools:
        request["tools"] = tools

    response = client.chat.completions.create(**request)
    return response.choices[0].message


def main(use_plan: bool = True) -> int:
    if not load_api_key():
        print("未找到 DEEPSEEK_API_KEY，请先在项目根目录的 .env 中填写。")
        return 1

    registry = build_default_registry()
    task = "查看当前目录，读取 .env.example 文件，然后告诉我这个项目需要配置哪个环境变量。"

    if use_plan:
        plan = make_plan(task, call_deepseek)
        print("Plan:")
        print(plan)
        print()
    else:
        plan = None
        print("Plan: disabled")
        print()

    state = run_agent(task, registry, call_deepseek, max_steps=10, plan=plan)

    print(f"Steps: {state.step}")
    print(f"Terminated: {state.terminated_reason}")
    print("Observations:")
    for observation in state.observations:
        print("  ", observation)
    print("Final answer:")
    print(state.final_answer)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())