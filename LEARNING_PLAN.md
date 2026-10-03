# 从零实现 Coding Agent 的步骤化学习计划

> 本计划不绑定固定日历、固定期限或固定投入时间。  
> 每个步骤都可以独立完成后暂停，但进入下一步前应先通过当前步骤的验收门槛。  
> 核心路线：先理解 → 再实现最小版本 → 再拆解现代完整系统 → 最后做选择性工程复现。

---

## 0. 使用说明

这不是一份“读完就算完成”的阅读清单，而是一张按依赖关系排列的执行板。

执行规则：

1. 一次只设置一个主要问题，避免同时学多个系统或多个高级能力。
2. 每个步骤都要留下可运行产物、可验证证据和复盘记录。
3. 每个步骤完成后做一次验收，没有通过就不要急着进入下一步。
4. 允许 AI 辅助读代码，但所有结论都要回到源码、测试或实验验证。
5. 高级能力必须有证据证明有价值后才能集成，不能因为流行就实现。
6. 步骤可以按实际情况拆分、重复或暂停，但不要跳过基础闭环。
7. 本计划关注“理解和实现核心机制”，不以功能数量作为完成标准。

---

## 1. 最终目标

完成一个自己的仓库：`agent-lab`。

最终应具备：

- 一个从零实现、可运行的 minimal SWE Agent；
- 一套清晰的 Agent 状态、循环、prompt、parser、executor 和 tool calling 机制；
- 基础文件 I/O 与 terminal 执行能力；
- 可记录、可回放、可统计的 Agent trace；
- 一组固定的评估任务和评测报告；
- 对至少一个成熟 Coding Agent 的架构拆解；
- 一个主系统和一个对照系统的能力对比矩阵；
- 2–3 个经过验证的高级工程能力，例如上下文压缩、MCP、后台任务或最小 TUI；
- 一份设计文档，解释每个功能解决什么问题、代价是什么、为什么不实现某些功能。

一句话验收标准：

> 我能运行自己的 Agent，解释它每一步为什么这样做；也能指出成熟 Agent 的某个能力具体在哪个文件、哪个状态机、哪个循环中实现，并说明其设计取舍。

---

## 2. 学习边界

本计划重点覆盖 Coding Agent 的核心工程链路。

本计划不要求：

- 从头训练大模型；
- 复刻生产级 Codex、OpenCode 或 Kimi Code CLI；
- 第一版就实现完整 multi-agent；
- 第一版就实现长期记忆、分布式任务队列和复杂权限系统；
- 追求覆盖所有框架和所有模型提供商；
- 用“功能数量”代替“系统理解和可验证结果”。

本计划必须覆盖：

- Agent 循环；
- Tool calling；
- 文件系统与 shell；
- 任务状态；
- 上下文构建与压缩；
- 错误恢复；
- 沙箱与安全边界；
- trace 与评估；
- 现代 Coding Agent 的代码结构；
- 对插件、MCP、后台任务、memory、multi-agent 的工程理解。

---

## 3. 能力阶梯

| 层级 | 能力 | 可观察证据 |
|---|---|---|
| C1 | 理解 Agent 基本概念 | 能解释 ReAct、Action、Observation、ACI |
| C2 | 调用模型和工具 | 能完成一次 tool call 并回填结果 |
| C3 | 构建最小循环 | 模型能连续执行多步并结束任务 |
| C4 | 操作真实开发环境 | 能读文件、搜索、执行命令、写文件 |
| C5 | 提高可靠性 | 能处理超时、错误、循环和预算限制 |
| C6 | 测量和优化 | 有成功率、token、步数、耗时和失败分类 |
| C7 | 拆解成熟系统 | 能把功能定位到代码路径并复现核心机制 |

---

## 4. 项目目录结构

当前代码按六个学习部分分开存放：

