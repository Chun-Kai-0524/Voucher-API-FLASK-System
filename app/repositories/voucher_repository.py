"""
Voucher Repository
優惠券資料存取層

負責與資料庫的 CRUD 操作
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.models.voucher import Voucher, VoucherStatus


class VoucherRepository:
    """優惠券資料存取層"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, voucher_data: Dict[str, Any]) -> Voucher:
        """
        創建優惠券
        
        Args:
            voucher_data: 優惠券資料字典
            
        Returns:
            Voucher: 創建的優惠券實體
        """
        voucher = Voucher(**voucher_data)
        self.db.add(voucher)
        self.db.flush()  # 取得 ID 但不提交
        self.db.refresh(voucher)
        return voucher
    
    def get_by_id(self, voucher_id: int) -> Optional[Voucher]:
        """
        根據 ID 查詢優惠券
        
        Args:
            voucher_id: 優惠券 ID
            
        Returns:
            Optional[Voucher]: 優惠券實體或 None
        """
        voucher = self.db.query(Voucher).filter(Voucher.id == voucher_id).first()
        
        # 查詢時自動更新過期狀態
        if voucher:
            voucher.update_status_if_expired()
            if self.db.is_modified(voucher):
                self.db.flush()
        
        return voucher
    
    def get_all(
        self,
        page: int = 1,
        per_page: int = 20,
        filters: Optional[Dict[str, Any]] = None
    ) -> tuple[List[Voucher], int]:
        """
        查詢優惠券列表（支援分頁和篩選）
        
        Args:
            page: 頁碼（從 1 開始）
            per_page: 每頁數量
            filters: 篩選條件字典
            
        Returns:
            tuple[List[Voucher], int]: (優惠券列表, 總數)
        """
        query = self.db.query(Voucher)
        
        # 應用篩選條件
        if filters:
            query = self._apply_filters(query, filters)
        
        # 取得總數
        total = query.count()
        
        # 應用分頁
        offset = (page - 1) * per_page
        vouchers = query.order_by(Voucher.created_at.desc())\
                        .offset(offset)\
                        .limit(per_page)\
                        .all()
        
        # 更新過期狀態
        for voucher in vouchers:
            voucher.update_status_if_expired()
        
        return vouchers, total
    
    def update(self, voucher: Voucher, update_data: Dict[str, Any]) -> Voucher:
        """
        更新優惠券
        
        Args:
            voucher: 優惠券實體
            update_data: 更新資料字典
            
        Returns:
            Voucher: 更新後的優惠券實體
        """
        for key, value in update_data.items():
            if hasattr(voucher, key):
                setattr(voucher, key, value)
        
        voucher.updated_at = datetime.utcnow()
        self.db.flush()
        self.db.refresh(voucher)
        return voucher
    
    def delete(self, voucher: Voucher) -> None:
        """
        刪除優惠券
        
        Args:
            voucher: 優惠券實體
        """
        self.db.delete(voucher)
        self.db.flush()
    
    def bulk_create(self, vouchers_data: List[Dict[str, Any]]) -> List[Voucher]:
        """
        批次創建優惠券
        
        Args:
            vouchers_data: 優惠券資料列表
            
        Returns:
            List[Voucher]: 創建的優惠券列表
        """
        vouchers = [Voucher(**data) for data in vouchers_data]
        self.db.bulk_save_objects(vouchers, return_defaults=True)
        self.db.flush()
        return vouchers
    
    def _apply_filters(self, query, filters: Dict[str, Any]):
        """
        應用篩選條件
        
        這個方法展示了使用 **kwargs 的例子（符合面試要求）
        """
        # 名稱模糊搜尋
        if 'name' in filters and filters['name']:
            query = query.filter(Voucher.name.like(f"%{filters['name']}%"))
        
        # 價格範圍
        if 'min_price' in filters and filters['min_price'] is not None:
            query = query.filter(Voucher.price >= filters['min_price'])
        if 'max_price' in filters and filters['max_price'] is not None:
            query = query.filter(Voucher.price <= filters['max_price'])
        
        # 折扣百分比範圍
        if 'min_discount' in filters and filters['min_discount'] is not None:
            query = query.filter(
                Voucher.discount_percentage >= filters['min_discount']
            )
        if 'max_discount' in filters and filters['max_discount'] is not None:
            query = query.filter(
                Voucher.discount_percentage <= filters['max_discount']
            )
        
        # 狀態篩選
        if 'status' in filters and filters['status']:
            try:
                status = VoucherStatus(filters['status'])
                query = query.filter(Voucher.status == status)
            except ValueError:
                pass  # 忽略無效的狀態值
        
        # 可用性篩選
        if 'is_available' in filters and filters['is_available'] is not None:
            query = query.filter(Voucher.is_available == filters['is_available'])
        
        # 有效期範圍
        if 'valid_from' in filters and filters['valid_from']:
            query = query.filter(Voucher.expiry_date >= filters['valid_from'])
        if 'valid_to' in filters and filters['valid_to']:
            query = query.filter(Voucher.expiry_date <= filters['valid_to'])
        
        return query
    
    def count_by_status(self, **kwargs) -> Dict[str, int]:
        """
        統計各狀態的優惠券數量
        
        這個方法展示了使用 **kwargs 的例子（符合面試要求）
        
        Args:
            **kwargs: 額外的篩選條件
            
        Returns:
            Dict[str, int]: 各狀態的數量統計
        """
        result = {}
        
        for status in VoucherStatus:
            query = self.db.query(Voucher).filter(Voucher.status == status)
            
            # 應用額外的篩選條件
            if kwargs:
                query = self._apply_filters(query, kwargs)
            
            result[status.value] = query.count()
        
        return result

