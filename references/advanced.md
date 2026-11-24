# 進階（可選，未必每個項目都需要）

### A. 強制機制
以上規則預設係 AI 要跟嘅指引。如果發現規則會被漏（文件有寫但 AI 仍然跳過），可以加自動檢查：
- 依賴檢查：跨 folder 只准 import interface（Python：import-linter；TS：dependency-cruiser；Java：ArchUnit）。
- Pre-commit 或 CI：改咗 interface 檔案但冇改 `ARCHITECTURE.md` 就失敗。
- 改 interface 檔案時要求批准標記。
- 型別同 docstring 檢查：型別用 mypy 或 pyright，docstring 用 ruff 嘅 `D` 規則（Google convention）。
- DataFrame 欄位驗證：邊界函式至少檢查必需欄位存在；建議用 `pandera`（或自己寫 decorator）連 dtype、null、數值範圍一齊檢查。留意每次呼叫都驗證有成本，只放喺 interface 邊界，必要時可喺 production 關閉。
- 實作簽名相容：參數名、順序、kind 要同 interface 一致；型別按型別檢查器嘅規則（參數可以放寬、return 可以收窄）。用型別檢查器強制：Python 用 pyright（`reportIncompatibleMethodOverride`）或 mypy，TypeScript 用 `tsc --strict`，Java／C# 編譯器本身會擋。留意工具保證嘅係「相容」，唔係「文字上完全相同」；要完全相同就要靠 review 或自訂檢查。唔好為咗呢點自己寫 runtime 檢查放入 skill。

### B. Commit hash 對應
喺 `ARCHITECTURE.md` 記錄 diagram 同 implementation 對應嘅 commit。注意 commit 唔可以包含自己嘅 hash，所以記錄嘅係上一個 commit。較穩陣嘅做法係用 script 偵測：比較 `git log -1 --format=%H -- <diagram>` 同 code 最後改動嘅 commit，而唔係手寫 hash。

### C. Test plan 同 notebook（只限重要 class）
- 只有重要嘅 class（核心邏輯、資料入口）先需要 test plan。
- Test plan 由 diagram 同 interface 推導：每個方法嘅正常、邊界、錯誤情況，由人確認「測乜」，然後先寫 test。
- Notebook 由 test plan 生成，畀人試玩同確認行為，**只係本地即棄物，唔入 git，壞咗先再生，唔維護**。
- 試玩時發現有用嘅 case，要升級返去 test plan 同 test，唔好留喺 notebook。
- Notebook 唔好放喺以 `.` 開頭嘅 folder（Jupyter 唔支援隱藏路徑，網址打唔開）。
- 除非用戶要求，唔好自行執行 notebook。

### D. 分級批准
當用戶累積咗經驗，可以將 interface 改動分級：自動（typo、private helper、不影響 interface）、事後通知（向後兼容嘅新增，而且冇無關嘅其他使用者）、必須批准（見上面清單）。由嚴開始，睇邊類批准次次都通過，再逐步放鬆。分級由用戶決定。