```text
agent-lab/
├─ parts/
│  ├─ part1_basics_and_concepts/
│  │  ├─ hello.py
│  │  ├─ toy_react.py
│  │  └─ README.md
│  ├─ part2_minimal_swe_agent/
│  │  ├─ agent_lab/
│  │  │  ├─ agent.py
│  │  │  ├─ loop.py
│  │  │  ├─ state.py
│  │  │  ├─ prompt.py
│  │  │  ├─ parser.py
│  │  │  └─ tools/
│  │  └─ README.md
│  ├─ part3_reliability_observability/
│  ├─ part4_context_engineering/
│  ├─ part5_codebase_study/
│  └─ part6_integration_delivery/
├─ tests/
├─ evals/
├─ notes/
├─ traces/
├─ reports/
├─ .env
├─ .env.example
├─ .gitignore
├─ pytest.ini
└─ README.md
```

目录职责：

- `parts/`：按六个学习部分组织代码和说明；
- `tests/`：单元测试和集成测试；
- `evals/`：评估任务及其初始仓库；
- `traces/`：每次运行的 JSONL 轨迹；
- `notes/`：问题、调用链、实验和结论；
- `reports/`：评测报告、架构对比和最终设计文档。
## 5. 总体路线：六个主要步骤

| 步骤 | 名称 | 主要目标 | 核心产物 | 进入下一步的门槛 |
|---:|---|---|---|---|
| 1 | 打基础与理解概念 | 掌握 LLM API、tool calling、ReAct 和 SWE-agent | API CLI、工具调用 demo、概念笔记 | 模型要求工具后能执行并回填结果 |
| 2 | 实现最小 SWE Agent | 从零打通状态、prompt、parser、executor、file I/O 和 loop | minimal agent v0 | 能修复小型玩具仓库任务 |
| 3 | 可靠性、可观察性与评估 | 让 Agent 可恢复、可回放、可量化 | trace、评估集、第一份评测报告 | 有成功率、成本和失败分类 |
| 4 | 上下文工程与 v1 | 管理上下文预算，区分不同类型的记忆 | context compressor、v1 | 压缩后 token 下降且成功率不明显下降 |
| 5 | 拆解现代 Coding Agent | 逆向分析主系统、对照系统和关键工程能力 | 架构图、调用链、能力矩阵、最小复现 | 能把功能定位到具体代码路径 |
| 6 | 选择性集成与交付 | 只集成经过验证的高级能力并完成演示 | v2、文档、评测报告、demo | 新环境可复现，结果和限制都清楚 |

六个步骤之间存在依赖关系：

```text
概念模型
→ 最小闭环
→ 可靠性验证
→ 上下文优化
→ 成熟系统拆解
→ 选择性集成交付
```

不要颠倒顺序。尤其不要在最小 Agent 还不能评估时，就开始做 memory、multi-agent 或复杂插件系统。

---

## 6. 步骤一：打基础与理解概念

### 1.1 掌握模型调用和 tool calling

目标：证明自己可以从零调用模型、声明工具、执行工具并把结果送回模型。

任务：

- 学习 Python 项目结构、虚拟环境、配置管理和测试基础；
- 学习 messages、system/user/assistant 角色和结构化输出；
- 学习 tool/function calling 的请求与响应格式；
- 学习 subprocess、pathlib、超时、工作目录和错误处理；
- 创建一个最小 CLI；
- 让模型能够调用 `read_file` 或 `run_command` 等单一工具。

交付物：

- `pyproject.toml` 和 `README.md`；
- `call_llm.py` 或 `cli.py`；
- `tool_call_demo.py`；
- 一份 API 和 tool calling 笔记。

验收标准：

- 能展示完整链路：用户输入 → 模型选择工具 → 程序执行 → 结果回填 → 模型输出；
- 能解释 messages、tool schema、tool result 的区别；
- 能处理 API 错误、超时和格式错误中的至少一种。

### 1.2 理解 ReAct 与 SWE-agent

目标：建立 Agent 的心智模型，而不是只记术语。

任务：

