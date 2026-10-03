"""测试文件系统工具和工具注册表。"""

import pytest

from agent_lab.tools.fs import list_dir, read_file, search_text, write_file
from agent_lab.tools.registry import ToolRegistry, build_default_registry
from agent_lab.tools.workspace import resolve_workspace_path, set_workspace_root


def test_list_dir_returns_entries(tmp_path):
    set_workspace_root(tmp_path)
    (tmp_path / "a.txt").write_text("hello", encoding="utf-8")
    (tmp_path / "sub").mkdir()

    result = list_dir(str(tmp_path))

    assert result["ok"] is True
    names = {entry["name"] for entry in result["entries"]}
    assert names == {"a.txt", "sub"}


def test_list_dir_missing_path(tmp_path):
    set_workspace_root(tmp_path)
    result = list_dir(str(tmp_path / "missing"))

    assert result["ok"] is False
    assert "error" in result


def test_read_file_range(tmp_path):
    set_workspace_root(tmp_path)
    path = tmp_path / "sample.txt"
    path.write_text("line1\nline2\nline3\n", encoding="utf-8")

    result = read_file(str(path), start_line=2, end_line=3)

    assert result["ok"] is True
    assert result["content"] == "line2\nline3"


def test_write_file(tmp_path):
    set_workspace_root(tmp_path)
    path = tmp_path / "out.txt"

    result = write_file(str(path), "hello world")

    assert result["ok"] is True
    assert path.read_text(encoding="utf-8") == "hello world"


def test_search_text_in_file(tmp_path):
    set_workspace_root(tmp_path)
    path = tmp_path / "code.py"
    path.write_text("def hello():\n    return 1\n\nhello()\n", encoding="utf-8")

    result = search_text("hello", str(path))

    assert result["ok"] is True
    assert result["match_count"] == 2


def test_search_text_in_directory(tmp_path):
    set_workspace_root(tmp_path)
    (tmp_path / "a.txt").write_text("alpha\nbeta\n", encoding="utf-8")
    (tmp_path / "b.txt").write_text("gamma\nalpha\n", encoding="utf-8")

    result = search_text("alpha", str(tmp_path))

    assert result["ok"] is True
    assert result["match_count"] == 2


def test_search_text_missing_path(tmp_path):
    set_workspace_root(tmp_path)
    result = search_text("x", str(tmp_path / "missing"))

    assert result["ok"] is False
    assert "error" in result


def test_registry_execute_unknown_tool():
    registry = ToolRegistry()
    result = registry.execute("does_not_exist", {})

    assert result["ok"] is False
    assert "unknown tool" in result["error"]


def test_default_registry_has_tools():
    registry = build_default_registry()

    specs = registry.to_openai_specs()
    names = {spec["function"]["name"] for spec in specs}

    assert {"list_dir", "read_file", "write_file", "search_text", "run_command"} <= names


def test_resolve_rejects_outside_path(tmp_path):
    set_workspace_root(tmp_path)
    outside = tmp_path.parent / "outside"

    with pytest.raises(PermissionError):
        resolve_workspace_path(str(outside))


def test_registry_rejects_outside_path(tmp_path):
    set_workspace_root(tmp_path)
    registry = build_default_registry()

    result = registry.execute("list_dir", {"path": str(tmp_path.parent)})

    assert result["ok"] is False
    assert "outside workspace" in result["error"]


def test_read_file_rejects_env(tmp_path):
    set_workspace_root(tmp_path)
    (tmp_path / ".env").write_text("DEEPSEEK_API_KEY=secret", encoding="utf-8")

    result = read_file(str(tmp_path / ".env"))

    assert result["ok"] is False
    assert "sensitive" in result["error"]


def test_write_file_rejects_env(tmp_path):
    set_workspace_root(tmp_path)

    result = write_file(str(tmp_path / ".env"), "DEEPSEEK_API_KEY=secret")

    assert result["ok"] is False
    assert "sensitive" in result["error"]


def test_search_text_skips_dotfiles(tmp_path):
    set_workspace_root(tmp_path)
    (tmp_path / ".env").write_text("DEEPSEEK_API_KEY=secret", encoding="utf-8")
    (tmp_path / "code.py").write_text("DEEPSEEK_API_KEY=placeholder", encoding="utf-8")

    result = search_text("DEEPSEEK_API_KEY", str(tmp_path))

    assert result["ok"] is True
    assert result["match_count"] == 1
    assert result["matches"][0]["file"].endswith("code.py")