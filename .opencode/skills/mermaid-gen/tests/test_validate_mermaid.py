from __future__ import annotations

import os
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_validator(*args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(ROOT / "scripts" / "validate_mermaid.py"), *args],
        cwd=ROOT,
        env=env,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )


class ValidateMermaidCliTests(unittest.TestCase):
    def test_valid_themed_block_passes_structure_check(self) -> None:
        markdown = """# 示例

```mermaid
%%{init: {"theme": "base"}}%%
flowchart LR
    A[开始] --> B[完成]
```
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "valid.md"
            path.write_text(markdown, encoding="utf-8")
            result = run_validator(str(path))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_theme_fails(self) -> None:
        markdown = """```mermaid
flowchart LR
    A --> B
```
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "invalid.md"
            path.write_text(markdown, encoding="utf-8")
            result = run_validator(str(path))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("init", result.stdout)

    def test_examples_cover_declared_types(self) -> None:
        result = run_validator(str(ROOT / "examples"), "--check-coverage")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_skill_folder_is_standalone(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "mermaid-gen"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            result = subprocess.run(
                [sys.executable, "-X", "utf8", str(copy / "scripts" / "validate_mermaid.py"), str(copy / "examples"), "--check-coverage"],
                cwd=copy,
                text=True,
                encoding="utf-8",
                capture_output=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_fallback_renderer_version_is_pinned(self) -> None:
        script = (ROOT / "scripts" / "validate_mermaid.py").read_text(encoding="utf-8")
        self.assertIn("@mermaid-js/mermaid-cli@11.16.0", script)

    def test_mermaid_diagram_plan_rejects_duplicate_ids_and_bad_references(self) -> None:
        plan = {"designSystemVersion": "1.0", "renderer": "mermaid", "type": "flowchart", "theme": "light", "title": "流程", "nodes": [{"id": "a", "label": "A"}, {"id": "a", "label": "B"}], "edges": [{"id": "e", "source": "a", "target": "missing"}]}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "plan.json"
            path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run([sys.executable, "-X", "utf8", str(ROOT / "scripts" / "validate_plan.py"), str(path)], cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("不得重复", result.stdout)
        self.assertIn("引用不存在", result.stdout)


if __name__ == "__main__":
    unittest.main()