- 阅读 ReAct 论文，重点理解 Thought、Action、Observation 循环；
- 阅读 SWE-agent 论文及官方仓库说明，重点理解 Agent-Computer Interface；
- 了解 SWE-bench 的任务形式和评价逻辑；
- 画一张 ReAct 循环图；
- 画一张 SWE-agent 的“模型—工具—环境—反馈”图；
- 写一个只能读文件和计算的玩具 ReAct Agent。

注意：

- ReAct 是 Shunyu Yao 主导的经典工作；
- SWE-agent 是 Shunyu Yao 参与的系统论文，但他不是第一作者；
- 阅读时区分“论文思想”和“仓库工程实现”，不要混为一谈。

交付物：

- `notes/react.md`；
- `notes/swe-agent.md`；
- `labs/toy-react/`；
- 一次完整玩具轨迹。

验收标准：

- 不看资料能解释 ReAct 为什么能构成 Agent；
- 能解释 ACI 为何重要；
- 能指出玩具 Agent 的循环、工具接口、观察结果和终止条件。

完成步骤一后，应得到的最小结果是：

> 模型能选择工具 → 程序能执行工具 → 结果能回到模型 → 模型能继续下一步。

---

## 7. 步骤二：实现最小 SWE Agent

这个步骤的目标不是复刻完整产品，而是亲手打通最小闭环。

### 2.1 设计 Agent 骨架

任务：

- 定义 `AgentState`；
- 定义 `ToolSpec`、`ToolCall`、`ToolResult`；
- 实现 `LLMClient`；
- 实现 `PromptBuilder` 的基础版本；
- 实现 `ToolRegistry`；
- 实现 `OutputParser` 的第一版；
- 让模型调用一个 `echo` 或 `list_dir` 工具。

建议数据结构：

```python
@dataclass
class AgentState:
    task: str
    messages: list[dict]
    plan: str | None
    step: int
    max_steps: int
    observations: list[dict]
    final_answer: str | None
    token_budget: int | None
    started_at: float
```

交付物：

- `src/agent_lab/state.py`；
- `src/agent_lab/llm.py`；
- `src/agent_lab/prompt.py`；
- `src/agent_lab/parser.py`；
- `src/agent_lab/tools/registry.py`。

验收标准：

- 模型可以输出一个合法工具调用；
- 解析器可以验证工具名和参数；
- 未知工具和非法参数有明确错误信息。

### 2.2 实现文件系统和 terminal 工具

任务：

- 实现 `read_file`；
- 实现 `write_file`；
- 实现 `list_dir`；
- 实现 `grep` 或文本搜索；
- 实现 `run_command`；
- 统一工作目录；
- 实现路径规范化，禁止访问工作区外文件；
- 实现 shell 超时、输出截断和退出码；
- 为每个工具写测试。

交付物：

- `tools/fs.py`；
- `tools/shell.py`；
- `tests/test_tools.py`；
- 工具说明文档。

验收标准：

- 读取、写入、搜索、执行命令均可用；
- 越界路径被拒绝；
- 超时、非零退出码和异常都有结构化返回；
- 工具不会把巨量输出直接塞回上下文。

### 2.3 打通 Agent Loop

任务：

- 实现主循环；
- 实现 message 更新；
- 把工具结果作为 observation 回填；
- 让模型输出计划或当前步骤；
- 实现最大步数限制；
- 实现 token 或时间预算；
- 实现 `final_answer` 终止条件；
- 准备 3 个玩具仓库任务。

主循环：

```text
初始化 State
while 未完成且未超过预算:
    prompt = build_prompt(state)
    output = call_llm(prompt, tools)
    action = parse(output)
    result = execute(action)
    state = update(state, action, result)
return final_answer
```

交付物：

- `loop.py`；
- `executor.py`；
- 3 个玩具任务及其结果；
- 一份循环流程图。

验收标准：

- Agent 能读到目标文件；
- 能执行检查命令；
- 能修改文件；
- 能再次验证；
- 能在完成或超过预算时停止。

### 2.4 理解任务拆分与状态转移

任务：

