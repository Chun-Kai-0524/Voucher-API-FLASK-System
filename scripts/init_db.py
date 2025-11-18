#!/usr/bin/env python3
"""
Database Initialization Script
資料庫初始化腳本
"""
import sys
import os

# 添加專案根目錄到路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import init_db, engine
from app.config import get_config

def main():
    """初始化資料庫"""
    config = get_config()
    
    print(f"Initializing database...")
    print(f"Database URL: {config.SQLALCHEMY_DATABASE_URI}")
    
    try:
        # 建立表格
        init_db()
        print("[OK] Database tables created successfully!")
        
        # 驗證表格
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"[OK] Tables created: {', '.join(tables)}")
        
        # 可選：插入測試資料
        insert_test_data = input("\nDo you want to insert test data? (y/N): ")
        if insert_test_data.lower() == 'y':
            from app.database import SessionLocal
            from app.models.voucher import Voucher, VoucherStatus
            from datetime import datetime, timedelta
            from decimal import Decimal
            
            db = SessionLocal()
            try:
                test_vouchers = [
                    {
                        'name': '新用戶註冊優惠',
                        'price': Decimal('100.00'),
                        'discount_percentage': Decimal('20.00'),
                        'expiry_date': datetime.utcnow() + timedelta(days=45),
                        'is_available': True,
                        'status': VoucherStatus.UNUSED
                    },
                    {
                        'name': '週年慶優惠券',
                        'price': Decimal('500.00'),
                        'discount_percentage': Decimal('50.00'),
                        'expiry_date': datetime.utcnow() + timedelta(days=30),
                        'is_available': True,
                        'status': VoucherStatus.UNUSED
                    },
                    {
                        'name': '黑色星期五特惠',
                        'price': Decimal('300.00'),
                        'discount_percentage': Decimal('30.00'),
                        'expiry_date': datetime.utcnow() + timedelta(days=15),
                        'is_available': True,
                        'status': VoucherStatus.UNUSED
                    }
                ]
                
                for voucher_data in test_vouchers:
                    voucher = Voucher(**voucher_data)
                    db.add(voucher)
                
                db.commit()
                print(f"[OK] Inserted {len(test_vouchers)} test vouchers!")
            except Exception as e:
                db.rollback()
                print(f"[ERROR] Error inserting test data: {e}")
            finally:
                db.close()
        
        print("\n[OK] Database initialization completed!")
        
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

