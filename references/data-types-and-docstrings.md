# 資料型別細節同 docstring 規範

由 `SKILL.md` 第 4 點引用。

## DataFrame 契約

欄位同 dtype 型別表達唔到，所以係資料契約，要寫入契約表（欄位、dtype、單位、可否有 null、多出嘅欄位係咪容許）。欄位清單只定義一次（例如 `data_types.py` 嘅常數），文件表同驗證共用，唔好兩邊各抄一份。跨 folder 嘅函式喺邊界驗證輸入同輸出，內部 private helper 唔使重複驗證。

## Docstring（Google 風格，必須）
- 範圍：所有 public module、class、method、function、TypedDict 必須有完整 docstring。private helper 至少一行摘要。測試靠描述性嘅名，docstring 可選。
- 語言隨項目，但章節標題固定用英文 `Args:`、`Returns:`、`Raises:`、`Attributes:`，工具同 AI 都認得。
- 第一行：一句祈使句摘要（`Return ...`、`Calculate ...`），一行寫完。
- `Args:` 每個參數一行：`名稱: 意思，單位，範圍`。
- `Returns:` 講返回咩、單位、保證（例如排序、唔超過某值）。返回 TypedDict 時，欄位意思寫喺 TypedDict 嘅 `Attributes:`，唔好喺度重複。
- `Raises:` 每種例外同觸發條件；冇就唔寫呢節。
- 有副作用或不變量先加 `Note:`（例如「唔會改動傳入嘅 order」）。
- Class docstring：一句職責，加 `Not responsible for:`，要同 `ARCHITECTURE.md` 嘅職責表一致。
- TypedDict docstring：一句說明，加 `Attributes:` 逐欄位寫意思、單位、範圍。

標準範本：

```python
class OrderItem(TypedDict):
    """One line of an order.

    Attributes:
        sku: Product identifier, non-empty.
        unit_price_pence: Price of one unit in pence, at least 0.
        quantity: Number of units, at least 1.
    """

    sku: str
    unit_price_pence: int
    quantity: int


class DiscountPolicy:
    """Decide the discount for an order subtotal.

    Not responsible for: tax, validation.
    """

    def discount(self, subtotal_pence: int, customer_tier: CustomerTier) -> int:
        """Return the discount for a subtotal.

        Args:
            subtotal_pence: Order subtotal in pence, at least 0.
            customer_tier: Customer tier. "vip" adds 5% on top of the base rate.

        Returns:
            Discount in pence, never more than the subtotal.
        """
```