- 区分任务目标、当前计划、当前步骤和工具观察；
- 不引入独立 planner，先把“计划文本”保存在 State 中；
- 让模型根据 observation 更新下一步；
- 识别已完成、未完成和阻塞状态；
- 记录每次状态变化。

验收标准：

- Agent 能说明当前正在做什么；
- Agent 不会在任务完成后继续无意义调用工具；
- 任务被拆成可观察的小步骤，而不是一次性输出大段计划。

---

## 8. 步骤三：可靠性、可观察性与评估

这个步骤把“偶尔能跑”变成“可以稳定观察、复现和量化”。

### 3.1 实现错误恢复和预算控制

任务：

- 对模型输出做重试；
- 对 tool 调用失败做重试或替代方案；
- 识别重复工具调用；
- 识别无进展循环；
- 实现上下文裁剪；
- 实现错误摘要；
- 区分可恢复错误和不可恢复错误；
- 记录每一步耗时和 token。

交付物：

- 重试和错误恢复逻辑；
- `tests/test_loop.py`；
- 失败案例集合；
- 可靠性说明。

验收标准：

- 工具报错后，Agent 至少能尝试一次修正；
- 重复调用不会无限循环；
- 预算耗尽时能给出清晰失败原因；
- 失败轨迹可以被重放。

### 3.2 实现 Trace

任务：

- 定义 JSONL trace schema；
- 记录 prompt、模型输出、工具调用、结果、耗时和 token；
- 实现 trace replay；
- 区分公开任务和 holdout 任务；
- 支持按 run、task、step 检索轨迹。

建议 trace 字段：

```json
{
  "run_id": "uuid",
  "task_id": "toy-001",
  "step": 1,
  "model": "model-name",
  "action": {"tool": "read_file", "args": {"path": "src/main.py"}},
  "result": {"ok": true, "content": "..."},
  "prompt_tokens": 1200,
  "completion_tokens": 180,
  "duration_ms": 2300,
  "error": null
}
```

交付物：

- `trace.py`；
- `traces/*.jsonl`；
- trace replay 命令；
- trace schema 文档。

验收标准：

- 任意一次失败都能从 trace 中复现；
- 能看见每一步的状态转移；
- trace 不只记录最终结果。

### 3.3 建立固定评估集

任务：

- 建立 10–20 个评估任务；
- 覆盖只读分析、单文件修复、测试失败修复、多文件修改和错误恢复；
- 每个任务配置初始仓库、执行命令、期望命令和预算；
- 保留一部分任务不用于日常调试；
- 统计成功率、平均步数、token、耗时和失败类型；
- 写第一份失败分析。

任务定义模板：

```yaml
id: task-001
type: single-file-fix
repo: evals/tasks/task-001/repo
instruction: "修复 tests/test_calc.py 中失败的测试，不要修改测试文件。"
setup:
  command: "pytest -q"
expected:
  command: "pytest -q"
budget:
  max_steps: 15
  timeout_seconds: 180
```

交付物：

- `evals/tasks/`；
- `reports/eval-01.md`；
- 失败分类表；
- 基线指标。

验收标准：

- 有一定规模的可重复评估；
- 任意一次失败都能从 trace 中复现；
- 不允许通过修改评估标准来制造“成功”。

建议初始目标：

- 玩具任务成功率达到 70% 以上；
- 安全违规为 0；
- 每个失败任务都有可复现 trace 和明确失败分类。

这些目标不是绝对标准，而是迫使自己测量和复盘的最低要求。

---

## 9. 步骤四：上下文工程与 v1

目标：理解上下文预算，而不是简单无限追加消息。

任务：

- 区分 working memory、conversation history、task state、project memory 和 artifact memory；
- 计算 prompt token budget；
- 实现旧观察摘要；
- 实现工具输出截断；
- 实现文件片段和 artifact 引用；
- 保留关键任务目标、已修改文件和未解决问题；
- 比较压缩前后效果；
- 压缩失败时回退到未压缩版本。

交付物：

- `context/budget.py`；
- `context/compact.py`；
- 压缩前后对比报告；
- minimal agent v1。

