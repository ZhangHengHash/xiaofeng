---
name: source-understanding
description: Use when 吃透陌生仓库源码、源码级理解、查符号定义/调用链/数据流、给高星项目做 8 维度深读、吸收专业源码。触发：晓风、吃透开源项目、查调用链、八维穿透。
---

# 源码理解硬核工作流（五步法）

> **全流程**：`discover`（选型）→ 本 skill（吃透五步法）→ `settle`（归档）。本 skill 是中间「吃透」环节。
> 脚本在 `scripts/` 下，引擎 codebase-memory-mcp 外部引用（`CBM_BIN` 环境变量指向 exe）。
> **脚本管机械骨架，LLM 管理解填空**——逐函数读、八维分析必须 LLM 亲自做，不许脚本代劳。

## 五步法（脚本 ↔ LLM 分工）

| 步 | 动作 | 谁做 | 命令 |
|---|---|---|---|
| 1 打包定位 | 索引 + 提取符号 + 生成 `00_index.md` 骨架 | 脚本 | `python scripts/pack.py <repo> [--mode moderate]` |
| 2 链路深读 | 派 deep-reader 子代理逐模块深读，汇总 `01_dataflow.md` | 子代理 | dispatch `agents/deep-reader.md` |
| 3 八维模板 | 生成 8 维度硬模板 `02_dimensions.md` | 脚本 | `python scripts/dimensions.py` |
| 3.5 填八维 | 派 dimension-analyzer 子代理逐维度分析，汇总 `02_dimensions.md` | 子代理 | dispatch `agents/dimension-analyzer.md` |
| 4 验证 | 硬检查 file:line 锚定是否齐全（防脑补） | 脚本 | `python scripts/verify.py 01_dataflow.md 02_dimensions.md` |
| 5 沉淀 | 合并笔记 + 提取 file:line 地图（回填 memory） | 脚本 | `python scripts/report.py --repo <名> --notes 00 01 02 --out 最终.md --map` |

## 子任务分工（理解密集型）

第 2、3.5 步是理解密集型，需派**独立子代理**执行（不继承主会话上下文），主代理只编排 + 汇总。子代理的 prompt 用 `agents/` 下模板填充，模板是框架无关的 prompt 文本：

- 第 2 步：每个模块派一个 deep-reader，prompt = `agents/deep-reader.md`（填 {repo}/{module}/{range}）
- 第 3.5 步：每个维度派一个 dimension-analyzer，prompt = `agents/dimension-analyzer.md`（填 {repo}/{dimension}/{how}）

- **并行**：多个子任务并行派发。
- **主代理只做**：填占位符 → 派子代理 → 汇总产出 → 跑脚本。
- dispatch 机制由宿主 agent 框架决定（Claude Code 用 Agent 工具，其他框架用各自的子任务机制），`agents/*.md` 不绑定任何框架。

## 依赖

- **引擎**：codebase-memory-mcp 预编译 exe（外部，不粘源码），`CBM_BIN` 环境变量指定（从 https://github.com/DeusData/codebase-memory-mcp 下载）。
- **运行时**：Python 3。

## 铁律

1. 脚本是机械骨架，理解（逐函数读、八维分析）必须 LLM 亲自做。
2. 每条结论必须 `file:line` 锚定，`verify.py` 不过不许收尾。
3. 引擎可替换：换图引擎只改 `scripts/cbm_client.py` 的调用，五步法不变。
4. 已索引的 repo 直接跑 `pack.py`（跳过重索引），节省时间。

## 参考

- 五步法方法论：memory `source-understanding-workflow`
- 引擎源码理解：见仓库 README「依赖」
