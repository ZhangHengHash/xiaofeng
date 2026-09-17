---
name: discover
description: Use when 找高星项目借鉴、选型技术方案、判断某项目值不值得深挖、clone 一个 repo 准备吃透。触发：晓风选型、找高星项目、判断值不值得吃透。
---

# 源码选型（discover）

> 吸收专业源码的第 0 步：找到值得吃透的高星项目，判断价值，clone 到本地。

## 流程

1. 派 `agents/discoverer.md` 子代理搜 GitHub（`gh search repos`，关键词多角度）。
2. 判断：star 实测（`gh api` 为准，不信搜索摘要数字）+ 活跃度（pushedAt）+ 语言 + license + 与需求匹配。
3. 确认后 clone 到 `E:\agentic_src\<name>`（`--depth 1`）。
4. 回填 `source-repos-clone-map.md`（memory）。

## 铁律

- star 数必须 `gh api` 实测，不脑补。
- 先判方向对不对（代码理解 vs RAG，别选错——参考 memory `code-understanding-vs-rag`）。
- clone 后立即回填 clone map，否则下次失忆。
- 代理只搜只评，不 clone 不写文件；clone 由主代理执行。

## 参考

- memory `github-high-star-first`（先搜高星）
- memory `source-repos-clone-map`（clone 清单）
