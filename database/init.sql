-- Voucher Management System Database Initialization
-- 優惠券管理系統資料庫初始化腳本

-- PostgreSQL Version

-- 建立狀態枚舉類型
CREATE TYPE voucher_status AS ENUM ('unused', 'used', 'expired');

-- 建立優惠券表
CREATE TABLE IF NOT EXISTS vouchers (
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

-- 建立索引
CREATE INDEX idx_status ON vouchers(status);
CREATE INDEX idx_expiry_date ON vouchers(expiry_date);
CREATE INDEX idx_is_available ON vouchers(is_available);
CREATE INDEX idx_created_at ON vouchers(created_at DESC);
CREATE INDEX idx_name ON vouchers(name);
CREATE INDEX idx_status_expiry ON vouchers(status, expiry_date);

-- 建立 updated_at 自動更新觸發器
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

-- 建立註解
COMMENT ON TABLE vouchers IS '優惠券資料表';
COMMENT ON COLUMN vouchers.id IS '優惠券唯一識別碼';
COMMENT ON COLUMN vouchers.name IS '優惠券名稱';
COMMENT ON COLUMN vouchers.price IS '優惠券面額/原價';
COMMENT ON COLUMN vouchers.discount_percentage IS '折扣百分比 (0-100)';
COMMENT ON COLUMN vouchers.expiry_date IS '優惠券到期日期時間 (UTC)';
COMMENT ON COLUMN vouchers.is_available IS '是否可用';
COMMENT ON COLUMN vouchers.status IS '優惠券狀態: unused/used/expired';
COMMENT ON COLUMN vouchers.created_at IS '創建時間 (UTC)';
COMMENT ON COLUMN vouchers.updated_at IS '最後修改時間 (UTC)';
COMMENT ON COLUMN vouchers.used_at IS '使用時間 (UTC)';

