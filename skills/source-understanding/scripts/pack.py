"""pack.py — 五步法第1步「打包定位」：索引 + 提取符号 → 生成 00_index.md 骨架。

用法：
    python pack.py <repo_path> [--mode moderate] [--out 00_index.md]

产物 00_index.md 含：模块边界（节点/边统计）+ 入口点 + 待深读清单（骨架）。
LLM 只需在「待深读清单」里填空，不必手动敲 cbm-mcp 命令。
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

import cbm_client


def _parse_arch_text(text: str) -> dict:
    """解析 get_architecture 的纯文本输出（entry_points 等 aspect）。"""
    total_nodes = total_edges = None
    entry_points: list[tuple[str, str]] = []
    for line in text.splitlines():
        line = line.strip()
        m = re.match(r"total_nodes:\s*(\d+)", line)
        if m:
            total_nodes = int(m.group(1))
        m = re.match(r"total_edges:\s*(\d+)", line)
        if m:
            total_edges = int(m.group(1))
        # entry_points 行格式： "  <qn> <file>"
        if line and not line.startswith(("project:", "total_", "entry_points:", "has_more", "results:", "search_mode", "cols", "---")):
            parts = line.split()
            if len(parts) >= 2 and parts[1].count(".") >= 1 or "/" in parts[-1]:
                entry_points.append((parts[0], parts[-1]))
    return {"total_nodes": total_nodes, "total_edges": total_edges, "entry_points": entry_points}


def render_index(project: str, repo: Path, node_labels: list, edge_types: list, arch: dict) -> str:
    L: list[str] = []
    L.append(f"# 源码理解 · 00 索引（{repo.name}）")
    L.append("")
    L.append(f"> 生成：pack.py · {date.today().isoformat()} · project=`{project}`")
    L.append("")
    L.append("## 一、模块边界（节点 label 统计）")
    L.append("")
    L.append("| label | 数量 |")
    L.append("|---|---|")
    for n in sorted(node_labels, key=lambda x: -x.get("count", 0)):
        L.append(f"| {n.get('label')} | {n.get('count')} |")
    L.append("")
    L.append("## 二、关系类型（边 type 统计）")
    L.append("")
    L.append("| type | 数量 | 含义 |")
    L.append("|---|---|---|")
    for e in sorted(edge_types, key=lambda x: -x.get("count", 0)):
        L.append(f"| {e.get('type')} | {e.get('count')} | |")
    L.append("")
    if arch.get("total_nodes") is not None:
        L.append(f"## 三、规模（get_architecture）")
        L.append("")
        L.append(f"- 总节点：{arch['total_nodes']} · 总边：{arch['total_edges']}")
        L.append("")
    eps = arch.get("entry_points", [])
    if eps:
        L.append("## 四、入口点（entry_points）")
        L.append("")
        L.append("| qualified_name | file |")
        L.append("|---|---|")
        for qn, f in eps[:30]:
            L.append(f"| `{qn}` | `{f}` |")
        L.append("")
    L.append("## 五、待深读清单（LLM 填写）")
    L.append("")
    L.append("> 从入口点出发，沿主链路逐函数读 body，把核心方法 + file:line 填进来。")
    L.append("")
    L.append("| 核心方法 | file:line | 一句话职责 |")
    L.append("|---|---|---|")
    L.append("| （待填） | （待填） | （待填） |")
    L.append("")
    L.append("---")
    L.append("")
    L.append("下一步：`python dimensions.py` 生成八维穿透模板；主链路深读后写 01_dataflow.md。")
    return "\n".join(L)


def main() -> int:
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description="五步法第1步：打包定位（索引 + 提取符号 → 00_index.md）")
    ap.add_argument("repo", help="repo 路径")
    ap.add_argument("--mode", default="moderate", choices=["full", "moderate", "fast"])
    ap.add_argument("--out", default="00_index.md")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    if not repo.is_dir():
        print(f"错误：{repo} 不是目录", file=sys.stderr)
        return 1

    project = cbm_client.project_name_for(repo)
    if project is None:
        print(f"[1/4] 索引 {repo}（mode={args.mode}）...")
        cbm_client.index(repo, args.mode)
        project = cbm_client.project_name_for(repo)
        if project is None:
            print("索引后仍找不到 project，请检查 cbm-mcp", file=sys.stderr)
            return 1
    else:
        print(f"[1/4] 已索引：{project}")

    print("[2/4] 提取图 schema ...")
    schema = cbm_client.graph_schema(project)
    node_labels = schema.get("node_labels", [])
    edge_types = schema.get("edge_types", [])

    print("[3/4] 提取入口点 ...")
    arch_text = cbm_client.architecture(project, ["entry_points"]).get("_text", "")
    arch = _parse_arch_text(arch_text)

    print(f"[4/4] 生成 {args.out} ...")
    md = render_index(project, repo, node_labels, edge_types, arch)
    Path(args.out).write_text(md, encoding="utf-8")
    print(f"完成 → {args.out}（{len(node_labels)} 节点 label / {len(edge_types)} 边 type / {len(arch.get('entry_points', []))} 入口点）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
