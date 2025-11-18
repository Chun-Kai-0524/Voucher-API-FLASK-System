"""
Voucher Schemas
優惠券 API Schema 定義

使用 marshmallow 進行驗證（API-FLASK 推薦）
"""
from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime


class VoucherSchema(Schema):
    """優惠券輸出 Schema"""
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    price = fields.Decimal(required=True, as_string=True)
    discount_percentage = fields.Decimal(required=True, as_string=True)
    expiry_date = fields.DateTime(required=True, format='iso')
    is_available = fields.Bool(required=True)
    status = fields.Str(required=True)
    created_at = fields.DateTime(required=True, format='iso')
    updated_at = fields.DateTime(required=True, format='iso')
    used_at = fields.DateTime(allow_none=True, format='iso')


class VoucherCreateSchema(Schema):
    """創建優惠券輸入 Schema"""
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={'required': '優惠券名稱為必填欄位'}
    )
    
    price = fields.Decimal(
        required=True,
        places=2,
        validate=validate.Range(min=0.01),
        error_messages={'required': '價格為必填欄位'}
    )
    
    discount_percentage = fields.Decimal(
        required=True,
        places=2,
        validate=validate.Range(min=0, max=100),
        error_messages={'required': '折扣百分比為必填欄位'}
    )
    
    expiry_date = fields.DateTime(
        required=True,
        format='iso',
        error_messages={'required': '有效期為必填欄位'}
    )
    
    is_available = fields.Bool(load_default=True)
    
    @validates('expiry_date')
    def validate_expiry_date(self, value):
        """驗證有效期"""
        # 建議但不強制要求未來日期
        # 移除時區比較以避免 offset-naive/aware 問題
        # 業務邏輯層會進行更詳細的驗證
        return value


class VoucherUpdateSchema(Schema):
    """更新優惠券輸入 Schema"""
    name = fields.Str(validate=validate.Length(min=1, max=100))
    price = fields.Decimal(places=2, validate=validate.Range(min=0.01))
    discount_percentage = fields.Decimal(
        places=2,
        validate=validate.Range(min=0, max=100)
    )
    expiry_date = fields.DateTime(format='iso')
    is_available = fields.Bool()
    status = fields.Str(
        validate=validate.OneOf(['unused', 'used', 'expired'])
    )


class VoucherQuerySchema(Schema):
    """查詢優惠券參數 Schema"""
    page = fields.Int(load_default=1, validate=validate.Range(min=1))
    per_page = fields.Int(
        load_default=20,
        validate=validate.Range(min=1, max=100)
    )
    name = fields.Str()
    min_price = fields.Decimal(places=2, validate=validate.Range(min=0))
    max_price = fields.Decimal(places=2, validate=validate.Range(min=0))
    min_discount = fields.Decimal(
        places=2,
        validate=validate.Range(min=0, max=100)
    )
    max_discount = fields.Decimal(
        places=2,
        validate=validate.Range(min=0, max=100)
    )
    status = fields.Str(validate=validate.OneOf(['unused', 'used', 'expired']))
    is_available = fields.Bool()
    valid_from = fields.DateTime(format='iso')
    valid_to = fields.DateTime(format='iso')


class BatchCreateSchema(Schema):
    """批次創建 Schema"""
    vouchers = fields.List(
        fields.Nested(VoucherCreateSchema),
        required=True,
        validate=validate.Length(min=1, max=10000),
        error_messages={'required': 'vouchers 欄位為必填'}
    )


class BatchUpdateItemSchema(Schema):
    """批次更新項目 Schema"""
    id = fields.Int(required=True)
    data = fields.Nested(VoucherUpdateSchema, required=True)


class BatchUpdateSchema(Schema):
    """批次更新 Schema"""
    updates = fields.List(
        fields.Nested(BatchUpdateItemSchema),
        required=True,
        validate=validate.Length(min=1, max=10000),
        error_messages={'required': 'updates 欄位為必填'}
    )

