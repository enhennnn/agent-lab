# 第二部分：实现最小 SWE Agent

状态：已完成

内容：

- `agent_lab/agent.py`：入口，调用 DeepSeek 并启动循环。
- `agent_lab/loop.py`：Agent 主循环。
- `agent_lab/state.py`：Agent 状态。
- `agent_lab/prompt.py`：提示词。
- `agent_lab/parser.py`：解析模型输出。
- `agent_lab/tools/fs.py`：工具实现。
- `agent_lab/tools/registry.py`：工具注册与执行。

验收结果：3 个玩具任务全部通过（pytest 1 passed × 3）。

- `list_dir`
- `read_file`
- `write_file`
- `search_text`
- `run_command`
- `toy_eval.py`：运行 3 个玩具任务验收
- `workspace.py`：工作区安全边界（路径限制）
- `.env` 保护：禁止读写 .env，搜索时跳过点开头文件