验收标准：

- token 平均下降，成功率不显著下降；
- 压缩后仍能回答“当前目标是什么、已经改了什么、下一步是什么”；
- 不同上下文类型不会被混为一谈；
- 压缩机制有明确的触发条件和回退策略。

建议初始目标：

- 压缩后 token 下降至少 20%；
- 成功率下降不超过 5 个百分点；
- 压缩后的关键任务信息仍然可追踪。

---

## 10. 步骤五：拆解现代 Coding Agent

这个步骤的目标不是“看完一个仓库”，而是用问题驱动逆向分析。

### 5.1 选择主系统和对照系统

选择原则：

- 主系统只选一个：Codex、OpenCode 或 Kimi Code CLI；
- 对照系统再选一个；
- 第三个只做功能对比，不做完整精读。

任务：

- 写清为什么选择这个主系统；
- 确定自己最关心的 5–8 个工程问题；
- 建立代码阅读日志；
- 记录源码版本和 commit，避免结论漂移。

### 5.2 建立架构地图

任务：

- 找到 CLI 入口；
- 找到 session 或 conversation 对象；
- 找到模型调用位置；
- 找到主 Agent loop；
- 找到工具注册和 executor；
- 找到文件编辑、shell 和权限处理；
- 串起一次完整任务的调用链；
- 画顶层架构图和时序图。

交付物：

- `notes/codebase-map.md`；
- `diagrams/system-architecture.md`；
- `diagrams/task-sequence.md`。

验收标准：

- 能从用户输入追到模型调用；
- 能从工具调用追到真正执行位置；
- 能指出状态是如何被保存和恢复的。

### 5.3 深挖核心执行机制

每个主题只追一条调用链，不要泛读整个仓库。

主题：

- 主循环如何判断继续和结束；
- workflow 如何限制 Agent 行为；
- context compression / compaction 何时触发；
- 工具注册表如何管理 schema 和权限；
- MCP 如何接入外部能力；
- 错误和取消如何传播。

每个主题使用同一流程：

```text
提出具体问题
→ 找到入口
→ 追踪调用链
→ 找到数据结构和状态
→ 找测试或日志验证
→ 写最小复现
→ 记录设计取舍
```

交付物：

- 5 份 `notes/feature-*.md`；
- 5 个 `labs/*` 最小复现；
- 一张调用链总图。

验收标准：

- 每个结论都有文件、函数或测试支撑；
- 能用自己的 Agent 复现至少一个机制的核心思想；
- 能说出这个机制的失败模式和替代方案。

### 5.4 研究扩展能力和安全边界

任务：

- 研究 sandbox 的工作目录、网络、进程和文件权限限制；
- 研究后台任务的创建、查询、取消和结果收集；
- 研究 skills 如何提供上下文和流程指令；
- 研究 plugins 如何注册工具、命令或 UI 扩展；
- 为自己的 Agent 设计统一扩展接口；
- 选择 2–3 个机制做最小原型。

交付物：

- `labs/sandbox/`；
- `labs/background-task/`；
- `labs/plugin-or-mcp/`；
- `reports/extension-design.md`。

验收标准：

- 能区分“工具扩展”“上下文扩展”“UI 扩展”；
- 能在不修改主循环的情况下注册一个新工具；
- 后台任务有状态、超时和取消机制；
- 能说明哪些操作必须审批或拒绝。

### 5.5 研究高级能力并做能力矩阵

任务：

- 区分 session memory、project memory、long-term memory 和 artifact memory；
- 研究多 Agent 的角色划分、通信、冲突和成本；
- 研究 log、trace、metrics、replay 和可视化；
- 研究 terminal UI 的流式输出、状态栏、工具卡片和审批交互；
- 建立主系统、对照系统和自己的 Agent 的功能矩阵；
- 给每个候选项写“收益、成本、风险、是否集成”。

能力矩阵模板：

