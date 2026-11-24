# 接手既有非 OOP 項目

由 `SKILL.md` 第 10 點引用。

舊項目冇元件邊界、冇圖、可能冇測試時，唔好一次過重寫。用 strangler 方式逐塊搬：

1. **搵入口**：搵到核心邏輯嘅入口，向舊 code 注入一個薄 caller（改動最少）。
2. **釘死現有行為**：舊 code 冇測試時，先寫 characterization test 記錄「而家做緊咩」，包括輸出同下游依賴嘅格式。
3. **開新元件 folder**：interface、`TypedDict`、`ARCHITECTURE.md`，只放呢一塊核心邏輯。
4. **新元件過同一批測試**，高風險邏輯可以新舊兩邊都跑，比較結果（shadow run）。
5. **切換 caller**，並保留退返用舊路徑嘅方法（例如開關）。
6. **驗證後刪舊 path**，連 adapter 一齊刪，再搬下一塊。

**幾時先值得搬**：符合其中幾項先搬：核心邏輯大、經常改、AI 成日改壞、輸入輸出邊界清楚。細 script、膠水 code、純函式唔使硬轉 OOP；純函式加 `TypedDict` 已經足夠，class 一定要有行為職責。

**注入 caller 要薄**：
- 只做兩件事：將舊資料轉成新元件嘅 `TypedDict`，然後呼叫新 interface。唔放任何業務邏輯。
- 放喺舊 code 一側（例如 `legacy_adapter`），方便日後一齊刪走。
- 注入 caller 等於新增跨 folder 依賴，按第 7 點預設要批准。

**文件**：新元件有自己嘅 `ARCHITECTURE.md`。舊 code 喺 root 圖同 sequence diagram 只畫成一個 `<<legacy>>` 參與者，唔展開；每次只搬一塊，唔好一次過畫晒成個舊系統。
