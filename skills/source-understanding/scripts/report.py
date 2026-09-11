"""report.py — 五步法第5步「沉淀」：合并笔记 + 提取 file:line 地图（回填 memory 用）。

用法：
    # 合并 00/01/02/03 为最终笔记
    python report.py --repo aider --notes 00_index.md 01_dataflow.md 02_dimensions.md --out 源码理解_aider.md
    # 额外提取「核心方法 file:line 地图」（回填 source-repos-clone-map 表格）
    python report.py --repo aider --notes 00_index.md 01_dataflow.md 02_dimensions.md --map
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

FILELINE_RE = re.compile(r"([\w./\\\-]+\.\w+):(\d+)(-\d+)?")
FRONTMATTER = """---
tags: [源码理解, codebase-memory-mcp, 五步法]
type: source-code
source: {repo}
---
"""


def merge_notes(notes: list[Path], repo: str) -> str:
    L = [f"# {repo} 源码理解（合并）", "", f"> 生成：report.py · {date.today().isoformat()}", ""]
    for note in notes:
        if not note.exists():
            L.append(f"<!-- 缺失：{note} -->")
            continue
        L.append(f"<!-- ===== {note.name} ===== -->")
        L.append("")
        L.append(note.read_text(encoding="utf-8", errors="replace").rstrip())
        L.append("")
    return "\n".join(L)


def extract_map(notes: list[Path]) -> str:
    """提取「真实结论」的 file:line 引用（仅 - [x] 勾选行 + 表格行），去重生成地图。

    跳过模板说明（> / # 开头）和未填行（- [ ]），避免把模板示例当真实结论。
    """
    seen: dict[str, set[str]] = {}
    for note in notes:
        if not note.exists():
            continue
        for line in note.read_text(encoding="utf-8", errors="replace").splitlines():
            s = line.strip()
            if not (s.startswith("- [x]") or s.startswith("- [X]") or s.startswith("|")):
                continue
            for m in FILELINE_RE.finditer(line):
                fpath, lineno = m.group(1), m.group(2)
                seen.setdefault(fpath, set()).add(lineno)
    L = ["# 核心方法 file:line 地图", ""]
    L.append("> 回填 source-repos-clone-map.md 的「核心入口」列。")
    L.append("")
    L.append("| file | 行号 |")
    L.append("|---|---|")
    for fpath in sorted(seen):
        lines = ",".join(sorted(seen[fpath], key=int))
        L.append(f"| `{fpath}` | {lines} |")
    return "\n".join(L)


def main() -> int:
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description="五步法第5步：合并笔记 + 提取 file:line 地图")
    ap.add_argument("--repo", required=True, help="repo 名")
    ap.add_argument("--notes", nargs="+", required=True, help="要合并的笔记文件（按序）")
    ap.add_argument("--out", default=None, help="合并输出文件")
    ap.add_argument("--map", action="store_true", help="额外输出 file:line 地图")
    args = ap.parse_args()

    notes = [Path(n) for n in args.notes]
    missing = [str(n) for n in notes if not n.exists()]
    if missing:
        print(f"错误：笔记缺失（上一步产物，不许跳步）：{', '.join(missing)}", file=sys.stderr)
        return 1

    if args.out:
        merged = FRONTMATTER.format(repo=args.repo) + "\n" + merge_notes(notes, args.repo)
        Path(args.out).write_text(merged, encoding="utf-8")
        print(f"合并完成 → {args.out}")

    if args.map or not args.out:
        print(extract_map(notes))

    return 0


if __name__ == "__main__":
    sys.exit(main())
