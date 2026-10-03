# agent-lab

从零实现一个 minimal SWE Agent 的学习项目。

当前进度：第一部分和第二部分已完成，正在向第三部分推进。

## 项目目标

- 理解 ReAct 和 SWE-agent；
- 从零实现 Agent 主循环、工具调用、安全边界；
- 用固定任务评估 Agent；
- 逐步拆解现代 Coding Agent 的工程能力。

详细学习计划见：[LEARNING_PLAN.md](./LEARNING_PLAN.md)

## 当前能力

已实现：

- 工具：
  - `list_dir`
  - `read_file`
  - `write_file`
  - `search_text`
  - `run_command`
- Agent 主循环；
- 状态管理；
- 模型输出解析；
- 工作区安全边界；
- `.env` 敏感文件保护；
- 任务拆分 `plan`；
- 3 个玩具任务验收。

单元测试结果：`33 passed`

## 项目结构

```text
agent-lab/
├─ parts/
│  ├─ part1_basics_and_concepts/
│  ├─ part2_minimal_swe_agent/
│  ├─ part3_reliability_observability/
│  ├─ part4_context_engineering/
│  ├─ part5_codebase_study/
│  └─ part6_integration_delivery/
├─ tests/
├─ evals/
│  └─ tasks/
├─ notes/
├─ traces/
├─ reports/
├─ .env
├─ .env.example
├─ .gitignore
├─ pytest.ini
├─ LEARNING_PLAN.md
└─ README.md
```

## 环境

- conda 环境名：`agent-lab`
- Python：3.12
- 主要依赖：`openai`、`python-dotenv`、`pytest`

## 配置

在项目根目录的 `.env` 中填写：

```text
DEEPSEEK_API_KEY=你的真实 key
```

## 常用命令

激活环境：

```powershell
conda activate agent-lab
```

运行测试：

```powershell
cd D:\MyWork\codex_work\agent-lab
python -m pytest -q
```

运行 minimal SWE Agent：

```powershell
$env:PYTHONPATH='D:\MyWork\codex_work\agent-lab\parts\part2_minimal_swe_agent'
python -m agent_lab.agent
```

运行 3 个玩具任务验收：

```powershell
$env:PYTHONPATH='D:\MyWork\codex_work\agent-lab\parts\part2_minimal_swe_agent'
python -m agent_lab.toy_eval
```

运行第一部分的玩具 ReAct：

```powershell
$env:PYTHONPATH='D:\MyWork\codex_work\agent-lab\parts'
python -m part1_basics_and_concepts.toy_react
```

## 当前进度

| 部分 | 状态 |
|---|---|
| 1. 打基础与理解概念 | 已完成 |
| 2. 实现最小 SWE Agent | 已完成 |
| 3. 可靠性、可观察性与评估 | 未开始 |
| 4. 上下文工程与 v1 | 未开始 |
| 5. 拆解现代 Coding Agent | 未开始 |
| 6. 选择性集成与交付 | 未开始 |