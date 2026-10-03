"""Agent 提示词。"""

SYSTEM_PROMPT = """你是一个 minimal SWE Agent。

你的任务是使用可用工具完成用户的要求。
如果需要查看目录，请调用 list_dir。
如果需要查看文件内容，请调用 read_file。
如果需要写入文件，请调用 write_file。
如果需要搜索文本，请调用 search_text。
如果需要执行命令，请调用 run_command。

完成全部任务后，直接输出最终答案，不要再调用工具。
"""

PLAN_PROMPT = """你是一个任务规划器。

请根据用户任务，输出一个简短的分步执行计划。
只输出计划本身，不要调用工具，不要输出其他内容。
计划用数字列表表示，例如：

1. 读取目标文件
2. 找到问题
3. 修改文件
4. 运行测试验证
"""


def build_messages(task: str, plan: str | None = None) -> list[dict]:
    system = SYSTEM_PROMPT

    if plan:
        system += f"\n\n当前执行计划：\n{plan}\n请按计划逐步执行。"

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": task},
    ]


def build_planning_messages(task: str) -> list[dict]:
    return [
        {"role": "system", "content": PLAN_PROMPT},
        {"role": "user", "content": task},
    ]