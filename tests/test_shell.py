"""测试 run_command 工具。"""

import sys

from agent_lab.tools.shell import run_command
from agent_lab.tools.workspace import set_workspace_root


def test_run_command_success():
    command = f'"{sys.executable}" -c "print(123)"'
    result = run_command(command)

    assert result["ok"] is True
    assert result["returncode"] == 0
    assert "123" in result["stdout"]


def test_run_command_nonzero_exit():
    command = f'"{sys.executable}" -c "import sys; sys.exit(3)"'
    result = run_command(command)

    assert result["ok"] is False
    assert result["returncode"] == 3


def test_run_command_timeout():
    command = f'"{sys.executable}" -c "import time; time.sleep(5)"'
    result = run_command(command, timeout_seconds=1)

    assert result["ok"] is False
    assert "timed out" in result["error"]


def test_run_command_missing_cwd(tmp_path):
    result = run_command("echo hi", cwd=str(tmp_path / "missing"))

    assert result["ok"] is False
    assert "error" in result


def test_run_command_truncates_output():
    command = f'"{sys.executable}" -c "print(\'x\' * 1000)"'
    result = run_command(command, max_output_chars=10)

    assert result["ok"] is True
    assert len(result["stdout"]) <= 10
    assert result["stdout_truncated"] is True