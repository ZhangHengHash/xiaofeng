---
name: settle
description: Use when 源码理解完成收尾、把 00-03 笔记沉淀成知识库笔记、回填 clone map 的 file:line 地图、归档知识库。触发：晓风归档、源码理解收尾、沉淀笔记、回填 memory。
---

# 源码归档（settle）

> 吸收专业源码的最后一步：把吃透的产物归档进知识库 + 回填 memory，形成可复用资产。

## 流程

1. 跑 `source-understanding/scripts/report.py --repo <名> --notes 00 01 02 --out 最终.md --map` 合并笔记 + 提取 file:line 地图。
2. 派 `agents/archiver.md` 子代理：按 md-style 规范写 Obsidian 笔记到知识库（默认 `E:\AI-KB\02_项目\`）。
3. 回填 memory：`source-repos-clone-map.md` 的 file:line 地图行 + 相关记忆卡。

## 铁律

- file:line 必须来自笔记原文，不脑补。
- 排版遵循 `md-style` skill（Google Markdown Style Guide）。
- 归档后立即回填 memory，否则下次失忆。

## 参考

- skill `md-style`（排版规范）
- skill `doc-to-obsidian-kb`（文档转知识库）
