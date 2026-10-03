"""工作区安全边界。

所有文件工具都应该通过 resolve_workspace_path 解析路径，
确保只能访问工作区内的文件。
"""

import os
from pathlib import Path

_workspace_root: Path | None = None


def get_workspace_root() -> Path:
    """返回当前工作区根目录。"""
    if _workspace_root is not None:
        return _workspace_root

    env_root = os.getenv("AGENT_WORKSPACE_ROOT")
    if env_root:
        return Path(env_root).resolve()

    return Path.cwd().resolve()


def set_workspace_root(path: str | Path) -> None:
    """设置工作区根目录。"""
    global _workspace_root
    _workspace_root = Path(path).resolve()


def reset_workspace_root() -> None:
    """恢复为默认工作区（当前目录）。"""
    global _workspace_root
    _workspace_root = None


def resolve_workspace_path(path: str | Path) -> Path:
    """把路径解析到工作区内；越界时抛出 PermissionError。"""
    root = get_workspace_root()
    target = Path(path)

    if not target.is_absolute():
        target = root / target

    target = target.resolve()

    if target != root and root not in target.parents:
        raise PermissionError(f"path is outside workspace: {path}")

    return target