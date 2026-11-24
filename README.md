# diagram-driven-coding

一個畀 AI 寫 code 用嘅 skill：用每個元件 folder 內嘅 `ARCHITECTURE.md`（class／sequence diagram、職責、資料契約）先行，配合 TDD 同 interface 分層，收窄 AI 改 code 嘅爆炸半徑。

*English: a skill that keeps AI-written changes inside a component boundary. Diagram first, then tests, then code. Interface changes need human approval.*

## 解決咩問題

> 想先睇成品：[demo/ARCHITECTURE.md](demo/ARCHITECTURE.md) 係 root 元件地圖，順住連結可以睇到元件同子元件嘅文件。

叫 AI 改一個功能，佢順手改咗三個唔相關嘅檔案；改 A 壞 B；錯咗之後逐行 debug 慳唔到時間。

呢個 skill 唔係叫 AI「更加小心」，而係令佢冇得亂改：

- **邊界清楚**：每個元件一個 folder，只經 interface 對外，private helper 外面唔准碰。
- **先改圖、再寫 test、後實作**：圖係 AI 同人都睇得明嘅導航圖，亦係 review 嘅重點。
- **測對外承諾，唔測內部結構**：防止 AI 用大量結構測試製造虛假嘅 coverage 安全感。
- **改 interface 要經人批准**：AI 會先估算有冇「同當前工作無關」嘅其他使用者，再主動問你要唔要批准。
- **錯咗可以整個 class 換走**：多個實作共用同一套行為 contract test。

更多做法見最後嘅「核心原則詳解」。

## 內容

| 路徑 | 內容 |
| --- | --- |
| `SKILL.md` | skill 本體，一個檔案（核心做法、進階可選項、ARCHITECTURE.md 模板） |
| `demo/` | 一個細小嘅 Python 示範項目（root、元件、子元件各有 `ARCHITECTURE.md`），三個情境示範 skill 點樣運作，詳見 `demo/DEMO.md`。想快啲睇成品：[demo/ARCHITECTURE.md](demo/ARCHITECTURE.md)（root 元件地圖）→ [demo/pricing/ARCHITECTURE.md](demo/pricing/ARCHITECTURE.md)（元件）→ [demo/pricing/rules/ARCHITECTURE.md](demo/pricing/rules/ARCHITECTURE.md)（子元件） |

## 點用

- **Claude Code**：將 `SKILL.md` 放入 `.claude/skills/diagram-driven-coding/SKILL.md`。
- **ChatGPT**：將 `SKILL.md` 嘅內容貼入 Project 或自訂 GPT 嘅 instructions，或者作為檔案上載；如果用 Codex，就併入項目嘅 `AGENTS.md`。
- **其他 AI 工具**：放入該工具嘅 skills 目錄，或者將內容併入項目嘅指引檔（例如 `CLAUDE.md`、`.cursorrules`）。

適用於中型以上、AI 會長期參與維護嘅項目。細 script 或一次性項目唔使用。

## 狀態

核心做法來自多個真實項目嘅長期使用經驗；「進階」部分（自動強制檢查、commit hash、分級批准等）仲未驗證，請當作建議。

## 試跑 demo 嘅測試

```bash
cd demo
python3 -m unittest discover -v
```

只需要 Python 3.9 或以上，冇外部依賴。

## 跑型別檢查（可選）

Interface 簽名一致性靠型別檢查器強制（見 skill 嘅「簽名一致」原則）。Demo 已附設定檔：

```bash
pip install mypy pyright
cd demo
mypy       # 讀 mypy.ini（strict）
pyright    # 讀 pyrightconfig.json（standard）
```

兩個都應該係 0 error。

## 核心原則詳解

### 文件有階層

