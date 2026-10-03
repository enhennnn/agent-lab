"""Agent 状态。"""

from dataclasses import dataclass, field


@dataclass
class AgentState:
    task: str
    plan: str | None = None
    messages: list[dict] = field(default_factory=list)
    max_steps: int = 10
    step: int = 0
    observations: list[dict] = field(default_factory=list)
    final_answer: str | None = None
    terminated_reason: str | None = None