# Data Model: Voucher Management System

**Feature**: 001-voucher-api-system  
**Created**: 2025-11-14  
**Status**: Design

## Entity: Voucher (優惠券)

### Purpose
優惠券實體代表系統中可用於折扣的券碼。每張優惠券有唯一識別碼、價格資訊、折扣力度、有效期限和使用狀態。

### Fields

| Field Name | Type | Constraints | Description |
|------------|------|-------------|-------------|
| `id` | Integer | PRIMARY KEY, AUTO_INCREMENT | 優惠券唯一識別碼 |
| `name` | String(100) | NOT NULL | 優惠券名稱，描述用途 |
| `price` | Decimal(10,2) | NOT NULL, > 0 | 優惠券面額/原價 |
| `discount_percentage` | Decimal(5,2) | NOT NULL, >= 0, <= 100 | 折扣百分比 (0-100) |
| `expiry_date` | DateTime | NOT NULL | 優惠券到期日期時間 (UTC) |
| `is_available` | Boolean | NOT NULL, DEFAULT TRUE | 是否可用 |
| `status` | Enum | NOT NULL, DEFAULT 'unused' | 狀態: unused/used/expired |
| `created_at` | DateTime | NOT NULL, AUTO | 創建時間 (UTC) |
| `updated_at` | DateTime | NOT NULL, AUTO | 最後修改時間 (UTC) |
| `used_at` | DateTime | NULLABLE | 使用時間 (UTC)，當狀態變為 used 時記錄 |

### Status Enum Values
- `unused` - 未使用（初始狀態）
- `used` - 已使用（已被消費）
- `expired` - 過期（超過有效期）

### Business Rules

1. **狀態自動判定**
   - 當 `expiry_date < NOW()` 時，狀態應為 `expired`
   - 查詢時動態判斷或使用觸發器更新

2. **狀態轉換規則**
   - `unused` → `used`: 允許（正常使用流程）
   - `unused` → `expired`: 自動（時間到期）
   - `used` → 其他: 不允許（已使用不可改變）
   - `expired` → 其他: 不允許（過期不可復原）

3. **刪除限制**
   - 狀態為 `used` 的優惠券不可刪除
   - 狀態為 `unused` 或 `expired` 的優惠券可刪除

4. **可用性規則**
   - 當 `status = 'expired'` 時，`is_available` 應為 `false`
   - 當 `status = 'used'` 時，建議 `is_available` 為 `false`

5. **使用時間記錄**
   - 當狀態從 `unused` 變更為 `used` 時，必須記錄 `used_at = NOW()`

### Indexes

```sql
-- 主鍵索引（自動）
PRIMARY KEY (id)

-- 查詢優化索引
INDEX idx_status (status)                    -- 按狀態查詢
INDEX idx_expiry_date (expiry_date)          -- 按有效期查詢
INDEX idx_is_available (is_available)         -- 按可用性查詢
INDEX idx_created_at (created_at DESC)        -- 按創建時間排序
INDEX idx_name (name)                         -- 按名稱搜尋（可選用 FULLTEXT）

-- 複合索引（效能優化）
INDEX idx_status_expiry (status, expiry_date) -- 組合查詢優化
```

### Validation Rules

#### Field Validations
- `name`: 
  - 不可為空
  - 長度 1-100 字元
  - 允許 Unicode 字元（中文、英文等）
  
- `price`:
  - 必須 > 0
  - 最大值: 99999999.99 (10 digits, 2 decimals)
  - 精確到小數點後 2 位
  
- `discount_percentage`:
  - 範圍: 0.00 ~ 100.00
  - 精確到小數點後 2 位
  - 0 表示無折扣，100 表示全免
  
- `expiry_date`:
  - 必須為有效的 ISO 8601 日期時間格式
  - 建議為 UTC 時區
  - 創建時建議 >= 當前時間（但不強制）
  
- `status`:
  - 只能是 'unused', 'used', 'expired' 三者之一
  - 大小寫敏感

#### Business Validations
- 不可將 `status = 'used'` 的優惠券狀態改為其他值
- 不可將 `status = 'expired'` 的優惠券狀態改為其他值
- 當修改 `status` 為 'used' 時，必須同時設定 `used_at`

### SQLAlchemy 2.0 Model Structure

```python
from datetime import datetime
from decimal import Decimal
from enum import Enum as PyEnum
from sqlalchemy import String, Numeric, Boolean, DateTime, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class VoucherStatus(PyEnum):
    UNUSED = "unused"
    USED = "used"
    EXPIRED = "expired"

class Base(DeclarativeBase):
    pass

class Voucher(Base):
    __tablename__ = "vouchers"
    
    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Basic Information
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    discount_percentage: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    
    # Date/Time Fields
    expiry_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    used_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    
    # Status Fields
    is_available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    status: Mapped[VoucherStatus] = mapped_column(
        Enum(VoucherStatus, native_enum=False),
        nullable=False,
        default=VoucherStatus.UNUSED
    )
```