| 能力 | Codex | OpenCode | Kimi CLI | 我的 Agent | 是否集成 | 理由 |
|---|---|---|---|---|---|---|
| Context compression |  |  |  |  |  |  |
| Long-term memory |  |  |  |  |  |  |
| Multi-agent |  |  |  |  |  |  |
| Background tasks |  |  |  |  |  |  |
| Skills / Plugins |  |  |  |  |  |  |
| MCP |  |  |  |  |  |  |
| Sandbox |  |  |  |  |  |  |
| Observability |  |  |  |  |  |  |
| Terminal UI |  |  |  |  |  |  |

交付物：

- `reports/feature-matrix.md`；
- `reports/architecture-comparison.md`；
- 集成候选清单。

验收标准：

- 能解释哪些能力是必要的，哪些是特定架构或产品选择；
- 每个集成候选都有明确问题定义；
- 不因为“其他项目有”就默认实现。

---

## 11. 步骤六：选择性集成与交付

### 6.1 选择并集成高级能力

只集成 2–3 个最有价值的高级能力。

推荐顺序：

1. context compression；
2. tool registry / MCP；
3. observability 与 trace replay；
4. background tasks；
5. skills / plugins；
6. 最小 TUI；
7. multi-agent，最后考虑。

任务：

- 为每个新能力写需求和不做范围；
- 先写测试，再接入主循环；
- 保证旧功能回归测试通过；
- 记录新增能力的 token、延迟和成功率；
- 如果收益不明确，撤销该能力。

交付物：

- minimal agent v2；
- 每项能力的测试；
- 变更记录和设计取舍。

验收标准：

- 新增能力不破坏原有闭环；
- 能用指标证明收益；
- 失败时能降级或关闭；
- 代码中没有只为演示存在的死路径。

### 6.2 完成最终评估和文档

任务：

- 跑最终评估任务集；
- 和 v0、v1、v2 对比；
- 写失败分析和未来改进；
- 完成 README 和安装说明；
- 录制或准备 5–10 分钟演示；
- 写最终设计文档；
- 清理无效实验和过时说明。

交付物：

- `reports/final-evaluation.md`；
- `reports/design-document.md`；
- 更新后的 README；
- 演示脚本或演示录屏；
- 最终 v2 标签或 release。

验收标准：

- 新环境按 README 可以运行；
- 至少一个任务可完整演示；
- 至少一个高级能力有前后对比；
- 所有指标和限制都写清楚。

---

## 12. 最小 SWE Agent 技术规格

### 12.1 核心模块

| 模块 | 责任 | 不应承担 |
|---|---|---|
| State | 保存任务、历史、预算、修改记录 | 保存模型内部推理 |
| Prompt Builder | 组装系统提示、任务、工具和历史 | 决定工具是否安全 |
| LLM Client | 调用模型、处理重试和 token 统计 | 执行工具 |
| Parser | 解析和验证模型输出 | 修改系统状态 |
| Registry | 管理工具 schema 和实现 | 绕过权限检查 |
| Executor | 执行工具并标准化结果 | 做高层任务规划 |
| Loop | 驱动状态转移和终止 | 直接操作文件系统 |
| Trace | 记录全过程 | 影响 Agent 决策 |
| Evaluator | 运行任务并计算指标 | 修改任务期望结果 |

### 12.2 工具接口

```python
@dataclass
class ToolResult:
    ok: bool
    content: str
    error: str | None = None
    metadata: dict | None = None
```

所有工具都应返回结构化结果，不能只返回无法区分的字符串。

至少实现：

- `read_file(path, start_line, end_line)`；
- `write_file(path, content)`；
- `list_dir(path)`；
- `search_text(pattern, path)`；
- `run_command(command, timeout_seconds)`。

### 12.3 终止条件

Agent 必须在以下任一情况下停止：

- 模型给出最终答案；
- 达到最大步数；
- 超过 token 预算；
- 超过总时间预算；
- 连续重复同一动作；
- 遇到不可恢复错误；
- 用户取消。

### 12.4 安全边界

最低要求：

