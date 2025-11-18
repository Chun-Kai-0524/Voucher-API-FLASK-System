"""
Voucher API Routes
優惠券 API 路由

使用 API-FLASK 框架
"""
from apiflask import APIBlueprint
from flask import request

from app.database import get_db
from app.services.voucher_service import VoucherService
from app.schemas.voucher_schema import (
    VoucherSchema,
    VoucherCreateSchema,
    VoucherUpdateSchema,
    VoucherQuerySchema
)

# 建立藍圖
bp = APIBlueprint('vouchers', __name__, url_prefix='/api/v1/vouchers')


@bp.get('/')
@bp.input(VoucherQuerySchema, location='query')
@bp.output(
    {
        'data': {'type': 'array', 'items': VoucherSchema},
        'pagination': {
            'type': 'object',
            'properties': {
                'page': {'type': 'integer'},
                'per_page': {'type': 'integer'},
                'total': {'type': 'integer'},
                'pages': {'type': 'integer'}
            }
        }
    },
    status_code=200,
    description='優惠券列表'
)
@bp.doc(
    summary='查詢優惠券列表',
    description='查詢所有優惠券，支援多條件篩選和分頁',
    tags=['vouchers']
)
def list_vouchers(query_data):
    """查詢優惠券列表"""
    db = next(get_db())
    service = VoucherService(db)
    
    # 提取分頁參數
    page = query_data.pop('page', 1)
    per_page = query_data.pop('per_page', 20)
    
    # 其餘為篩選條件
    filters = query_data if query_data else None
    
    # 查詢
    vouchers, total, pages = service.list_vouchers(page, per_page, filters)
    
    return {
        'data': [v.to_dict() for v in vouchers],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': pages
        }
    }


@bp.post('/')
@bp.input(VoucherCreateSchema)
@bp.doc(
    summary='創建優惠券',
    description='創建一張新的優惠券',
    tags=['vouchers']
)
def create_voucher(json_data):
    """創建優惠券"""
    db = next(get_db())
    service = VoucherService(db)
    
    try:
        voucher = service.create_voucher(json_data)
        # 在 session 關閉前轉換為 dict
        result = voucher.to_dict()
        return result, 201
    except ValueError as e:
        return {'message': str(e)}, 400


@bp.get('/<int:voucher_id>')
@bp.doc(
    summary='查詢單一優惠券',
    description='根據 ID 查詢優惠券詳細資訊',
    tags=['vouchers']
)
def get_voucher(voucher_id):
    """查詢單一優惠券"""
    db = next(get_db())
    service = VoucherService(db)
    
    voucher = service.get_voucher(voucher_id)
    
    if not voucher:
        return {'message': f'Voucher with id {voucher_id} not found'}, 404
    
    return voucher.to_dict()


@bp.patch('/<int:voucher_id>')
@bp.input(VoucherUpdateSchema)
@bp.doc(
    summary='修改優惠券',
    description='修改優惠券資訊（部分更新）',
    tags=['vouchers']
)
def update_voucher(voucher_id, json_data):
    """修改優惠券"""
    db = next(get_db())
    service = VoucherService(db)
    
    try:
        voucher = service.update_voucher(voucher_id, json_data)
        return voucher.to_dict()
    except ValueError as e:
        error_msg = str(e)
        if 'not found' in error_msg:
            return {'message': error_msg}, 404
        return {'message': error_msg}, 400


@bp.delete('/<int:voucher_id>')
@bp.output({}, status_code=204, description='優惠券刪除成功')
@bp.doc(
    summary='刪除優惠券',
    description='刪除優惠券（已使用的優惠券不可刪除）',
    tags=['vouchers']
)
def delete_voucher(voucher_id):
    """刪除優惠券"""
    db = next(get_db())
    service = VoucherService(db)
    
    try:
        service.delete_voucher(voucher_id)
        return '', 204
    except ValueError as e:
        error_msg = str(e)
        if 'not found' in error_msg:
            return {'message': error_msg}, 404
        return {'message': error_msg}, 400

