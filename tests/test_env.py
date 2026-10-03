"""验证项目配置模板存在。"""

from pathlib import Path

# 检查.env.exampele是否存在
def test_env_example_exists():
    assert Path(".env.example").exists()

# 检查.env.exampele里是否包含DEEPSEEK_API_KEY
def test_env_example_contains_key():
    content = Path(".env.example").read_text(encoding="utf-8")
    assert "DEEPSEEK_API_KEY" in content