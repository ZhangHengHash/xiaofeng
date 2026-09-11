"""dimensions.py — 五步法第3步「八维穿透」：生成 02_dimensions.md 硬模板。

强制 LLM 覆盖 8 维度，每个维度都要 file:line 锚定，缺一维即验证不过（verify.py 会检查）。
用法：
    python dimensions.py [--out 02_dimensions.md]
"""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

# 八维度：名称 -> (该查什么, 建议查法)
DIMENSIONS: list[tuple[str, str, str]] = [
    ("数据流与算子链路", "主入口 → 各算子的输入类型 → 处理逻辑 → 输出类型", "沿主链路逐函数读 + search_graph 追调用链"),
    ("底层存储抽象", "存储接口/抽象类/落地实现（schema、表结构、文件格式）", "grep class/interface/ABC，找抽象与实现分离点"),
    ("实体消歧", "同名实体怎么区分（FQN / 唯一 ID / 命名空间）", "找唯一 key 的生成逻辑，验证同名是否分裂/误合并"),
    ("并发与状态锁", "锁 / 原子操作 / 并发模型 / 竞态防护", "grep lock/atomic/mutex/threading/async"),
    ("异常与重试机制", "异常处理 / 重试 / 降级 / 兜底", "grep try/except/retry/fallback/timeout"),
    ("性能瓶颈", "缓存 / 并行 / 索引 / 惰性加载", "grep cache/parallel/index/lazy"),
    ("工程落地落差", "文档/论文/README 声明 vs 代码真实实现", "对比 README 承诺与源码，标出不一致处"),
    ("模块可切割性", "模块边界 / 依赖方向 / 可否独立运行", "看目录结构 + import 关系 + 入口可独立跑否"),
]


def render() -> str:
    L: list[str] = []
    L.append("# 源码理解 · 02 八维穿透")
    L.append("")
    L.append(f"> 生成：dimensions.py · {date.today().isoformat()} · 逐维度填空，每条结论必须 file:line 锚定。")
    L.append("")
    for i, (name, what, how) in enumerate(DIMENSIONS, 1):
        L.append(f"## 维度 {i}：{name}")
        L.append("")
        L.append(f"- **该查什么**：{what}")
        L.append(f"- **建议查法**：{how}")
        L.append("")
        L.append("**结论**（每条必须带 file:line，如 `lightrag.py:1839`）：")
        L.append("")
        L.append("- [ ] （待填，file:line）")
        L.append("")
    L.append("---")
    L.append("")
    L.append("填完后运行 `python verify.py 02_dimensions.md` 检查 file:line 锚定是否齐全。")
    return "\n".join(L)


def main() -> int:
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description="五步法第3步：生成八维穿透硬模板")
    ap.add_argument("--out", default="02_dimensions.md")
    args = ap.parse_args()
    Path(args.out).write_text(render(), encoding="utf-8")
    print(f"完成 → {args.out}（{len(DIMENSIONS)} 维度）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
