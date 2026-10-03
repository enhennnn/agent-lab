"""让 pytest 能找到 parts 下的各模块，并重置工作区。"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / "parts"
PART1 = PARTS / "part1_basics_and_concepts"
PART2 = PARTS / "part2_minimal_swe_agent"

for path in (ROOT, PARTS, PART2):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))


@pytest.fixture(autouse=True)
def _reset_workspace_root():
    from agent_lab.tools.workspace import reset_workspace_root

    reset_workspace_root()
    yield
    reset_workspace_root()