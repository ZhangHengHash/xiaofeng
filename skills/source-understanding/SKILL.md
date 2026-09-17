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

## 子代理 dispatch（理解密集型子任务）

第 2、3.5 步是理解密集型，用 `Agent` 工具派**新鲜子代理**独立执行（不继承主会话上下文），主代理只编排 + 汇总：

```text
# 第 2 步：一个模块派一个 deep-reader（可并行 dispatch 多个模块）
Agent(subagent_type="general-purpose", prompt=agents/deep-reader.md 内容 + 填入 {repo}/{module}/{range})

# 第 3.5 步：一个维度派一个 dimension-analyzer（可并行 dispatch 8 个维度）
Agent(subagent_type="general-purpose", prompt=agents/dimension-analyzer.md 内容 + 填入 {repo}/{dimension}/{how})
```

- **并行**：同一条消息里多个 Agent 调用 = 并行执行；一条一个 = 串行。
- **主代理只做**：填 prompt 占位符 → dispatch → 汇总子代理产出 → 跑脚本验证/沉淀。

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
