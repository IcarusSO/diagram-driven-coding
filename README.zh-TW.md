# diagram-driven-coding

[English](README.md) | [繁體中文](README.zh-TW.md) | [简体中文](README.zh-CN.md)

一個給 AI 寫程式用的 skill：每個元件資料夾內都有自己的 `ARCHITECTURE.md`（class／sequence diagram、職責、資料契約）先行，配合 TDD 與 interface 分層，把 AI 改程式的影響範圍收窄。

> 注意：`SKILL.md` 與 demo 文件以粵語撰寫，AI 讀取沒有問題；README 提供三種語言。

## 解決什麼問題

> 想先看成品：[demo/ARCHITECTURE.md](demo/ARCHITECTURE.md) 是 root 元件地圖，順著連結可以看到元件與子元件的文件。

請 AI 改一個功能，它順手改了三個不相關的檔案；改 A 壞 B；出錯之後還得逐行 debug，省不了時間。

這個 skill 不是叫 AI「更小心」，而是讓它沒有機會亂改：

- **邊界清楚**：每個元件一個資料夾，只透過 interface 對外，private helper 外部不得碰。
- **先改圖、再寫 test、後實作**：圖是 AI 與人都看得懂的導覽圖，也是 review 的重點。
- **測對外承諾，不測內部結構**：避免 AI 用大量結構測試製造虛假的 coverage 安全感。
- **改 interface 要經人批准**：AI 會先評估有沒有「與當前工作無關」的其他使用者，再主動詢問你是否批准。
- **壞了可以整個 class 換掉**：多個實作共用同一套行為 contract test。

更多做法見最後的「核心原則詳解」。

## 內容

| 路徑 | 內容 |
| --- | --- |
| `SKILL.md` | skill 本體，單一檔案（核心做法、進階選項、ARCHITECTURE.md 範本） |
| `demo/` | 一個小型 Python 示範專案（root、元件、子元件各有 `ARCHITECTURE.md`），三個情境示範 skill 如何運作，詳見 `demo/DEMO.md`。想快速看成品：[demo/ARCHITECTURE.md](demo/ARCHITECTURE.md)（root 元件地圖）→ [demo/pricing/ARCHITECTURE.md](demo/pricing/ARCHITECTURE.md)（元件）→ [demo/pricing/rules/ARCHITECTURE.md](demo/pricing/rules/ARCHITECTURE.md)（子元件） |

## 使用方式

- **Claude Code**：將 `SKILL.md` 放入 `.claude/skills/diagram-driven-coding/SKILL.md`。
- **ChatGPT／Codex**：
  - ChatGPT：若帳號有 Skills 功能，到 Plugins → Skills → Create → Upload from your computer 上傳；沒有的話，將 `SKILL.md` 貼入 Project 的 instructions，或以檔案上傳。
  - Codex：放入專案的 `.agents/skills/diagram-driven-coding/SKILL.md`（想在所有專案使用，放在 `~/.agents/skills/`），輸入 `$diagram-driven-coding` 即可明確呼叫。不需要另外寫 `AGENTS.md`。
- **其他 AI 工具**：放入該工具的 skills 目錄，或將內容併入專案的指引檔（例如 `.cursorrules`）。

適用於中型以上、AI 會長期參與維護的專案。小 script 或一次性專案不需使用。

## 狀態

核心做法來自多個真實專案的長期使用經驗；「進階」部分（自動強制檢查、commit hash、分級批准等）尚未驗證，請當作建議。

## 試跑 demo 的測試

```bash
cd demo
python3 -m unittest discover -v
```

只需 Python 3.9 以上，沒有外部依賴。

## 執行型別檢查（可選）

Interface 簽名的相容性由型別檢查器強制（見 skill 的「簽名相容」原則）。Demo 已附設定檔：

```bash
pip install mypy pyright
cd demo
mypy       # 讀取 mypy.ini（strict）
pyright    # 讀取 pyrightconfig.json（standard）
```

兩者都應該是 0 error。

## 核心原則詳解

### 文件分層

