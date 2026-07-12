from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INIT = '%%{init: {"theme":"base","themeVariables":{"fontFamily":"Inter, sans-serif"}}}%%'


def run_validator(*args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(ROOT / "scripts" / "validate_mermaid.py"), *args],
        cwd=ROOT, env=env, text=True, encoding="utf-8", capture_output=True, check=False,
    )


def validate_text(markdown: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as temporary:
        path = Path(temporary) / "diagram.md"
        path.write_text(markdown, encoding="utf-8")
        return run_validator(str(path))


class ValidateMermaidCliTests(unittest.TestCase):
    def test_valid_flowchart_passes(self) -> None:
        result = validate_text(f"```mermaid\n{INIT}\nflowchart LR\n A[开始] --> B[结束]\n```\n")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unclosed_mermaid_fence_fails(self) -> None:
        result = validate_text(f"```mermaid\n{INIT}\nflowchart LR\n A[开始] --> B[结束]\n")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("未闭合", result.stdout)

    def test_multiple_blocks_fail(self) -> None:
        block = f"```mermaid\n{INIT}\nflowchart LR\n A[开始] --> B[结束]\n```\n"
        result = validate_text(block + block)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("只允许一个", result.stdout)

    def test_missing_theme_fails(self) -> None:
        result = validate_text("```mermaid\nflowchart LR\n A[开始] --> B[结束]\n```\n")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("init", result.stdout)

    def test_flowchart_requires_start_and_end(self) -> None:
        result = validate_text(f"```mermaid\n{INIT}\nflowchart LR\n A[提交] --> B[完成]\n```\n")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("开始和结束", result.stdout)

    def test_sequence_requires_participants_and_messages(self) -> None:
        result = validate_text(f"```mermaid\n{INIT}\nsequenceDiagram\n participant A\n```\n")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("两个参与者", result.stdout)

    def test_state_requires_initial_and_final(self) -> None:
        result = validate_text(f"```mermaid\n{INIT}\nstateDiagram-v2\n [*] --> 运行\n```\n")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("终止状态", result.stdout)

    def test_er_requires_cardinality(self) -> None:
        source = "erDiagram\n A {\n string id\n }\n B {\n string id\n }"
        result = validate_text(f"```mermaid\n{INIT}\n{source}\n```\n")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("关系基数", result.stdout)

    def test_gantt_requires_date_format(self) -> None:
        result = validate_text(f"```mermaid\n{INIT}\ngantt\n title 计划\n 任务 :2026-01-01, 1d\n```\n")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("dateFormat", result.stdout)

    def test_examples_cover_declared_types(self) -> None:
        result = run_validator(str(ROOT / "examples"), "--check-coverage")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_skill_folder_is_standalone(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            copy = Path(temporary) / "mermaid-gen"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            result = subprocess.run(
                [sys.executable, "-X", "utf8", str(copy / "scripts" / "validate_mermaid.py"), str(copy / "examples"), "--check-coverage"],
                cwd=copy, text=True, encoding="utf-8", capture_output=True, check=False,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_renderer_version_is_pinned(self) -> None:
        script = (ROOT / "scripts" / "validate_mermaid.py").read_text(encoding="utf-8")
        self.assertIn("@mermaid-js/mermaid-cli@11.16.0", script)


if __name__ == "__main__":
    unittest.main()
