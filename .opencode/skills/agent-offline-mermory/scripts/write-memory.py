#!/usr/bin/env python3
"""agent-offline-mermory 的跨平台写入器。"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


SKILL_ROOT = Path(__file__).resolve().parent.parent
SETTINGS_PATH = SKILL_ROOT / "settings.json"
TEMPLATE_ROOT = SKILL_ROOT / "assets" / "templates"
RECORD_TYPES = {"inbox": "Inbox", "task": "Task", "knowledge": "Knowledge"}
QUERY_DIRECTORIES = {
    "inbox": ("Inbox",),
    "task": ("Tasks",),
    "knowledge": ("Knowledge",),
    "all": ("Inbox", "Tasks", "Knowledge"),
}
WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}
DEFAULT_REQUIRE_OBSIDIAN = True
DEFAULT_EXPERIENCE_MODE = "auto"
INDEX_FILENAME = "_index.md"


class WriterError(RuntimeError):
    """可预期的参数校验或配置错误。"""


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_timestamp(value: datetime) -> str:
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


def normalized_path(value: Union[str, os.PathLike]) -> Path:
    text = os.fspath(value).strip()
    if not text:
        raise WriterError("路径不能为空。")
    return Path(text).expanduser().resolve(strict=False)


def assert_path_within_root(candidate: Path, root: Path) -> Path:
    candidate_full = candidate.resolve(strict=False)
    root_full = root.resolve(strict=False)
    try:
        candidate_full.relative_to(root_full)
    except ValueError as exc:
        raise WriterError(
            f"拒绝访问已配置记忆根目录之外的路径："
            f"{candidate_full}"
        ) from exc
    return candidate_full


def find_obsidian_vault(start_path: Path) -> Path:
    cursor = start_path.resolve(strict=False)
    while True:
        if (cursor / ".obsidian").is_dir():
            return cursor
        if cursor.parent == cursor:
            break
        cursor = cursor.parent
    raise WriterError(f"目标路径及其父目录中未找到 .obsidian：{start_path}")


def write_utf8(path: Path, value: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(value)


def append_utf8(path: Path, value: str) -> None:
    with path.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(value)


def render_template(template_name: str, values: Dict[str, str]) -> str:
    template_path = TEMPLATE_ROOT / template_name
    if not template_path.is_file():
        raise WriterError(f"缺少模板文件：{template_path}")
    rendered = template_path.read_text(encoding="utf-8")
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    return rendered


def save_settings(
    root: Path,
    vault_root: Path,
    require_obsidian: bool,
    experience_mode: str,
) -> None:
    settings = {
        "schema_version": 1,
        "memory_root": str(root),
        "vault_root": str(vault_root),
        "require_obsidian": require_obsidian,
        "experience_mode": experience_mode,
        "updated": iso_timestamp(utc_now()),
    }
    write_utf8(
        SETTINGS_PATH,
        json.dumps(settings, ensure_ascii=False, indent=2) + "\n",
    )


def get_settings() -> Dict[str, Any]:
    if not SETTINGS_PATH.is_file():
        raise WriterError("Skill 尚未初始化，请先执行 init 初始化记忆根目录。")
    try:
        settings = json.loads(SETTINGS_PATH.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise WriterError(f"无法读取配置文件：{SETTINGS_PATH}：{exc}") from exc
    if not str(settings.get("memory_root", "")).strip():
        raise WriterError(f"配置文件缺少 memory_root：{SETTINGS_PATH}")
    settings.setdefault("require_obsidian", True)
    settings.setdefault("experience_mode", "auto")
    return settings


def initialize_memory_root(
    root_value: str,
    require_obsidian: bool = DEFAULT_REQUIRE_OBSIDIAN,
    experience_mode: str = DEFAULT_EXPERIENCE_MODE,
) -> Dict[str, Any]:
    root = normalized_path(root_value)
    if require_obsidian:
        vault_root = find_obsidian_vault(root)
    else:
        vault_root = ""

    root.mkdir(parents=True, exist_ok=True)
    for directory_name in ("Inbox", "Tasks", "Knowledge"):
        (root / directory_name).mkdir(parents=True, exist_ok=True)

    root_name = root.name or "AgentMemory"
    dashboard_path = root / f"{root_name}.md"
    if not dashboard_path.exists():
        dashboard = render_template(
            "dashboard.md",
            {"timestamp": iso_timestamp(utc_now()), "name": root_name},
        )
        write_utf8(dashboard_path, dashboard.rstrip() + "\n")

    refresh_memory_indexes(root)
    save_settings(root, vault_root, require_obsidian, experience_mode)
    return {
        "success": True,
        "action": "initialized",
        "memory_root": str(root),
        "vault_root": str(vault_root),
        "require_obsidian": require_obsidian,
        "experience_mode": experience_mode,
        "dashboard": str(dashboard_path),
    }


def refresh_memory_indexes(root: Path) -> None:
    now = utc_now()
    for directory_name, index_title in (("Tasks", "任务索引"), ("Knowledge", "知识索引")):
        directory = root / directory_name
        if not directory.is_dir():
            continue

        rows: List[Tuple[datetime, str, str, str]] = []
        for candidate in sorted(directory.rglob("*.md")):
            if candidate.name == INDEX_FILENAME:
                continue
            resolved = candidate.resolve(strict=True)
            assert_path_within_root(resolved, root)
            if not resolved.is_file():
                continue
            content = resolved.read_text(encoding="utf-8-sig")
            frontmatter = parse_frontmatter(content)
            title = note_title(resolved, content)
            status = note_status(frontmatter)
            modified = datetime.fromtimestamp(
                resolved.stat().st_mtime, tz=timezone.utc
            )
            relative = os.path.relpath(resolved, root).replace("\\", "/")
            rows.append((modified, status, title, relative))

        rows.sort(key=lambda row: row[0], reverse=True)
        lines = ["| 状态 | 标题 | 更新时间 | 文件 |", "| --- | --- | --- | --- |"]
        for modified, status, title, relative in rows:
            safe_title = title.replace("|", "\\|")
            lines.append(
                f"| {status} | {safe_title} | {modified.strftime('%Y-%m-%d %H:%M')} "
                f"| [{title}]({relative}) |"
            )
        body = "\n".join(lines) + "\n" if rows else "（暂无记录）\n"
        document = (
            "---\n"
            "type: agent-memory-index\n"
            f'updated: "{iso_timestamp(now)}"\n'
            "---\n\n"
            f"# {index_title}\n\n"
            f"{body}"
        )
        write_utf8(directory / INDEX_FILENAME, document)


def safe_title(value: Optional[str]) -> str:
    clean = (value or "未命名记录").strip()
    clean = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "-", clean)
    clean = re.sub(r"\s+", "-", clean)
    clean = re.sub(r"-+", "-", clean).strip(" .-")
    if not clean:
        clean = "未命名记录"
    if clean.upper() in WINDOWS_RESERVED_NAMES:
        clean = "_" + clean
    return clean[:72].rstrip(" .-") or "未命名记录"


def resolve_existing_target(value: str, root: Path) -> Path:
    target = value.strip()
    if target.startswith("[[") and target.endswith("]]"):
        target = target[2:-2]
        target = target.split("|", 1)[0]
        target = target.split("#", 1)[0]
    if not Path(target).suffix:
        target += ".md"

    target_path = Path(target).expanduser()
    candidate = target_path if target_path.is_absolute() else root / target_path
    candidate = assert_path_within_root(candidate, root)
    if not candidate.is_file():
        raise WriterError(f"用户明确指定的目标文档不存在：{candidate}")
    if candidate.suffix.lower() != ".md":
        raise WriterError(f"目标文档必须是 Markdown 文件：{candidate}")

    resolved_existing = candidate.resolve(strict=True)
    assert_path_within_root(resolved_existing, root)
    return resolved_existing


def new_note_path(directory: Path, title: str, now: datetime) -> Path:
    base_name = f"{now.strftime('%Y-%m-%d-%H%M%S')}-{title}"
    candidate = directory / f"{base_name}.md"
    suffix = 2
    while candidate.exists():
        candidate = directory / f"{base_name}-{suffix}.md"
        suffix += 1
    return candidate


def capture_note(
    record_type: str,
    title: Optional[str],
    content: str,
    target_file: Optional[str],
) -> Dict[str, Any]:
    if not content.strip():
        raise WriterError("记录内容不能为空。")

    settings = get_settings()
    root = normalized_path(str(settings["memory_root"]))
    if not root.is_dir():
        raise WriterError(f"已配置的记忆根目录不存在，请重新初始化：{root}")

    now = utc_now()
    timestamp = iso_timestamp(now)
    default_titles = {
        "Inbox": "临时记录",
        "Task": "任务交接",
        "Knowledge": "知识记录",
    }
    record_title = (title or default_titles[record_type]).strip()

    if target_file and target_file.strip():
        target_path = resolve_existing_target(target_file, root)
        update = (
            f"\n\n## 更新 - {timestamp} - {record_title}\n\n"
            f"{content.strip()}\n"
        )
        append_utf8(target_path, update)
        result = {
            "success": True,
            "action": "updated",
            "type": record_type,
            "path": str(target_path),
        }
    else:
        title_for_filename = safe_title(record_title)
        if record_type == "Inbox":
            inbox_directory = assert_path_within_root(root / "Inbox", root)
            inbox_directory.mkdir(parents=True, exist_ok=True)
            target_path = inbox_directory / f"{now.strftime('%Y-%m-%d')}.md"
            entry = render_template(
                "inbox-entry.md",
                {
                    "timestamp": timestamp,
                    "title": record_title,
                    "content": content.strip(),
                },
            )
            if target_path.exists():
                append_utf8(target_path, "\n\n" + entry.rstrip() + "\n")
                result_action = "updated"
            else:
                document = f"# {now.strftime('%Y-%m-%d')}\n\n{entry.rstrip()}\n"
                write_utf8(target_path, document)
                result_action = "created"
        else:
            directory_name = "Tasks" if record_type == "Task" else "Knowledge"
            template_name = (
                "task-handoff.md" if record_type == "Task" else "knowledge-note.md"
            )
            destination = assert_path_within_root(root / directory_name, root)
            destination.mkdir(parents=True, exist_ok=True)
            target_path = new_note_path(destination, title_for_filename, now)
            document = render_template(
                template_name,
                {
                    "timestamp": timestamp,
                    "title": record_title,
                    "content": content.strip(),
                },
            )
            write_utf8(target_path, document.rstrip() + "\n")
            result_action = "created"
        result = {
            "success": True,
            "action": result_action,
            "type": record_type,
            "path": str(target_path),
        }

    refresh_memory_indexes(root)
    return result


def parse_frontmatter(content: str) -> Dict[str, str]:
    if not content.startswith("---\n"):
        return {}
    closing = content.find("\n---", 4)
    if closing < 0:
        return {}

    values: Dict[str, str] = {}
    for line in content[4:closing].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip().lower()] = value.strip().strip("\"'")
    return values


def note_title(path: Path, content: str) -> str:
    for line in content.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def note_status(frontmatter: Dict[str, str]) -> str:
    raw_status = frontmatter.get("status", "").strip().lower()
    if raw_status in {"completed", "complete", "done", "closed", "已完成", "完成"}:
        return "completed"
    return "active"


def query_terms(value: str) -> List[str]:
    terms: List[str] = []
    for token in re.findall(r"[a-z0-9]+|[\u3400-\u9fff]+", value.lower()):
        if token not in terms:
            terms.append(token)
        if re.fullmatch(r"[\u3400-\u9fff]+", token) and len(token) > 2:
            for index in range(len(token) - 1):
                pair = token[index : index + 2]
                if pair not in terms:
                    terms.append(pair)
    return terms


def match_score(title: str, content: str, terms: Sequence[str]) -> Tuple[int, str]:
    if not terms:
        return 1, ""

    title_lower = title.lower()
    content_lower = content.lower()
    matched: List[str] = []
    score = 0
    for term in terms:
        title_count = title_lower.count(term)
        content_count = content_lower.count(term)
        if title_count or content_count:
            matched.append(term)
            score += title_count * 8 + min(content_count, 5) * 2

    return score, matched[0] if matched else ""


def note_excerpt(content: str, matched_term: str, limit: int = 180) -> str:
    plain = re.sub(r"(?s)^---\n.*?\n---\n?", "", content)
    plain = re.sub(r"\s+", " ", plain).strip()
    if not plain:
        return ""
    if not matched_term:
        return plain[:limit]

    index = plain.lower().find(matched_term.lower())
    if index < 0:
        return plain[:limit]
    start = max(0, index - limit // 3)
    end = min(len(plain), start + limit)
    excerpt = plain[start:end]
    if start:
        excerpt = "…" + excerpt
    if end < len(plain):
        excerpt += "…"
    return excerpt


def query_notes(
    query_text: str,
    query_type: str,
    status: str,
    limit: int,
) -> Dict[str, Any]:
    settings = get_settings()
    root = normalized_path(str(settings["memory_root"]))
    if not root.is_dir():
        raise WriterError(f"已配置的记忆根目录不存在，请重新初始化：{root}")
    if limit < 1 or limit > 50:
        raise WriterError("--limit 必须介于 1 和 50 之间。")

    terms = query_terms(query_text)
    matches: List[Dict[str, Any]] = []
    for directory_name in QUERY_DIRECTORIES[query_type]:
        directory = assert_path_within_root(root / directory_name, root)
        if not directory.exists():
            continue
        if not directory.is_dir():
            raise WriterError(f"记忆分类路径不是目录：{directory}")

        for candidate in sorted(directory.rglob("*.md")):
            if candidate.name == INDEX_FILENAME:
                continue
            resolved = candidate.resolve(strict=True)
            assert_path_within_root(resolved, root)
            if not resolved.is_file():
                continue

            content = resolved.read_text(encoding="utf-8-sig")
            frontmatter = parse_frontmatter(content)
            current_status = note_status(frontmatter)
            if status != "all" and current_status != status:
                continue

            title = note_title(resolved, content)
            score, matched_term = match_score(title, content, terms)
            if score <= 0:
                continue

            modified = resolved.stat().st_mtime
            record_type = {
                "Inbox": "Inbox",
                "Tasks": "Task",
                "Knowledge": "Knowledge",
            }[directory_name]
            matches.append(
                {
                    "type": record_type,
                    "title": title,
                    "status": current_status,
                    "path": str(resolved),
                    "score": score,
                    "excerpt": note_excerpt(content, matched_term),
                    "_modified": modified,
                }
            )

    matches.sort(key=lambda item: (item["score"], item["_modified"]), reverse=True)
    selected = matches[:limit]
    for item in selected:
        item.pop("_modified", None)

    return {
        "success": True,
        "action": "queried",
        "query": query_text,
        "type": query_type,
        "status": status,
        "count": len(selected),
        "results": selected,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "写入或只读查询用户明确指定的本地 AI 协作记录"
            "（Obsidian 仓库或纯 Markdown 文件夹）。"
        ),
        add_help=False,
    )
    parser._optionals.title = "选项"
    parser.add_argument("-h", "--help", action="help", help="显示帮助信息并退出。")
    parser.add_argument(
        "--action",
        required=True,
        type=str.lower,
        choices=("init", "status", "set-root", "capture", "query"),
        help="要执行的操作。",
    )
    parser.add_argument("--memory-root", help="记忆根目录绝对路径。")
    parser.add_argument(
        "--require-obsidian",
        dest="require_obsidian",
        type=str.lower,
        choices=("true", "false"),
        default=None,
        help="初始化时是否要求记忆根目录位于 Obsidian 仓库内，默认 true。",
    )
    parser.add_argument(
        "--experience-mode",
        dest="experience_mode",
        type=str.lower,
        choices=("auto", "manual"),
        default=None,
        help="经验加载模式：auto 自动召回（默认），manual 仅显式调用时加载。",
    )
    parser.add_argument(
        "--type",
        dest="record_type",
        type=str.lower,
        choices=tuple(QUERY_DIRECTORIES),
        help="记录或查询类型。",
    )
    parser.add_argument("--title", help="记录标题。")
    parser.add_argument("--content", help="记录内容。")
    parser.add_argument(
        "--content-stdin",
        action="store_true",
        help="从标准输入读取记录内容。",
    )
    parser.add_argument("--target-file", help="用户明确指定的已有 Markdown 文档。")
    parser.add_argument("--query", default="", help="只读查询使用的关键词。")
    parser.add_argument(
        "--status",
        type=str.lower,
        choices=("active", "completed", "all"),
        default="all",
        help="查询任务状态，默认为 all。",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="查询最多返回的记录数，范围为 1 到 50。",
    )
    return parser.parse_args()


def run(args: argparse.Namespace) -> Dict[str, Any]:
    if args.action in {"init", "set-root"}:
        if not args.memory_root:
            raise WriterError(f"{args.action} 操作必须提供 --memory-root。")
        require_obsidian = DEFAULT_REQUIRE_OBSIDIAN
        experience_mode = DEFAULT_EXPERIENCE_MODE
        if args.action == "set-root" and SETTINGS_PATH.is_file():
            existing = get_settings()
            require_obsidian = bool(existing.get("require_obsidian", True))
            experience_mode = str(existing.get("experience_mode", "auto"))
        if args.require_obsidian is not None:
            require_obsidian = args.require_obsidian == "true"
        if args.experience_mode is not None:
            experience_mode = args.experience_mode
        result = initialize_memory_root(
            args.memory_root,
            require_obsidian,
            experience_mode,
        )
        if args.action == "set-root":
            result["action"] = "root-changed"
        return result

    if args.action == "status":
        if not SETTINGS_PATH.is_file():
            return {
                "success": True,
                "configured": False,
                "settings_path": str(SETTINGS_PATH),
            }
        settings = get_settings()
        memory_root = normalized_path(str(settings["memory_root"]))
        return {
            "success": True,
            "configured": True,
            "memory_root": str(memory_root),
            "vault_root": str(settings.get("vault_root", "")),
            "require_obsidian": bool(settings.get("require_obsidian", True)),
            "experience_mode": str(settings.get("experience_mode", "auto")),
            "root_exists": memory_root.is_dir(),
            "settings_path": str(SETTINGS_PATH),
        }

    if args.action == "query":
        return query_notes(
            args.query,
            args.record_type or "all",
            args.status,
            args.limit,
        )

    if not args.record_type:
        raise WriterError("capture 操作必须提供 --type。")
    if args.record_type == "all":
        raise WriterError("capture 操作的 --type 不能是 all。")
    if args.content is not None and args.content_stdin:
        raise WriterError("--content 和 --content-stdin 只能选择一个。")
    content = sys.stdin.read() if args.content_stdin else args.content
    if content is None:
        raise WriterError("capture 操作必须提供 --content 或 --content-stdin。")
    return capture_note(
        RECORD_TYPES[args.record_type],
        args.title,
        content,
        args.target_file,
    )


def main() -> int:
    try:
        result = run(parse_args())
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (WriterError, OSError) as exc:
        print(
            json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False),
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
