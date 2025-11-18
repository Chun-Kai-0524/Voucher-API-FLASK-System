# 修復報告：PostgreSQL ENUM 狀態類型不匹配

## 問題描述

創建優惠券時發生 500 錯誤：
```
sqlalchemy.exc.DataError: invalid input value for enum voucher_status: "UNUSED"
```

## 根本原因

SQLAlchemy 模型與 PostgreSQL 資料庫的 ENUM 類型定義不一致：

1. **資料庫定義**（`database/init.sql`）：
   ```sql
   CREATE TYPE voucher_status AS ENUM ('unused', 'used', 'expired');
   ```
   → 期望**小寫值**

2. **Python 枚舉定義**（`app/models/voucher.py`）：
   ```python
   class VoucherStatus(PyEnum):
       UNUSED = "unused"  # 值是小寫
   ```
   → 但 SQLAlchemy 發送**枚舉名稱**（大寫）而非值（小寫）

3. **SQLAlchemy 配置問題**：
   - `native_enum=False` → 不使用資料庫原生 ENUM
   - 缺少 `name` 參數 → 自動創建新的 ENUM 類型 `voucherstatus`
   - 缺少 `values_callable` → 發送枚舉名稱而非值

## 解決方案

### 1. 修改枚舉類定義

**檔案**: `app/models/voucher.py`

```python
class VoucherStatus(str, PyEnum):
    """優惠券狀態枚舉"""
    UNUSED = "unused"
    USED = "used"
    EXPIRED = "expired"
    
    def __str__(self):
        return self.value  # 確保序列化時使用值而非名稱
```

### 2. 修改 SQLAlchemy 欄位定義

**檔案**: `app/models/voucher.py`

```python
status: Mapped[VoucherStatus] = mapped_column(
    Enum(
        VoucherStatus,
        name='voucher_status',           # 使用資料庫現有 ENUM 類型
        create_type=False,                # 不創建新類型
        native_enum=True,                 # 使用資料庫原生 ENUM
        values_callable=lambda x: [e.value for e in x]  # 使用枚舉值而非名稱
    ),
    nullable=False,
    default=VoucherStatus.UNUSED,
    comment="優惠券狀態"
)
```

### 3. 清理錯誤的 ENUM 類型

```bash
docker exec voucher_db psql -U voucher_user -d voucher_db \
  -c "DROP TYPE IF EXISTS voucherstatus CASCADE;"
```

## 修改文件清單

- ✅ `app/models/voucher.py` - 修改枚舉定義和欄位配置
- ✅ `docker-compose.yml` - 重建容器應用修復

## 驗證結果

### 修復前
```
❌ 500 Internal Server Error
❌ invalid input value for enum voucher_status: "UNUSED"
```

### 修復後
```
✅ 201 Created
✅ 成功創建優惠券 (ID: 2, 3, 4)
✅ 資料庫狀態正確: status = 'unused'
```

### 測試確認

```sql
SELECT id, name, price, discount_percentage, status 
FROM vouchers;

 id |     name     | price  | discount_percentage | status 
----+--------------+--------+---------------------+--------
  2 | 優惠券-200元 | 200.00 |               20.00 | unused
  3 | 優惠券-300元 | 300.00 |               20.00 | unused
  4 | 優惠券-400元 | 400.00 |               20.00 | unused
```

## 關鍵要點

1. **SQLAlchemy ENUM 與 PostgreSQL ENUM 必須一致**
   - 使用 `name` 參數指定資料庫 ENUM 類型名稱
   - 使用 `create_type=False` 避免重複創建

2. **Python 枚舉序列化**
   - 繼承 `str` 類型：`class VoucherStatus(str, PyEnum)`
   - 實作 `__str__` 方法返回 `.value`

3. **使用 `values_callable` 確保正確序列化**
   - `lambda x: [e.value for e in x]` 提取枚舉值

## 日期

修復日期：2025-11-18

---

## 相關問題

若遇到類似問題，檢查：
1. 資料庫 ENUM 定義 vs Python 枚舉定義
2. SQLAlchemy `Enum()` 參數配置
3. 使用 `docker-compose logs` 查看詳細錯誤訊息

