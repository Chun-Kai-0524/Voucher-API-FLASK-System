"""
Voucher API Tests
優惠券 API 測試
"""
import json
from datetime import datetime, timedelta


def test_health_check(client):
    """測試健康檢查端點"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'


def test_create_voucher(client):
    """測試創建優惠券"""
    expiry_date = (datetime.utcnow() + timedelta(days=30)).isoformat() + 'Z'
    
    payload = {
        'name': '測試優惠券',
        'price': 100.00,
        'discount_percentage': 20.00,
        'expiry_date': expiry_date
    }
    
    response = client.post(
        '/api/v1/vouchers/',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == '測試優惠券'
    assert data['status'] == 'unused'


def test_list_vouchers(client):
    """測試查詢優惠券列表"""
    response = client.get('/api/v1/vouchers/')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'data' in data
    assert 'pagination' in data


def test_get_voucher_not_found(client):
    """測試查詢不存在的優惠券"""
    response = client.get('/api/v1/vouchers/99999')
    
    assert response.status_code == 404


def test_create_voucher_validation_error(client):
    """測試創建優惠券驗證錯誤"""
    payload = {
        'name': '測試優惠券'
        # 缺少必填欄位
    }
    
    response = client.post(
        '/api/v1/vouchers/',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 400

