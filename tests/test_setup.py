"""检查第一部分的配置和 hello.py。"""

from pathlib import Path

from part1_basics_and_concepts import hello

ROOT = Path(__file__).resolve().parents[1]


def test_env_example_has_api_key_placeholder():
    content = (ROOT / ".env.example").read_text(encoding="utf-8")
    assert "DEEPSEEK_API_KEY=" in content


def test_gitignore_ignores_env_file():
    content = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert ".env" in content.splitlines()


def test_load_api_key_returns_none_or_string():
    key = hello.load_api_key()
    assert key is None or isinstance(key, str)