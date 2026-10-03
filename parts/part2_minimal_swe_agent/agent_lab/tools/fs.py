"""基础文件系统工具。"""

from pathlib import Path

from .workspace import resolve_workspace_path

SENSITIVE_FILES = {".env"}


def _is_sensitive(target: Path) -> bool:
    return target.name in SENSITIVE_FILES


def list_dir(path: str) -> dict:
    """列出目录内容，返回结构化结果。"""
    target = resolve_workspace_path(path)

    if not target.exists():
        return {"ok": False, "error": f"path does not exist: {path}"}

    if not target.is_dir():
        return {"ok": False, "error": f"not a directory: {path}"}

    try:
        entries = []
        for child in sorted(target.iterdir()):
            entries.append(
                {
                    "name": child.name,
                    "type": "dir" if child.is_dir() else "file",
                }
            )
        return {"ok": True, "path": str(target), "entries": entries}
    except OSError as exc:
        return {"ok": False, "error": str(exc)}


def read_file(path: str, start_line: int | None = None, end_line: int | None = None) -> dict:
    """读取文件内容，可指定行范围。"""
    target = resolve_workspace_path(path)

    if _is_sensitive(target):
        return {"ok": False, "error": "access to sensitive file is not allowed"}

    if not target.exists():
        return {"ok": False, "error": f"path does not exist: {path}"}

    if not target.is_file():
        return {"ok": False, "error": f"not a file: {path}"}

    try:
        text = target.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()

        if start_line is None:
            start_line = 1
        if end_line is None:
            end_line = len(lines)

        selected = lines[start_line - 1 : end_line]
        content = "\n".join(selected)

        return {
            "ok": True,
            "path": str(target),
            "start_line": start_line,
            "end_line": min(end_line, len(lines)),
            "total_lines": len(lines),
            "content": content,
        }
    except OSError as exc:
        return {"ok": False, "error": str(exc)}


def write_file(path: str, content: str) -> dict:
    """把内容写入文件。"""
    target = resolve_workspace_path(path)

    if _is_sensitive(target):
        return {"ok": False, "error": "access to sensitive file is not allowed"}

    try:
        target.write_text(content, encoding="utf-8")
        return {"ok": True, "path": str(target), "bytes_written": target.stat().st_size}
    except OSError as exc:
        return {"ok": False, "error": str(exc)}


def search_text(pattern: str, path: str, max_matches: int = 50) -> dict:
    """在文件或目录中搜索包含 pattern 的文本行。"""
    target = resolve_workspace_path(path)

    if _is_sensitive(target):
        return {"ok": False, "error": "access to sensitive file is not allowed"}

    if not target.exists():
        return {"ok": False, "error": f"path does not exist: {path}"}

    if target.is_file():
        files = [target]
    elif target.is_dir():
        files = sorted(
            p
            for p in target.rglob("*")
            if p.is_file()
            and not p.name.startswith(".")
            and "__pycache__" not in p.parts
            and ".git" not in p.parts
            and ".pytest_cache" not in p.parts
        )
    else:
        return {"ok": False, "error": f"not a file or directory: {path}"}

    matches = []
    truncated = False

    for file in files:
        try:
            lines = file.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue

        for line_number, line in enumerate(lines, start=1):
            if pattern in line:
                matches.append(
                    {
                        "file": str(file),
                        "line": line_number,
                        "content": line,
                    }
                )
                if len(matches) >= max_matches:
                    truncated = True
                    break

        if truncated:
            break

    return {
        "ok": True,
        "pattern": pattern,
        "path": str(target),
        "match_count": len(matches),
        "truncated": truncated,
        "matches": matches,
    }