- 文件访问限制在指定工作区；
- shell 有工作目录和超时；
- 输出有最大长度；
- 不直接拼接未校验的 shell 字符串；
- 危险命令需要审批或拒绝；
- 每次修改保留 diff；
- 评估环境可重置。

### 12.5 可观测性

每一轮至少记录：

- run_id、task_id、step；
- 当前模型和配置；
- 输入 token、输出 token；
- 模型输出；
- 解析后的 action；
- 工具结果；
- 错误信息；
- 开始和结束时间；
- 最终状态和终止原因。

---

## 13. 评估集设计

### 13.1 任务类型

| 类型 | 示例 | 考察能力 |
|---|---|---|
| 只读分析 | 找到函数入口并解释流程 | 搜索、阅读、总结 |
| 单文件修复 | 修复边界条件 bug | 定位、编辑、测试 |
| 测试失败修复 | 根据 pytest 失败信息修复 | 观察、迭代 |
| 多文件修改 | 修改接口及调用方 | 规划和一致性 |
| 工具失败恢复 | 第一次命令失败后修改命令 | 错误恢复 |
| 上下文压力 | 大文件或长历史下完成任务 | 压缩和检索 |
| 安全边界 | 要求修改工作区外文件 | 权限拒绝和解释 |

### 13.2 指标

- 成功率；
- 平均步数；
- 平均输入和输出 token；
- 平均和 P95 延迟；
- 工具错误率；
- 错误恢复率；
- 重复动作率；
- 越界或危险操作次数，目标为 0；
- 每个成功任务的 token 成本；
- 不同版本之间的回归情况。

---

## 14. 成熟 Codebase 拆解模板

每个功能使用同一模板：

```markdown
# Feature: 功能名称

## 问题
这个功能解决什么问题？

## 入口
用户操作、命令、事件或函数入口是什么？

## 调用链
1. 
2. 
3. 

## 状态和数据结构
- 
- 

## 上下文来源
- 
- 

## 失败与边界
- 超时：
- 取消：
- 重试：
- 回退：

## 测试和证据
- 文件：
- 函数：
- 测试：

## 最小复现
我的核心复现代码或实验。

## 设计取舍
为什么这样做？代价是什么？

## 未解决问题
- 
```

读代码时优先问以下问题：

1. 这个能力的入口在哪里？
2. 状态保存在哪个对象或文件？
3. 主循环何时调用它？
4. 输入上下文从哪里来？
5. 输出为什么会回到模型？
6. 超时、取消、重试怎么处理？
7. 权限边界在哪里？
8. 如何记录日志和指标？
9. 有哪些测试？
10. 我能否写一个最小复现？

不要问“总结整个仓库”，要问“这个具体机制的入口、数据结构和失败路径是什么”。

---

## 15. 综合复现方案

### 方案 A：上下文与工具系统

- context compression；
- tool registry；
- MCP；
- trace replay。

推荐指数：最高。  
原因：直接改善 Agent 的能力和稳定性，且与 Coding Agent 核心架构紧密相关。

### 方案 B：后台任务与可观测性

- background tasks；
- task status；
- streaming output；
- minimal terminal UI。

推荐指数：高。  
原因：适合观察长任务、中断、恢复和用户交互。

### 方案 C：多 Agent 工作流

- planner / executor / reviewer；
- 任务队列；
- 结果合并和冲突处理。

推荐指数：最后考虑。  
原因：如果没有单 Agent 的稳定评估和多 Agent 的清晰收益证明，很容易只增加复杂度和成本。

---

## 16. 常见风险和反模式

