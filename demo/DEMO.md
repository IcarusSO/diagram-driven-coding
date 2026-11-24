# Demo：訂單定價

```
demo/
  ARCHITECTURE.md        Root：元件地圖、依賴方向、跨元件流程
  pricing/               元件：interface、驗證、小計、TypedDict 型別、ARCHITECTURE.md、行為測試
    rules/               子元件：折扣同稅（DiscountRule、TaxRule 兩個 interface 加兩個實作），有自己嘅 ARCHITECTURE.md
  checkout/              下游使用者 1：文字收據，有自己嘅 ARCHITECTURE.md
  reports/               下游使用者 2：每日銷售總額，有自己嘅 ARCHITECTURE.md
```

```bash
cd demo
python3 -m unittest discover -v     # 14 個測試，應該全部通過
```

## 先睇圖同型別，唔使讀實作

1. 由上至下讀文件，每層只讀需要嘅：
   - `ARCHITECTURE.md`（root）：有邊啲元件、誰依賴誰、跨元件流程。
   - `pricing/ARCHITECTURE.md`：計價元件嘅 **class diagram**、**class 職責表**、**sequence diagram**；折扣同稅只係一個子元件參與者，連去下一層。
   - `pricing/rules/ARCHITECTURE.md`：折扣同稅嘅 class、職責、協作（含 private helper）。
2. 打開 `pricing/data_types.py`：輸入 `Order`、輸出 `PriceBreakdown` 都係 `TypedDict`，每個欄位嘅意思、單位、範圍寫喺 docstring 嘅 `Attributes:`。
3. 任何 public 函式、class 都有 Google 風格 docstring（`Args:`／`Returns:`／`Raises:`），例如 `pricing/interface.py`。

AI 改 code 之前只需要讀 root 加目標元件嗰兩層文件同型別，就知道應該改邊個 class、資料長咩樣。

## 情境一：改折扣規則 → 只郁一個 class

> 新規則：訂單滿 £200，基本折扣由 10% 升至 15%。

已經喺 git 歷史做好（真實執行，每步都跑過測試）：

| 步驟 | commit | 發生咩事 |
| --- | --- | --- |
| 1a | 寫 test（RED） | 只改 `pricing/rules/tests/test_discount_policy.py`，新規則嘅 case 失敗 |
| 1b | 實作（GREEN） | 只改 `pricing/rules/discount_policy.py`（包括 docstring 內嘅規則說明），全部通過 |

```bash
git diff --stat demo-baseline demo-scenario-1-done
# 只有兩個檔案：pricing/rules/discount_policy.py 同佢嘅 test
```

重點：
- 其他 class、`Pricer` 嘅 contract test、兩個下游使用者全部冇郁。
- 三層 `ARCHITECTURE.md`（root、`pricing`、`pricing/rules`）都冇郁，因為冇改 interface、職責或資料契約。
- `Pricer` contract test 刻意唔寫死折扣金額，折扣規則由 `DiscountPolicy` 自己嘅 test 負責，所以改規則唔會連累其他檔案。

## 情境二：class 壞咗 → 整個換，唔逐行 debug

| 步驟 | commit | 發生咩事 |
| --- | --- | --- |
| 2a | 壞咗（RED） | **模擬**一次未審查嘅 AI 改動：`TaxCalculator` 改用浮點乘法加截斷，例如 1999 便士嘅 20% 變成 399 而唔係 400 |
| 2b | 整個重寫（GREEN） | 只靠 `ARCHITECTURE.md` 嘅職責同 `TaxCalculator` 自己嘅行為測試重寫成個 class |

2a 嗰度，失敗嘅測試會指向稅：`TaxCalculator` 自己嘅 3 個 case、`Pricer` 嘅契約 1 個、兩個下游各 1 個（共 6 個失敗）。睇一眼就知問題喺稅。順帶一提：2a 嘅壞版本仍然有 docstring，可見 docstring 唔會攔住 bug，攔住嘅係行為測試。

```bash
git diff --stat demo-scenario-1-done demo-scenario-2-done
# 只有 pricing/rules/tax_calculator.py 一個檔案
```

重點：
- 重寫時 public method（`tax(taxable_pence)`）不變，所以其他 class 同下游唔使改。
- 成立前提：class 夠細、職責單一、有行為測試。如果契約本身錯咗，換 class 解決唔到。
- 注意：2a 嘅「壞咗」係我為咗示範而模擬嘅，唔係真係 AI 亂改出嚟。

## 情境三：改輸出欄位 → AI 要停低，等你批准

呢個情境要你用自己嘅 AI 工具跑一次。

1. 退回起點，用 AI 工具打開 `demo/` 目錄（Claude Code 讀 `CLAUDE.md`、Codex 讀 `AGENTS.md`，兩份內容一致，都會指示 AI 跟 `../SKILL.md`）：
   ```bash
   git checkout demo-scenario-2-done
   ```
2. 對 AI 講：

   > 請將 Pricer 輸出嘅金額由整數便士改成英鎊（小數），欄位改名做 `subtotal_gbp`、`discount_gbp`、`tax_gbp`、`total_gbp`。

3. 試完返回最新：`git checkout master`。

### 預期行為（用嚟對照，唔係保證）

AI 應該：
- [ ] **未改任何檔案之前就停低**，因為呢個係資料結構、單位同語義嘅改動。
- [ ] **主動搜尋使用者**，搵到同呢個改動無關嘅下游：`checkout/receipt.py`、`reports/daily_sales.py` 同佢哋嘅 test；亦可以靠 root `ARCHITECTURE.md` 嘅依賴圖確認。
- [ ] **報告前後契約對比**：`PriceBreakdown` 嘅欄位名、型別、單位、原因、受影響嘅使用者、係咪破壞性改動。
- [ ] **建議每次都要批准**（因為有無關嘅使用者），並問你「呢類改動下次需唔需要事先批准？」。

你批准之後，AI 應該按順序：先改 `pricing/ARCHITECTURE.md` 嘅資料契約，同 `PriceBreakdown`（含 docstring）→ 改 `Pricer` contract test（先見失敗）→ 改實作 → 同步改兩個下游、佢哋自己嘅 `ARCHITECTURE.md`（資料契約提到 `total_pence` 等欄位）同 test，root `ARCHITECTURE.md` 嘅元件表如有提到欄位亦要同步 → 報告 `PASSED`／`FAILED` 同證據。

### 如果 AI 冇停低

即係規則冇被跟從，呢個係有價值嘅結果，代表：
- 指引要寫得更明確，或者
- 要用 skill「進階」部分嘅自動檢查，例如改 interface 檔案但冇改 `ARCHITECTURE.md` 就令 CI 失敗。

## 狀態

- 情境一、二：真實執行嘅 git 歷史，1a 同 2a 刻意係 RED，其餘每一步都跑過測試。
- 型別檢查已跑：`cd demo && mypy`（`mypy.ini`，strict）同 `pyright`（`pyrightconfig.json`，standard）對 source 同 tests 都係 0 error；三個 tag 同 HEAD 嘅 14 個 test 都通過。
- 如果改用 pyright strict，`pricing/order_validator.py` 會有 3 個 `reportUnnecessaryIsInstance`：嗰度刻意用 `isinstance` 驗證唔受信任嘅輸入，所以示範用 standard。
- 情境三：預期行為對照清單，**未有喺真實 AI 工具跑過嘅結果記錄**。跑完之後請按實際情況修改呢個檔案。