- **root `ARCHITECTURE.md`**：只畫元件地圖（邊個依賴邊個）同跨元件嘅主要流程，唔寫實作細節。
- **元件 `ARCHITECTURE.md`**：每個元件一份，寫職責、class／sequence diagram、資料契約同「唔負責咩」。
- **子元件**：只有符合開 interface 條件（跨 folder 使用、有多個可替換實作、接外部系統）先拆出嚟，同樣有自己嘅 `ARCHITECTURE.md`；喺父層嘅圖入面只當一個 participant。層數控制喺 2–3 層。
- 例子：[root](demo/ARCHITECTURE.md)、[元件](demo/pricing/ARCHITECTURE.md)、[子元件](demo/pricing/rules/ARCHITECTURE.md)。

### 資料形狀要寫明

- 返回值如果係固定 key 嘅結構，用 `TypedDict`，放喺元件嘅 `data_types.py` 並由 `__init__.py` 匯出。唔用裸 `dict`（睇唔出入面有咩），亦唔為咗包裝而硬砌 class（多咗隱藏邏輯，用起上嚟麻煩）。
- 值只可以係幾個固定字串，就用 `Literal`（例如 `CustomerTier`）。
- DataFrame 嘅 column 同 dtype 都係資料契約：column 清單只定義一次，文件同驗證共用；喺元件邊界驗證輸入同輸出（可以考慮 `pandera`）。
- 每個公開函式、class 都要有 Google style docstring（`Args:`、`Returns:`、`Raises:`、`Not responsible for:` 等）。

### 簽名相容交畀型別檢查器

- 原則：實作嘅簽名同 interface 相容：參數名、順序、kind 一致；型別按型別檢查器規則（參數可放寬、return 可收窄）。
- 留意工具保證嘅係「相容」，唔係「文字上完全相同」。
- 唔靠 AI 自覺，靠工具擋：Python 用 pyright 或 mypy，TypeScript 用 `tsc --strict`，Java／C# 由 compiler 負責。
- Demo 附咗 `demo/mypy.ini` 同 `demo/pyrightconfig.json`，見上面「跑型別檢查」。

### DIP 要做，但唔好令 interface 變亂（YAGNI）

- 實作 class 嘅 constructor 可以收 interface 型別嘅依賴，但呢啲參數只係元件內部嘅事。
- 組裝放喺元件 `__init__.py` 嘅工廠函式（例如 `default_pricer()`）；對外只匯出 interface、`TypedDict` 同工廠函式；實作 class 唔放入 `__all__`，約定其他 folder 只用工廠函式同 interface。Python 唔會強制，要強制就用依賴檢查。
- 冇 interface 嘅內部細 class（驗證、小計等）由實作自己建立，唔使注入。
- AI 如果為咗「將來可能替換」而新增公開參數或匯出實作 class，要講明係邊個具體需求；答唔到就唔加。
- Demo 對應：`demo/pricing/__init__.py` 同 `demo/pricing/standard_pricer.py`。

### 測試規則

- 測對外承諾（行為），唔鎖死內部結構。檢查標準：呢個 test 失敗，下游會唔會真係壞？下游依賴嘅 import 路徑、關鍵字參數名都算契約，可以測。
- 多個實作共用同一套 contract test，所以整個 class 換走時，行為保證仲喺度。

### 改 interface 要經人批准

- 預設所有 interface 改動都要批准。
- AI 會先估算有冇「同當前工作無關」嘅其他使用者（其他 folder 有冇引用），再向你講清楚影響範圍，主動問你批唔批。

### 接手舊項目

- 非 OOP 項目唔好一次過重寫：先喺現有 code 加一層薄薄嘅 caller（最少改動），先寫 characterization test 鎖住現有行為。
- 再喺新 folder 用 OOP 寫核心邏輯，同舊邏輯並行（shadow run）比對結果，滿意先切換，並保留回退。
- 核心邏輯大嘅話，逐件搬，root 圖用 `<<legacy>>` participant 表示未搬嘅部分。

### 誠實匯報

- AI 匯報時要分清楚：`PASSED`、`FAILED`、`NOT RUN`、`BLOCKED`，唔可以將冇跑過嘅 test 講成通過。

### 進階（可選，未驗證）

自動強制檢查、commit hash、test plan／notebook、分級批准，詳見 `SKILL.md` 嘅「進階」部分。
