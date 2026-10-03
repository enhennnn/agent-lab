"""用 3 个玩具仓库任务验收 minimal SWE Agent。"""

import json
import subprocess
import sys
from pathlib import Path

from .agent import call_deepseek
from .loop import make_plan, run_agent
from .tools.registry import build_default_registry
from .tools.workspace import set_workspace_root

PROJECT_ROOT = Path(__file__).resolve().parents[3]
TASKS_ROOT = PROJECT_ROOT / "evals" / "tasks"


def run_task(task_id: str, max_steps: int = 15) -> dict:
    task_dir = TASKS_ROOT / task_id
    config = json.loads((task_dir / "task.json").read_text(encoding="utf-8"))
    repo = task_dir / "repo"

    set_workspace_root(repo)

    plan = make_plan(config["instruction"], call_deepseek)
    state = run_agent(
        config["instruction"],
        build_default_registry(),
        call_deepseek,
        max_steps=max_steps,
        plan=plan,
    )

    verify = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=str(repo),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    return {
        "task_id": task_id,
        "passed": verify.returncode == 0,
        "steps": state.step,
        "final_answer": state.final_answer,
        "verify_stdout": verify.stdout,
        "verify_stderr": verify.stderr,
    }


def main() -> int:
    task_ids = [
        "task_001_fix_typo",
        "task_002_fix_test",
        "task_003_multi_file",
        "task_004_syntax_error",
    ]

    for task_id in task_ids:
        result = run_task(task_id)
        print("=" * 60)
        print(f"Task: {task_id}")
        print(f"Passed: {result['passed']}")
        print(f"Steps: {result['steps']}")
        print("Final answer:")
        print(result["final_answer"])
        print("Verification stdout:")
        print(result["verify_stdout"])
        if result["verify_stderr"]:
            print("Verification stderr:")
            print(result["verify_stderr"])
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())