"""verify.py — 五步法第4步「验证」：硬检查笔记的 file:line 锚定是否齐全，防脑补。

检查规则：
- 扫描 md 文件里的所有「待办行」（- [ ] / - [x]）
- 待办行仍是「待填/TODO」→ 未完成
- 已勾选但没有 file:line（形如 file.py:123 或 file.py:123-456）→ 缺锚定
用法：
    python verify.py <note.md> [note2.md ...]
退出码：0 = 全通过，1 = 有未完成/缺锚定。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# file:line 锚定：something.ext:123 或 something.ext:123-456
FILELINE_RE = re.compile(
    r"[\w./\\\-]+\.(?:py|c|h|cc|cpp|hpp|js|ts|tsx|jsx|go|rs|java|kt|rb|php|sh|md|json|yaml|yml|sql|toml):\d+(-\d+)?"
)
# 待办行： - [ ] 或 - [x]
TODO_RE = re.compile(r"^\s*-\s*\[([ xX])\]\s*(.*)$")
# 「未填」标记
TBD_RE = re.compile(r"待填|TODO|TBD|待定|（待", re.IGNORECASE)


def check_file(path: Path) -> list[tuple[int, str, str]]:
    issues: list[tuple[int, str, str]] = []
    for i, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        m = TODO_RE.match(line)
        if not m:
            continue
        checked, content = m.group(1), m.group(2).strip()
        has_fl = bool(FILELINE_RE.search(line))
        if checked in (" ", "") or TBD_RE.search(content):
            issues.append((i, "未填", line.strip()[:90]))
        elif not has_fl:
            issues.append((i, "缺锚定", line.strip()[:90]))
    return issues


def count_dimensions(path: Path) -> tuple[int, int]:
    """统计「## 维度 N」标题数 vs 已填（- [x] 带 file:line）结论数。"""
    text = path.read_text(encoding="utf-8", errors="replace")
    dims = re.findall(r"^##\s*维度\s*\d+", text, re.MULTILINE)
    filled = sum(
        1 for line in text.splitlines()
        if line.strip().startswith("- [x]") and FILELINE_RE.search(line)
    )
    return len(dims), filled


def main() -> int:
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description="五步法第4步：检查 file:line 锚定是否齐全")
    ap.add_argument("files", nargs="+", help="要检查的 md 文件")
    args = ap.parse_args()

    total = 0
    for f in args.files:
        p = Path(f)
        if not p.exists():
            print(f"错误：{f} 不存在（上一步产物缺失，不许跳步）", file=sys.stderr)
            total += 1
            continue
        issues = check_file(p)
        total += len(issues)
        ndim, nfill = count_dimensions(p)
        dim_msg = f"（{nfill} 条结论 / {ndim} 维度）" if ndim else ""
        if issues:
            print(f"X {f}：{len(issues)} 处问题 {dim_msg}")
            for ln, kind, content in issues:
                print(f"   L{ln:<4d} [{kind}] {content}")
        else:
            print(f"OK {f}：通过 {dim_msg}")
    print()
    print("全部通过" if total == 0 else f"合计 {total} 处问题（未填/缺锚定）")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
