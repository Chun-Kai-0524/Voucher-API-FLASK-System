-- Voucher Management System Database Initialization
-- SQLite Version (For Development)

-- 建立優惠券表
CREATE TABLE IF NOT EXISTS vouchers (
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

-- 建立索引
CREATE INDEX IF NOT EXISTS idx_status ON vouchers(status);
CREATE INDEX IF NOT EXISTS idx_expiry_date ON vouchers(expiry_date);
CREATE INDEX IF NOT EXISTS idx_is_available ON vouchers(is_available);
CREATE INDEX IF NOT EXISTS idx_created_at ON vouchers(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_name ON vouchers(name);
CREATE INDEX IF NOT EXISTS idx_status_expiry ON vouchers(status, expiry_date);

-- 建立 updated_at 自動更新觸發器
CREATE TRIGGER IF NOT EXISTS update_voucher_updated_at
    AFTER UPDATE ON vouchers
    FOR EACH ROW
BEGIN
    UPDATE vouchers SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

