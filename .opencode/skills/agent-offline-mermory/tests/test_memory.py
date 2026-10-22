import importlib.util
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("writer", Path(__file__).parents[1] / "scripts/write-memory.py")
w = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(w)


class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "memory"
        w.SETTINGS_PATH = Path(self.temp.name) / "settings.json"

    def test_four_types_and_task_state(self):
        w.initialize_memory_root(str(self.root), False)
        for kind in ("Experience", "Principle", "Daily"):
            note = w.capture_note(kind, "测试", "事实内容", None)
            self.assertNotIn("{{", Path(note["path"]).read_text(encoding="utf-8"))
        note = w.capture_note("Task", "压测", "- 状态：doing\n- 行动：运行压测", None)
        self.assertEqual(w.query_notes("", "task", "doing", 10)["count"], 1)
        w.capture_note("Task", "压测完成", "- 状态：done\n- 行动：归档报告", note["path"])
        self.assertEqual(w.query_notes("", "task", "done", 10)["count"], 1)
        updated = Path(note["path"]).read_text(encoding="utf-8")
        self.assertNotIn("- 状态：doing", updated)
        self.assertEqual(updated.count("- 行动："), 1)
        self.assertEqual(w.query_notes("", "all", "all", 10)["count"], 4)
        index = self.root / "Task/_index.md"
        self.assertIn("done", index.read_text(encoding="utf-8"))
        self.assertNotIn("](Task/", index.read_text(encoding="utf-8"))

    def test_migration_preserves_bodies_and_links(self):
        for kind in ("Tasks", "Knowledge"):
            directory = self.root / kind
            directory.mkdir(parents=True)
            (directory / "same.md").write_text("---\ntype: agent-task\n---\n# 原文\n内容", encoding="utf-8")
        (self.root / "links.md").write_text("[任务](Tasks/same.md) [[Knowledge/same]]", encoding="utf-8")
        result = w.initialize_memory_root(str(self.root), False)
        self.assertEqual(result["migration"]["count"], 2)
        self.assertFalse((self.root / "Tasks").exists())
        self.assertEqual(w.query_notes("", "experience", "all", 10)["count"], 2)
        self.assertEqual(w.query_notes("", "task", "all", 10)["count"], 0)
        self.assertIn("agent-experience", (self.root / "Experience/Tasks/same.md").read_text(encoding="utf-8"))
        self.assertIn("Experience/Tasks/same.md", (self.root / "links.md").read_text(encoding="utf-8"))
        self.assertTrue(Path(result["migration"]["backup"]).is_dir())
        self.assertEqual(w.initialize_memory_root(str(self.root), False)["migration"]["count"], 0)

    def test_migration_collision_stops_without_moving(self):
        (self.root / "Tasks").mkdir(parents=True)
        (self.root / "Experience/Tasks").mkdir(parents=True)
        with self.assertRaises(w.WriterError):
            w.initialize_memory_root(str(self.root), False)
        self.assertTrue((self.root / "Tasks").exists())

    def test_obsidian_and_escape(self):
        self.root.mkdir()
        (self.root / ".obsidian").mkdir()
        result = w.initialize_memory_root(str(self.root), True)
        self.assertIn("agent-principle", Path(result["dashboard"]).read_text(encoding="utf-8"))
        outside = Path(self.temp.name) / "outside.md"
        outside.write_text("private", encoding="utf-8")
        with self.assertRaises(w.WriterError):
            w.capture_note("Task", "bad", "content", str(outside))
        self.assertEqual(outside.read_text(encoding="utf-8"), "private")


if __name__ == "__main__":
    unittest.main()
