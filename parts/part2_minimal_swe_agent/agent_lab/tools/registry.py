"""工具注册表：统一管理工具定义、工具实现和工具执行。"""

from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class Tool:
    name: str
    description: str
    parameters: dict
    func: Callable[..., dict]

    def to_openai_spec(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def to_openai_specs(self) -> list[dict]:
        return [tool.to_openai_spec() for tool in self._tools.values()]

    def execute(self, name: str, arguments: dict[str, Any]) -> dict:
        tool = self.get(name)
        if tool is None:
            return {"ok": False, "error": f"unknown tool: {name}"}

        try:
            return tool.func(**arguments)
        except Exception as exc:  # noqa: BLE001 - 工具边界需要兜底
            return {"ok": False, "error": str(exc)}


def build_default_registry() -> ToolRegistry:
    from .fs import list_dir, read_file, search_text, write_file
    from .shell import run_command

    registry = ToolRegistry()

    registry.register(
        Tool(
            name="list_dir",
            description="列出指定目录下的文件和文件夹。",
            parameters={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "要查看的目录路径",
                    }
                },
                "required": ["path"],
            },
            func=list_dir,
        )
    )

    registry.register(
        Tool(
            name="read_file",
            description="读取文件内容，可选指定行范围。",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "要读取的文件路径"},
                    "start_line": {"type": "integer", "description": "起始行号，从 1 开始，可选"},
                    "end_line": {"type": "integer", "description": "结束行号，包含该行，可选"},
                },
                "required": ["path"],
            },
            func=read_file,
        )
    )

    registry.register(
        Tool(
            name="write_file",
            description="把内容写入文件。",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "要写入的文件路径"},
                    "content": {"type": "string", "description": "要写入的完整文本内容"},
                },
                "required": ["path", "content"],
            },
            func=write_file,
        )
    )

    registry.register(
        Tool(
            name="search_text",
            description="在文件或目录中搜索包含指定文本的行。",
            parameters={
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "要搜索的文本"},
                    "path": {"type": "string", "description": "文件或目录路径"},
                    "max_matches": {"type": "integer", "description": "最大匹配数量，默认 50，可选"},
                },
                "required": ["pattern", "path"],
            },
            func=search_text,
        )
    )

    registry.register(
        Tool(
            name="run_command",
            description="执行一条 shell 命令，并返回退出码、stdout 和 stderr。",
            parameters={
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "要执行的 shell 命令"},
                    "cwd": {"type": "string", "description": "工作目录，默认当前目录，可选"},
                    "timeout_seconds": {"type": "integer", "description": "超时秒数，默认 60，可选"},
                    "max_output_chars": {"type": "integer", "description": "输出最大字符数，默认 2000，可选"},
                },
                "required": ["command"],
            },
            func=run_command,
        )
    )

    return registry