### Example Data

```json
{
  "id": 1,
  "name": "新用戶註冊優惠券",
  "price": 100.00,
  "discount_percentage": 20.00,
  "expiry_date": "2025-12-31T23:59:59Z",
  "is_available": true,
  "status": "unused",
  "created_at": "2025-11-14T10:00:00Z",
  "updated_at": "2025-11-14T10:00:00Z",
  "used_at": null
}
```

### Migration Notes

#### Initial Table Creation (PostgreSQL)

```sql
CREATE TYPE voucher_status AS ENUM ('unused', 'used', 'expired');

CREATE TABLE vouchers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price > 0),
    discount_percentage NUMERIC(5, 2) NOT NULL CHECK (discount_percentage >= 0 AND discount_percentage <= 100),
    expiry_date TIMESTAMP NOT NULL,
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    status voucher_status NOT NULL DEFAULT 'unused',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    used_at TIMESTAMP NULL
);

-- Indexes
CREATE INDEX idx_status ON vouchers(status);
CREATE INDEX idx_expiry_date ON vouchers(expiry_date);
CREATE INDEX idx_is_available ON vouchers(is_available);
CREATE INDEX idx_created_at ON vouchers(created_at DESC);
CREATE INDEX idx_name ON vouchers(name);
CREATE INDEX idx_status_expiry ON vouchers(status, expiry_date);

-- Trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_voucher_updated_at
    BEFORE UPDATE ON vouchers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

#### Initial Table Creation (SQLite - Development)

```sql
CREATE TABLE vouchers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
    discount_percentage DECIMAL(5, 2) NOT NULL CHECK (discount_percentage >= 0 AND discount_percentage <= 100),
    expiry_date DATETIME NOT NULL,
    is_available BOOLEAN NOT NULL DEFAULT 1,
    status VARCHAR(10) NOT NULL DEFAULT 'unused' CHECK (status IN ('unused', 'used', 'expired')),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    used_at DATETIME NULL
);

-- Indexes
CREATE INDEX idx_status ON vouchers(status);
CREATE INDEX idx_expiry_date ON vouchers(expiry_date);
CREATE INDEX idx_is_available ON vouchers(is_available);
CREATE INDEX idx_created_at ON vouchers(created_at DESC);
CREATE INDEX idx_name ON vouchers(name);
CREATE INDEX idx_status_expiry ON vouchers(status, expiry_date);

-- Trigger for updated_at
CREATE TRIGGER update_voucher_updated_at
    AFTER UPDATE ON vouchers
    FOR EACH ROW
BEGIN
    UPDATE vouchers SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
```

### Test Data

```sql
-- Sample vouchers for testing
INSERT INTO vouchers (name, price, discount_percentage, expiry_date, is_available, status) VALUES
('新用戶註冊優惠', 100.00, 20.00, '2025-12-31 23:59:59', TRUE, 'unused'),
('週年慶優惠券', 500.00, 50.00, '2025-11-30 23:59:59', TRUE, 'unused'),
('過期測試券', 200.00, 10.00, '2024-01-01 23:59:59', FALSE, 'expired'),
('已使用測試券', 300.00, 30.00, '2025-12-31 23:59:59', FALSE, 'used');
```

## Relationships

Currently, the Voucher entity is standalone with no relationships to other entities. 

### Future Considerations

If the system expands, possible relationships might include:

- **User** (一對多): 一個用戶可擁有多張優惠券
- **Order** (多對一): 多張優惠券可用於一個訂單
- **Campaign** (多對一): 多張優惠券屬於一個促銷活動

These are not in the current scope but documented for future reference.

## Database Schema Diagram

```
┌─────────────────────────────────────────┐
│              Vouchers                    │
├─────────────────────────────────────────┤
│ PK  id                INTEGER            │
│     name              VARCHAR(100)       │
│     price             DECIMAL(10,2)      │
│     discount_percentage DECIMAL(5,2)     │
│     expiry_date       DATETIME           │
│     is_available      BOOLEAN            │
│     status            ENUM               │
│     created_at        DATETIME           │
│     updated_at        DATETIME           │
│     used_at           DATETIME (NULL)    │
└─────────────────────────────────────────┘
```

## Performance Considerations

1. **Indexing Strategy**: 已定義多個索引以優化常見查詢模式
2. **Pagination**: 列表查詢必須使用分頁，避免一次性載入大量數據
3. **Status Calculation**: 考慮使用觸發器或定時任務自動更新過期狀態
4. **Batch Operations**: 批次創建/更新時使用 bulk insert/update 提升效能

