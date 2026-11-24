# diagram-driven-coding

一個畀 AI 寫 code 用嘅 skill：用每個元件 folder 內嘅 `ARCHITECTURE.md`（class／sequence diagram、職責、資料契約）先行，配合 TDD 同 interface 分層，收窄 AI 改 code 嘅爆炸半徑。

*English: a skill that keeps AI-written changes inside a component boundary. Diagram first, then tests, then code. Interface changes need human approval.*

## 解決咩問題

叫 AI 改一個功能，佢順手改咗三個唔相關嘅檔案；改 A 壞 B；錯咗之後逐行 debug 慳唔到時間。

呢個 skill 唔係叫 AI「更加小心」，而係令佢冇得亂改：

- **邊界清楚**：每個元件一個 folder，只經 interface 對外，private helper 外面唔准碰。
- **先改圖、再寫 test、後實作**：圖係 AI 同人都睇得明嘅導航圖，亦係 review 嘅重點。
- **測對外承諾，唔測內部結構**：防止 AI 用大量結構測試製造虛假嘅 coverage 安全感。
- **改 interface 要經人批准**：AI 會先估算有冇「同當前工作無關」嘅其他使用者，再主動問你要唔要批准。
- **錯咗可以整個 class 換走**：多個實作共用同一套行為 contract test。

更多做法見下面「做法細節」。

## 做法細節

- **文件有階層**：root 一份元件地圖，每個元件（包括子元件）各自一份 `ARCHITECTURE.md`，每層只寫自己嗰層；子元件喺父層圖中只當一個 participant。
- **資料形狀要寫明**：返回值用 `TypedDict`（唔用裸 `dict`，亦唔為咗包裝而硬砌 class），固定選項用 `Literal`；DataFrame 就喺邊界驗證必要嘅 column。
- **簽名一致交畀型別檢查器**：實作嘅參數名、順序、型別、return 要同 interface 完全一致，Python 用 pyright／mypy 擋住，唔靠 AI 自覺。
- **DIP 要做，但唔好令 interface 變亂**：實作 constructor 可以收 interface 型別嘅依賴，但組裝放喺元件 `__init__.py` 嘅工廠函式，唔對外匯出實作 class，咁其他 folder 見唔到多出嚟嘅參數。
- **接手舊項目可以逐步嚟**：非 OOP 項目先加一層薄薄嘅 caller，再逐件將核心邏輯搬入新 folder，唔使一次過重寫。

## 內容

| 路徑 | 內容 |
| --- | --- |
| `SKILL.md` | skill 本體（核心做法、進階可選項、ARCHITECTURE.md 模板） |
| `demo/` | 一個細小嘅 Python 示範項目（root、元件、子元件各有 `ARCHITECTURE.md`），三個情境示範 skill 點樣運作，詳見 `demo/DEMO.md` |

## 點用

- **Claude Code**：將 `SKILL.md` 放入 `.claude/skills/diagram-driven-coding/SKILL.md`。
- **ChatGPT**：將 `SKILL.md` 嘅內容貼入 Project 或自訂 GPT 嘅 instructions，或者作為檔案上載；如果用 Codex，就併入項目嘅 `AGENTS.md`。
- **其他 AI 工具**：放入該工具嘅 skills 目錄，或者將內容併入項目嘅指引檔（例如 `CLAUDE.md`、`.cursorrules`）。

適用於中型以上、AI 會長期參與維護嘅項目。細 script 或一次性項目唔使用。

## 狀態

實驗中。核心做法來自一個真實項目嘅長期使用經驗；「進階」部分（自動強制檢查、commit hash、分級批准等）仲未驗證，請當作建議。

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
