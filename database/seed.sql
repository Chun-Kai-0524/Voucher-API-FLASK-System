-- Test Data for Voucher Management System
-- 測試資料

-- 插入測試優惠券
INSERT INTO vouchers (name, price, discount_percentage, expiry_date, is_available, status) VALUES
('新用戶註冊優惠', 100.00, 20.00, '2025-12-31 23:59:59', TRUE, 'unused'),
('週年慶優惠券', 500.00, 50.00, '2025-11-30 23:59:59', TRUE, 'unused'),
('黑色星期五特惠', 300.00, 30.00, '2025-11-29 23:59:59', TRUE, 'unused'),
('會員專屬折扣', 200.00, 15.00, '2025-12-15 23:59:59', TRUE, 'unused'),
('限時搶購優惠', 150.00, 25.00, '2025-11-20 23:59:59', TRUE, 'unused'),
('過期測試券', 200.00, 10.00, '2024-01-01 23:59:59', FALSE, 'expired'),
('已使用測試券', 300.00, 30.00, '2025-12-31 23:59:59', FALSE, 'used');

-- 更新已使用測試券的使用時間
UPDATE vouchers 
SET used_at = CURRENT_TIMESTAMP 
WHERE name = '已使用測試券';

