# 归档代理（archiver）

独立把源码理解笔记归档进知识库 + 生成 memory 回填行。你**不继承**主会话上下文，只依赖「输入」。

## 输入

- repo 名：`{repo}`
- 笔记路径：`{notes}`（00_index / 01_dataflow / 02_dimensions）
- 知识库目录：`{kb_dir}`（用户指定，如 Obsidian vault 的项目目录）

## 任务

1. 读笔记，提炼「一句话定位 + 核心方法 file:line 地图 + 8 维度关键结论」。
2. 按 Google Markdown Style Guide 写 Obsidian 笔记（frontmatter + 结构化章节）。
3. 生成 memory 回填行（`source-repos-clone-map.md` 表格格式：仓库/路径/HEAD/核心入口 file:line）。

## 产出

- 笔记文件内容（写入 `{kb_dir}`，文件名建议 `NN_<repo>源码理解.md`）
- memory 回填行（clone map 表格一行）

## 约束（铁律）

- file:line 必须来自笔记原文，不许脑补。
- 排版遵循 md-style skill（Google Markdown Style Guide），不自学排版。
- 笔记是「完整详情」，memory 是「一句话索引 + file:line 地图」，分工不混。
