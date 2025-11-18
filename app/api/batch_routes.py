"""
Batch API Routes
批次操作 API 路由（加分項）
"""
import asyncio
from apiflask import APIBlueprint

from app.database import get_db
from app.services.batch_service import BatchService
from app.schemas.voucher_schema import BatchCreateSchema, BatchUpdateSchema

# 建立藍圖
bp = APIBlueprint('batch', __name__, url_prefix='/api/v1/vouchers')


@bp.post('/batch')
@bp.input(BatchCreateSchema)
@bp.output(
    {
        'success_count': {'type': 'integer'},
        'failure_count': {'type': 'integer'},
        'total': {'type': 'integer'},
        'failures': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'index': {'type': 'integer'},
                    'error': {'type': 'string'},
                    'data': {'type': 'object'}
                }
            }
        }
    },
    status_code=201,
    description='批次創建結果'
)
@bp.doc(
    summary='批次創建優惠券',
    description='批次創建多張優惠券（支援大量資料，使用 asyncio）',
    tags=['batch']
)
def batch_create(json_data):
    """批次創建優惠券"""
    db = next(get_db())
    service = BatchService(db)
    
    vouchers_data = json_data['vouchers']
    
    # 使用 asyncio 執行批次操作
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        result = loop.run_until_complete(
            service.batch_create_vouchers(vouchers_data)
        )
        return result, 201
    except ValueError as e:
        return {'message': str(e)}, 400
    finally:
        loop.close()


@bp.patch('/batch/update')
@bp.input(BatchUpdateSchema)
@bp.output(
    {
        'success_count': {'type': 'integer'},
        'failure_count': {'type': 'integer'},
        'total': {'type': 'integer'},
        'failures': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'error': {'type': 'string'}
                }
            }
        }
    },
    status_code=200,
    description='批次修改結果'
)
@bp.doc(
    summary='批次修改優惠券',
    description='批次修改多張優惠券（使用 asyncio）',
    tags=['batch']
)
def batch_update(json_data):
    """批次修改優惠券"""
    db = next(get_db())
    service = BatchService(db)
    
    updates = json_data['updates']
    
    # 使用 asyncio 執行批次操作
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        result = loop.run_until_complete(
            service.batch_update_vouchers(updates)
        )
        return result, 200
    except ValueError as e:
        return {'message': str(e)}, 400
    finally:
        loop.close()