- **root `ARCHITECTURE.md`**：只畫元件地圖（誰依賴誰）與跨元件的主要流程，不寫實作細節。
- **元件 `ARCHITECTURE.md`**：每個元件一份，寫職責、class／sequence diagram、資料契約與「不負責什麼」。
- **子元件**：只有符合開 interface 條件（跨資料夾使用、有多個可替換實作、接外部系統）才拆出來，同樣有自己的 `ARCHITECTURE.md`；在父層的圖中只當作一個 participant。層數控制在 2–3 層。
- 範例：[root](demo/ARCHITECTURE.md)、[元件](demo/pricing/ARCHITECTURE.md)、[子元件](demo/pricing/rules/ARCHITECTURE.md)。

### 資料形狀要寫明

- 回傳值若是固定 key 的結構，用 `TypedDict`，放在元件的 `data_types.py`，並由 `__init__.py` 匯出。不用裸 `dict`（看不出裡面有什麼），也不為了包裝而硬做 class（多了隱藏邏輯，使用麻煩）。
- 值只能是幾個固定字串時，用 `Literal`（例如 `CustomerTier`）。
- DataFrame 的 column 與 dtype 也是資料契約：column 清單只定義一次，文件與驗證共用；在元件邊界驗證輸入與輸出（可考慮 `pandera`）。
- 每個公開函式、class 都要有 Google style docstring（`Args:`、`Returns:`、`Raises:`、`Not responsible for:` 等）。

### 簽名相容交給型別檢查器

- 原則：實作的簽名與 interface 相容：參數名稱、順序、kind 一致；型別依型別檢查器的規則（參數可放寬、return 可收窄）。
- 注意工具保證的是「相容」，不是「文字上完全相同」。
- 不靠 AI 自覺，靠工具把關：Python 用 pyright 或 mypy，TypeScript 用 `tsc --strict`，Java／C# 由 compiler 負責。
- Demo 附有 `demo/mypy.ini` 與 `demo/pyrightconfig.json`，見上面「執行型別檢查」。

### 要做 DIP，但別讓 interface 變亂（YAGNI）

- 實作 class 的 constructor 可以接收 interface 型別的依賴，但這些參數只是元件內部的事。
- 組裝放在元件 `__init__.py` 的工廠函式（例如 `default_pricer()`）；對外只匯出 interface、`TypedDict` 與工廠函式；實作 class 不放入 `__all__`，約定其他資料夾只使用工廠函式與 interface。Python 不會強制，要強制就用依賴檢查。
- 沒有 interface 的內部小 class（驗證、小計等）由實作自己建立，不需注入。
- AI 若為了「將來可能替換」而新增公開參數或匯出實作 class，必須說明是哪個具體需求；答不出來就不加。
- Demo 對應：`demo/pricing/__init__.py` 與 `demo/pricing/standard_pricer.py`。

### 測試規則

- 測對外承諾（行為），不鎖死內部結構。檢查標準：這個 test 失敗時，下游會不會真的壞？下游依賴的 import 路徑、關鍵字參數名稱也算契約，可以測。
- 多個實作共用同一套 contract test，所以整個 class 換掉時，行為保證仍在。

### 改 interface 要經人批准

- 預設所有 interface 改動都要批准。
- AI 會先評估有沒有「與當前工作無關」的其他使用者（其他資料夾有沒有引用），向你說明影響範圍，再主動詢問是否批准。

### 接手舊專案

- 非 OOP 專案不要一次重寫：先在現有程式加一層薄薄的 caller（最少改動），並先寫 characterization test 鎖住現有行為。
- 再在新資料夾用 OOP 寫核心邏輯，與舊邏輯並行（shadow run）比對結果，滿意再切換，並保留回退。
- 核心邏輯很大時，逐件搬，root 圖用 `<<legacy>>` participant 表示尚未搬的部分。

### 誠實回報

- AI 回報時要分清楚：`PASSED`、`FAILED`、`NOT RUN`、`BLOCKED`，不可將沒跑過的 test 說成通過。

### 進階（可選，尚未驗證）

自動強制檢查、commit hash、test plan／notebook、分級批准，詳見 `SKILL.md` 的「進階」部分。

## 授權

MIT，見 [LICENSE](LICENSE)。
