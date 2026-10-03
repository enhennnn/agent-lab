"""测试 Agent 主循环。"""

import json

from agent_lab.loop import make_plan, run_agent
from agent_lab.tools.registry import build_default_registry
from agent_lab.tools.workspace import set_workspace_root


class FakeFunction:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments


class FakeToolCall:
    def __init__(self, call_id, name, arguments):
        self.id = call_id
        self.function = FakeFunction(name, arguments)


class FakeMessage:
    def __init__(self, content=None, tool_calls=None):
        self.content = content
        self.tool_calls = tool_calls


def test_loop_runs_tool_then_finishes(tmp_path):
    registry = build_default_registry()

    responses = iter(
        [
            FakeMessage(
                tool_calls=[
                    FakeToolCall(
                        "call_1",
                        "list_dir",
                        json.dumps({"path": str(tmp_path)}),
                    )
                ]
            ),
            FakeMessage(content="任务完成。"),
        ]
    )

    def fake_model(messages, tools):
        return next(responses)

    state = run_agent("查看目录", registry, fake_model, max_steps=5)

    assert state.final_answer == "任务完成。"
    assert state.terminated_reason == "final_answer"
    assert len(state.observations) == 1
    assert state.observations[0]["tool"] == "list_dir"


def test_loop_stops_at_max_steps():
    registry = build_default_registry()

    def fake_model(messages, tools):
        return FakeMessage(
            tool_calls=[
                FakeToolCall(
                    "call_1",
                    "list_dir",
                    json.dumps({"path": "."}),
                )
            ]
        )

    state = run_agent("测试", registry, fake_model, max_steps=2)

    assert state.final_answer is None
    assert state.terminated_reason == "max_steps"
    assert state.step == 2


def test_make_plan_returns_plan_text():
    def fake_model(messages, tools):
        assert tools is None
        return FakeMessage(content="1. 读取文件\n2. 修复问题")

    plan = make_plan("修复问题", fake_model)

    assert plan == "1. 读取文件\n2. 修复问题"


def test_run_agent_stores_plan(tmp_path):
    set_workspace_root(tmp_path)
    registry = build_default_registry()

    def fake_model(messages, tools):
        return FakeMessage(content="任务完成。")

    plan = "1. 列出目录\n2. 读取文件"
    state = run_agent("查看目录", registry, fake_model, max_steps=5, plan=plan)

    assert state.plan == plan
    assert plan in state.messages[0]["content"]
    assert state.final_answer == "任务完成。"