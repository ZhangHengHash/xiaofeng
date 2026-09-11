"""cbm_client.py — codebase-memory-mcp CLI 调用封装（薄层，引擎外部引用，不粘源码）。

依赖外部引擎 codebase-memory-mcp（预编译 exe），通过 CBM_BIN 环境变量定位。
默认 E:\\agentic_src\\cbm-bin\\codebase-memory-mcp.exe。
"""
from __future__ import annotations

import json
import os
import subprocess

CBM_BIN = os.environ.get("CBM_BIN", r"E:\agentic_src\cbm-bin\codebase-memory-mcp.exe")


def _extract_envelope(stdout: str):
    """从 cbm-mcp stdout 提取 JSON envelope（跳过 warning/hint 等文本行）。

    cbm-mcp CLI 的 stdout 是「若干提示文本行 + 最后一行 JSON envelope」，
    故从后往前找第一个能解析成 JSON 的行。
    """
    for line in reversed(stdout.strip().splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue
    return None


def run(tool: str, args: dict | None = None) -> dict:
    """调 cbm-mcp 一个 CLI 工具，返回解析后的结果。

    返回 structuredContent（结构化 JSON 工具），
    或 {"_text": ...}（纯文本表格工具如 search_graph / get_architecture）。
    """
    if not os.path.isfile(CBM_BIN):
        raise RuntimeError(
            f"引擎缺失：{CBM_BIN} 不存在。请设置 CBM_BIN 环境变量指向 codebase-memory-mcp.exe"
        )
    args = args or {}
    cmd = [CBM_BIN, "cli", "--json", tool, json.dumps(args, ensure_ascii=False)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    env = _extract_envelope(p.stdout or "")
    if env is None:
        raise RuntimeError(
            f"cbm-mcp {tool} 无 JSON 输出\nstdout={p.stdout[-300:]}\nstderr={p.stderr[-300:]}"
        )
    if env.get("isError"):
        raise RuntimeError(f"cbm-mcp {tool} 报错: {json.dumps(env, ensure_ascii=False)[:500]}")
    sc = env.get("structuredContent")
    if sc:
        return sc
    content = env.get("content") or []
    return {"_text": content[0].get("text", "") if content else ""}


def list_projects() -> list[dict]:
    return run("list_projects").get("projects", [])


def project_name_for(repo_path) -> str | None:
    """返回 repo 已索引的 project name（按 root_path 精确匹配），未索引返回 None。"""
    rp = str(repo_path).replace("\\", "/").rstrip("/")
    for p in list_projects():
        if p.get("root_path", "").replace("\\", "/").rstrip("/") == rp:
            return p["name"]
    return None


def index(repo_path, mode: str = "moderate") -> dict:
    return run("index_repository", {"repo_path": str(repo_path), "mode": mode})


def graph_schema(project: str) -> dict:
    return run("get_graph_schema", {"project": project})


def architecture(project: str, aspects: list[str]) -> dict:
    return run("get_architecture", {"project": project, "aspects": aspects})


def search(project: str, query: str, limit: int = 10) -> dict:
    return run("search_graph", {"project": project, "query": query, "limit": limit})