| 风险 | 表现 | 处理方式 |
|---|---|---|
| 范围过大 | 同时读三个仓库、学十个功能 | 一个主系统，一个特征，一个复现 |
| AI 代读 | 只收集摘要，不验证源码 | 必须指出文件和函数 |
| 过早优化 | 还没评测就做 memory 和 multi-agent | 先完成 v0 和评估 |
| 过度设计 | 一开始就做插件系统和抽象层 | 三个重复场景后再抽象 |
| 忽略安全 | Agent 可任意写文件和执行命令 | 工作区限制、超时、审批和日志 |
| 过拟合评估 | 针对测试写死答案 | 保留 holdout 任务 |
| 只看成功 | 不分析失败轨迹 | 每个失败都必须分类 |
| 无限重构 | 永远在改架构，无法交付 | 每个步骤必须有可运行产物 |
| 黑盒依赖 | 不知道为什么能跑 | 关键路径写最小复现 |
| 成本失控 | 长历史无限增长 | 预算、压缩、截断和缓存 |

---

## 17. 步骤进度跟踪表

| 步骤 | 子任务状态 | 可验证证据 | 是否通过门槛 | 问题与调整 |
|---|---|---|---|---|
| 1. 打基础与理解概念 | 已完成 | `hello.py`、`toy_react.py` 可运行 | 是 |  |
| 2. 实现最小 SWE Agent | 已完成 | 5 个工具、主循环、安全边界、任务拆分、3 个玩具任务通过 | 是 |  |
| 3. 可靠性、可观察性与评估 | 未开始 |  | 否 |  |
| 4. 上下文工程与 v1 | 未开始 |  | 否 |  |
| 5. 拆解现代 Coding Agent | 未开始 |  | 否 |  |
| 6. 选择性集成与交付 | 未开始 |  | 否 |  |

---

## 18. 启动清单

开始执行时先完成：

- [ ] 创建 `agent-lab`；
- [ ] 创建 Python 项目和虚拟环境；
- [ ] 配置格式化、测试和基础 lint；
- [ ] 写 README 第一版；
- [ ] 建立 `notes/`、`labs/`、`traces/`、`evals/`、`reports/`；
- [ ] 跑通一次 LLM API 调用；
- [ ] 记录第一条 API 请求和响应；
- [ ] 明确第一个要用的模型和配置方式。

完成后直接进入步骤一。

---

## 19. 推荐阅读和参考材料

核心论文和概念：

- ReAct：Reasoning and Acting in Language Models，arXiv:2210.03629；
- SWE-agent：Agent-Computer Interfaces Enable Automated Software Engineering，arXiv:2405.15793；
- SWE-bench：Can Language Models Resolve Real-World GitHub Issues?，arXiv:2310.06770；
- Toolformer、Reflexion、Generative Agents：作为后续扩展阅读；
- Model Context Protocol 规范：研究工具、资源和提示的统一接入。

工程重点：

- LLM API 的 messages、tool calling 和 structured output；
- Python 的 `subprocess`、`pathlib`、`asyncio`、`typing`；
- pytest、JSONL、日志和 trace；
- Git diff、测试驱动修改和工作区隔离；
- sandbox、权限、审批和错误恢复；
- context window、token budget、summary 和 compaction。

---

## 20. 最终验收清单

完成后逐项检查：

- [ ] 能从零调用模型；
- [ ] 能声明工具并解析 tool call；
- [ ] 能执行 terminal 和文件工具；
- [ ] 能驱动多步 Agent loop；
- [ ] 能处理错误、超时、重复和预算；
- [ ] 每次运行都有 trace；
- [ ] 有固定评估任务集；
- [ ] 有成功率、token、延迟和失败分类；
- [ ] 有上下文压缩机制和前后对比；
- [ ] 能定位成熟 Agent 的主循环；
- [ ] 能定位成熟 Agent 的 tool registry 和 executor；
- [ ] 能解释 sandbox、MCP、skills/plugins 的设计取舍；
- [ ] 能说明 memory 和 multi-agent 何时值得实现；
- [ ] 至少集成 2–3 个有指标收益的高级能力；
- [ ] README 可以让新环境复现；
- [ ] 能完成 5–10 分钟演示；
- [ ] 能清楚说明系统限制和未解决问题。

最终判断标准：

> 不是“我实现了很多功能”，而是“我能证明这个最小 Agent 为什么能工作、在哪些情况下失败、现代系统如何解决这些问题，以及哪些解决方案值得引入自己的系统”。