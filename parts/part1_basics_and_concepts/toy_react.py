"""一个最小 ReAct 玩具。

让模型按 Thought -> Action -> Observation 循环，
直到模型输出 finish 并给出最终答案。

本文件刻意不使用原生 tool calling，而是用 JSON 文本协议，
以便更直观地看到 ReAct 的推理和行动过程。
"""

import ast
import json
import operator
import os

from dotenv import load_dotenv
from openai import OpenAI

DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"

SYSTEM_PROMPT = """你是一个 ReAct Agent。

每一步只输出一个 JSON 对象，不要输出其他任何文字。

调用工具时输出：
{"thought": "你的思考", "action": "calculator", "action_input": {"expression": "2+3"}}

结束任务时输出：
{"thought": "你的思考", "action": "finish", "answer": "最终答案"}

当前唯一可用工具是 calculator，参数 expression 是一个算术表达式字符串。
"""

_BINARY_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _eval_node(node):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op = _BINARY_OPS.get(type(node.op))
        if op is None:
            raise ValueError(f"unsupported operator: {type(node.op).__name__}")
        return op(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op = _UNARY_OPS.get(type(node.op))
        if op is None:
            raise ValueError(f"unsupported unary operator: {type(node.op).__name__}")
        return op(operand)

    raise ValueError(f"unsupported expression node: {type(node).__name__}")


def calculator(expression: str) -> dict:
    """安全地计算简单算术表达式。"""
    if not isinstance(expression, str):
        return {"ok": False, "error": "expression must be a string"}

    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval_node(tree)
        if isinstance(result, complex):
            return {"ok": False, "error": "complex numbers are not allowed"}
        return {"ok": True, "result": result}
    except Exception as exc:  # noqa: BLE001 - 玩具工具需要兜底
        return {"ok": False, "error": str(exc)}


def execute_tool(name: str, arguments: dict) -> dict:
    if name == "calculator":
        return calculator(arguments.get("expression"))
    return {"ok": False, "error": f"unknown tool: {name}"}


def parse_action(raw: str) -> dict:
    """把模型输出解析成 JSON 动作。"""
    text = raw.strip()

    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    return json.loads(text)


def run_react_loop(task: str, call_model, max_steps: int = 6):
    """执行 ReAct 循环，返回 (最终答案, 步骤记录)。"""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": task},
    ]
    steps = []

    for _ in range(max_steps):
        raw = call_model(messages)

        try:
            action = parse_action(raw)
        except Exception as exc:
            observation = f"输出无法解析为 JSON：{exc}。请重新只输出一个 JSON 对象。"
            messages.append({"role": "user", "content": f"Observation: {observation}"})
            steps.append({"raw": raw, "action": None, "observation": observation})
            continue

        if not isinstance(action, dict):
            observation = "动作必须是 JSON 对象。"
            messages.append({"role": "user", "content": f"Observation: {observation}"})
            steps.append({"raw": raw, "action": action, "observation": observation})
            continue

        if action.get("action") == "finish":
            answer = action.get("answer")
            steps.append({"raw": raw, "action": action, "observation": "finish"})
            return answer, steps

        tool_name = action.get("action")
        arguments = action.get("action_input") or {}
        result = execute_tool(tool_name, arguments)
        observation = json.dumps(result, ensure_ascii=False)

        messages.append({"role": "assistant", "content": raw})
        messages.append({"role": "user", "content": f"Observation: {observation}"})
        steps.append({"raw": raw, "action": action, "observation": result})

    return "达到最大步数", steps


def call_deepseek(messages) -> str:
    load_dotenv()
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("未找到 DEEPSEEK_API_KEY，请先在项目根目录的 .env 中填写。")

    client = OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)
    response = client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content or ""


def main() -> int:
    task = "请用 calculator 计算 12 * 8 + 7，然后告诉我结果。"

    answer, steps = run_react_loop(task, call_deepseek, max_steps=6)

    for index, step in enumerate(steps, start=1):
        print(f"--- Step {index} ---")
        print("模型输出:", step["raw"])
        if step.get("action"):
            print("Action:", step["action"])
        print("Observation:", step["observation"])
        print()

    print("最终答案:", answer)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())