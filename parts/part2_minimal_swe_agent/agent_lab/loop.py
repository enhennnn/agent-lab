"""Agent 主循环。"""

import json

from .parser import parse_response
from .prompt import build_messages, build_planning_messages
from .state import AgentState


def make_plan(task: str, call_model) -> str:
    """让模型先生成一个执行计划。"""
    messages = build_planning_messages(task)
    message = call_model(messages, None)
    return message.content or ""


def run_agent(
    task: str,
    registry,
    call_model,
    max_steps: int = 10,
    plan: str | None = None,
) -> AgentState:
    """运行 minimal SWE Agent，直到输出最终答案或达到最大步数。"""
    messages = build_messages(task, plan)
    state = AgentState(
        task=task,
        plan=plan,
        messages=messages,
        max_steps=max_steps,
    )
    tools = registry.to_openai_specs()

    while state.step < state.max_steps:
        message = call_model(messages, tools)
        parsed = parse_response(message)

        if parsed.tool_calls:
            messages.append(parsed.assistant_message)

            for tool_call in parsed.tool_calls:
                result = registry.execute(tool_call.name, tool_call.arguments)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.call_id,
                        "content": json.dumps(result, ensure_ascii=False),
                    }
                )
                state.observations.append(
                    {
                        "tool": tool_call.name,
                        "arguments": tool_call.arguments,
                        "result": result,
                    }
                )

            state.step += 1
            continue

        state.final_answer = parsed.final_text
        state.terminated_reason = "final_answer"
        return state

    state.terminated_reason = "max_steps"
    return state