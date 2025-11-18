"""
Voucher Model
優惠券資料模型 - 使用 SQLAlchemy 2.0 語法
"""
from datetime import datetime
from decimal import Decimal
from enum import Enum as PyEnum
from typing import Optional

from sqlalchemy import String, Numeric, Boolean, DateTime, Enum, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class VoucherStatus(str, PyEnum):
    """優惠券狀態枚舉"""
    UNUSED = "unused"
    USED = "used"
    EXPIRED = "expired"
    
    def __str__(self):
        return self.value


class Voucher(Base):
    """
    優惠券模型
    
    使用 SQLAlchemy 2.0 的 Mapped 類型提示和 mapped_column
    符合面試要求的 2.0 語法
    """
    __tablename__ = "vouchers"
    
    # 主鍵
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # 基本資訊
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="優惠券名稱"
    )
    
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        comment="優惠券面額/原價"
    )
    
    discount_percentage: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        comment="折扣百分比 (0-100)"
    )
    
    # 日期時間欄位
    expiry_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        comment="優惠券到期日期時間 (UTC)"
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        comment="創建時間 (UTC)"
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="最後修改時間 (UTC)"
    )
    
    used_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="使用時間 (UTC)"
    )
    
    # 狀態欄位
    is_available: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        comment="是否可用"
    )
    
    status: Mapped[VoucherStatus] = mapped_column(
        Enum(VoucherStatus, name='voucher_status', create_type=False, native_enum=True, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=VoucherStatus.UNUSED,
        comment="優惠券狀態"
    )
    
    # 索引定義
    __table_args__ = (
        Index('idx_status', 'status'),
        Index('idx_expiry_date', 'expiry_date'),
        Index('idx_is_available', 'is_available'),
        Index('idx_created_at', 'created_at'),
        Index('idx_name', 'name'),
        Index('idx_status_expiry', 'status', 'expiry_date'),
    )
    
    def __repr__(self) -> str:
        return f"<Voucher(id={self.id}, name='{self.name}', status='{self.status.value}')>"
    
    def is_expired(self) -> bool:
        """檢查優惠券是否過期"""
        return datetime.utcnow() > self.expiry_date
    
    def can_be_used(self) -> bool:
        """檢查優惠券是否可以使用"""
        return (
            self.is_available and 
            self.status == VoucherStatus.UNUSED and 
            not self.is_expired()
        )
    
    def can_be_deleted(self) -> bool:
        """檢查優惠券是否可以刪除"""
        # 已使用的優惠券不可刪除
        return self.status != VoucherStatus.USED
    
    def mark_as_used(self) -> None:
        """標記優惠券為已使用"""
        if self.status != VoucherStatus.UNUSED:
            raise ValueError(f"Cannot mark {self.status.value} voucher as used")
        
        self.status = VoucherStatus.USED
        self.used_at = datetime.utcnow()
        self.is_available = False
    
    def update_status_if_expired(self) -> None:
        """如果已過期，自動更新狀態"""
        if self.status == VoucherStatus.UNUSED and self.is_expired():
            self.status = VoucherStatus.EXPIRED
            self.is_available = False
    
    def to_dict(self) -> dict:
        """
        轉換為字典格式
        用於 API 回應
        """
        return {
            'id': self.id,
            'name': self.name,
            'price': float(self.price),
            'discount_percentage': float(self.discount_percentage),
            'expiry_date': self.expiry_date.isoformat() + 'Z',
            'is_available': self.is_available,
            'status': self.status.value,
            'created_at': self.created_at.isoformat() + 'Z',
            'updated_at': self.updated_at.isoformat() + 'Z',
            'used_at': self.used_at.isoformat() + 'Z' if self.used_at else None
        }

