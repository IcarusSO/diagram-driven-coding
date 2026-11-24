# 示範項目嘅 AI 指引（Codex 等讀 AGENTS.md 嘅工具用；內容同 CLAUDE.md 一致）

請跟 `../SKILL.md`（diagram-driven-coding）工作，包括第 4 點：dict 形狀用 `TypedDict` 命名，public 項目要有 Google 風格 docstring。

## 改動前先讀文件

先讀 `ARCHITECTURE.md`（元件地圖），再讀目標元件自己嘅 `ARCHITECTURE.md`；子元件（例如 `pricing/rules`）有自己嘅文件。只讀需要嘅部分，唔好掃描整個項目。

## 本項目嘅批准設定

以下 interface 改動一律事先批准：改簽名、回傳、資料結構、單位、語義、class 職責、跨 folder 依賴，以及改或刪 contract test。

改 interface 之前，先搜尋並列出「同當前工作無關」嘅其他使用者，連同前後契約對比向我報告，等我批准先繼續。

## 運行測試

```bash
cd demo
python3 -m unittest discover -v
```
