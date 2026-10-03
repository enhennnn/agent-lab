"""测试玩具 ReAct 的解析、工具和循环。"""

from part1_basics_and_concepts.toy_react import calculator, parse_action, run_react_loop


def test_calculator_basic():
    result = calculator("2 + 3 * 4")
    assert result["ok"] is True
    assert result["result"] == 14


def test_calculator_rejects_unsafe_code():
    result = calculator("__import__('os').getcwd()")
    assert result["ok"] is False


def test_parse_action_strips_code_fence():
    raw = '```json\n{"action": "finish", "answer": "5"}\n```'
    action = parse_action(raw)
    assert action["action"] == "finish"
    assert action["answer"] == "5"


def test_react_loop_reaches_finish():
    responses = iter(
        [
            '{"thought": "先计算", "action": "calculator", "action_input": {"expression": "2+3"}}',
            '{"thought": "得到5", "action": "finish", "answer": "5"}',
        ]
    )

    def fake_model(messages):
        return next(responses)

    answer, steps = run_react_loop("计算 2+3", fake_model, max_steps=4)
    assert answer == "5"
    assert len(steps) == 2


def test_react_loop_stops_at_max_steps():
    def fake_model(messages):
        return '{"thought": "继续", "action": "calculator", "action_input": {"expression": "1+1"}}'

    answer, steps = run_react_loop("测试", fake_model, max_steps=3)
    assert answer == "达到最大步数"
    assert len(steps) == 3