# 晓风（源码理解工作流）

吸收专业源码的全流程 Claude Code 插件：**选型 → 吃透 → 归档**。引擎外部引用，可进阶。

## 快速开始

前置条件：Claude Code 环境、Python 3、codebase-memory-mcp 预编译二进制。

```bash
# 1. 装引擎：下载 codebase-memory-mcp 预编译二进制
#    https://github.com/DeusData/codebase-memory-mcp/releases
#    解压得到 codebase-memory-mcp(.exe)，设环境变量指向它
export CBM_BIN=/path/to/codebase-memory-mcp

# 2. 装插件（二选一）
#    方式 A：Claude Code 插件市场安装
#    方式 B：把 skills/ 下三个目录复制到 ~/.claude/skills/
#            discover / settle / source-understanding

# 3. 使用：对某个 repo 触发五步法
#    dispatch discoverer 选型 → pack → deep-reader → verify → archiver
```

## 架构：3 skill + 4 agent + 4 脚本

| 阶段 | skill | agent | 脚本 |
|---|---|---|---|
| 选型 | `discover` | `discoverer`（搜高星+评估） | — |
| 吃透 | `source-understanding`（五步法） | `deep-reader`（逐模块深读）、`dimension-analyzer`（逐维度分析） | `pack.py` / `dimensions.py` / `verify.py` / `report.py` |
| 归档 | `settle` | `archiver`（写笔记+回填 memory） | — |

**分工铁律**：脚本管机械骨架（索引/模板/验证/合并），agent 管理解密集型（深读/分析/归档），主代理只编排 + 汇总。

## 依赖（引擎外部引用，不粘代码）

- **codebase-memory-mcp**（图索引引擎）：`CBM_BIN` 环境变量指向预编译二进制，从 https://github.com/DeusData/codebase-memory-mcp 下载。
- **Python 3**：脚本运行时。
- 换引擎只改 `skills/source-understanding/scripts/cbm_client.py`，五步法不变。

## 全流程用法

```text
# 0 选型（discover）
dispatch discoverer → 搜高星 → 评估 → clone 到本地仓库目录

# 1-5 吃透（source-understanding 五步法）
python scripts/pack.py <repo>                     # 打包定位 → 00_index.md
dispatch deep-reader × N                          # 链路深读 → 01_dataflow.md
python scripts/dimensions.py                      # 八维模板 → 02_dimensions.md
dispatch dimension-analyzer × 8                   # 八维分析 → 回填 02
python scripts/verify.py 01_dataflow.md 02_dimensions.md   # 硬验证锚定

# 6 归档（settle）
python scripts/report.py --repo X --notes 00 01 02 --map    # 合并 + 地图
dispatch archiver                                 # 写笔记 + 回填 memory
```

## 目录

```
skills/
├── discover/
│   ├── SKILL.md
│   └── agents/discoverer.md
├── source-understanding/
│   ├── SKILL.md
│   ├── scripts/{cbm_client,pack,dimensions,verify,report}.py
│   └── agents/{deep-reader,dimension-analyzer}.md
└── settle/
    ├── SKILL.md
    └── agents/archiver.md
```
