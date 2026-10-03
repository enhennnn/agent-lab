"""terminal 工具：执行 shell 命令。"""

import subprocess

from .workspace import resolve_workspace_path


def run_command(
    command: str,
    cwd: str = ".",
    timeout_seconds: int = 60,
    max_output_chars: int = 2000,
) -> dict:
    """执行一条 shell 命令，并限制超时和输出长度。"""
    if not isinstance(command, str) or not command.strip():
        return {"ok": False, "error": "command must be a non-empty string"}

    try:
        workdir = resolve_workspace_path(cwd)
    except PermissionError as exc:
        return {"ok": False, "error": str(exc)}

    if not workdir.exists():
        return {"ok": False, "error": f"cwd does not exist: {cwd}"}

    if not workdir.is_dir():
        return {"ok": False, "error": f"cwd is not a directory: {cwd}"}

    try:
        completed = subprocess.run(
            command,
            cwd=str(workdir),
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "error": f"command timed out after {timeout_seconds} seconds",
        }
    except OSError as exc:
        return {"ok": False, "error": str(exc)}

    stdout = completed.stdout or ""
    stderr = completed.stderr or ""

    stdout_truncated = len(stdout) > max_output_chars
    stderr_truncated = len(stderr) > max_output_chars

    return {
        "ok": completed.returncode == 0,
        "returncode": completed.returncode,
        "stdout": stdout[:max_output_chars],
        "stderr": stderr[:max_output_chars],
        "stdout_truncated": stdout_truncated,
        "stderr_truncated": stderr_truncated,
    }