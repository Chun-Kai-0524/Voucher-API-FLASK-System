"""
Voucher Service
優惠券業務邏輯層
"""
from typing import List, Optional, Dict, Any
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.voucher import Voucher, VoucherStatus
from app.repositories.voucher_repository import VoucherRepository


class VoucherService:
    """優惠券業務邏輯服務"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = VoucherRepository(db)
    
    def create_voucher(self, data: Dict[str, Any]) -> Voucher:
        """
        創建優惠券
        
        Args:
            data: 優惠券資料
            
        Returns:
            Voucher: 創建的優惠券
            
        Raises:
            ValueError: 驗證失敗
        """
        # 業務規則驗證
        self._validate_voucher_data(data)
        
        # 創建優惠券
        voucher = self.repository.create(data)
        self.db.commit()
        
        return voucher
    
    def get_voucher(self, voucher_id: int) -> Optional[Voucher]:
        """
        查詢單一優惠券
        
        Args:
            voucher_id: 優惠券 ID
            
        Returns:
            Optional[Voucher]: 優惠券或 None
        """
        return self.repository.get_by_id(voucher_id)
    
    def list_vouchers(
        self,
        page: int = 1,
        per_page: int = 20,
        filters: Optional[Dict[str, Any]] = None
    ) -> tuple[List[Voucher], int, int]:
        """
        查詢優惠券列表
        
        Args:
            page: 頁碼
            per_page: 每頁數量
            filters: 篩選條件
            
        Returns:
            tuple: (優惠券列表, 總數, 總頁數)
        """
        vouchers, total = self.repository.get_all(page, per_page, filters)
        pages = (total + per_page - 1) // per_page
        
        return vouchers, total, pages
    
    def update_voucher(
        self,
        voucher_id: int,
        data: Dict[str, Any]
    ) -> Voucher:
        """
        更新優惠券
        
        Args:
            voucher_id: 優惠券 ID
            data: 更新資料
            
        Returns:
            Voucher: 更新後的優惠券
            
        Raises:
            ValueError: 驗證失敗或業務規則錯誤
        """
        voucher = self.repository.get_by_id(voucher_id)
        
        if not voucher:
            raise ValueError(f"Voucher with id {voucher_id} not found")
        
        # 驗證更新資料
        self._validate_update_data(voucher, data)
        
        # 執行更新
        updated_voucher = self.repository.update(voucher, data)
        self.db.commit()
        
        return updated_voucher
    
    def delete_voucher(self, voucher_id: int) -> None:
        """
        刪除優惠券
        
        Args:
            voucher_id: 優惠券 ID
            
        Raises:
            ValueError: 業務規則不允許刪除
        """
        voucher = self.repository.get_by_id(voucher_id)
        
        if not voucher:
            raise ValueError(f"Voucher with id {voucher_id} not found")
        
        # 業務規則檢查：已使用的優惠券不可刪除
        if not voucher.can_be_deleted():
            raise ValueError(
                f"Cannot delete voucher with status '{voucher.status.value}'. "
                "Used vouchers cannot be deleted."
            )
        
        self.repository.delete(voucher)
        self.db.commit()
    
    def _validate_voucher_data(self, data: Dict[str, Any]) -> None:
        """驗證優惠券資料"""
        # 價格驗證
        if 'price' in data:
            price = float(data['price'])
            if price <= 0:
                raise ValueError("Price must be greater than 0")
        
        # 折扣百分比驗證
        if 'discount_percentage' in data:
            discount = float(data['discount_percentage'])
            if discount < 0 or discount > 100:
                raise ValueError("Discount percentage must be between 0 and 100")
        
        # 有效期驗證
        if 'expiry_date' in data:
            expiry_date = data['expiry_date']
            if isinstance(expiry_date, str):
                # 如果是字串，會在 Schema 層轉換
                pass
            elif isinstance(expiry_date, datetime):
                # 建議但不強制要求未來日期
                pass
    
    def _validate_update_data(
        self,
        voucher: Voucher,
        data: Dict[str, Any]
    ) -> None:
        """驗證更新資料"""
        # 驗證基本欄位
        self._validate_voucher_data(data)
        
        # 狀態轉換驗證
        if 'status' in data:
            new_status = data['status']
            if isinstance(new_status, str):
                new_status = VoucherStatus(new_status)
            
            # 已使用或已過期的優惠券不可改變狀態
            if voucher.status in [VoucherStatus.USED, VoucherStatus.EXPIRED]:
                if new_status != voucher.status:
                    raise ValueError(
                        f"Cannot change status from '{voucher.status.value}' "
                        f"to '{new_status.value}'"
                    )
            
            # 如果標記為已使用，需要設定使用時間
            if new_status == VoucherStatus.USED and 'used_at' not in data:
                data['used_at'] = datetime.utcnow()
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        取得統計資訊
        
        Returns:
            Dict: 統計資料
        """
        status_counts = self.repository.count_by_status()
        
        return {
            'total': sum(status_counts.values()),
            'by_status': status_counts
        }

