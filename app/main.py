"""
Main Application
主應用程式入口

使用 API-FLASK 框架
"""
from apiflask import APIFlask
from flask_cors import CORS

from app.config import get_config
from app.database import init_db
from app.api import register_blueprints

# 建立應用程式
app = APIFlask(
    __name__,
    title='Voucher Management API',
    version='1.0.0'
)

# 載入配置
config = get_config()
app.config.from_object(config)

# 啟用 CORS
if config.CORS_ENABLED:
    CORS(app, origins=config.CORS_ORIGINS)

# 註冊藍圖
register_blueprints(app)


@app.route('/health')
def health_check():
    """健康檢查端點"""
    return {'status': 'healthy', 'message': 'Voucher API is running'}, 200


@app.before_request
def create_tables():
    """在第一次請求前初始化資料庫"""
    if not hasattr(app, 'db_initialized'):
        init_db()
        app.db_initialized = True


@app.errorhandler(404)
def not_found(error):
    """404 錯誤處理"""
    return {'message': 'Resource not found'}, 404


@app.errorhandler(500)
def internal_error(error):
    """500 錯誤處理"""
    return {'message': 'Internal server error'}, 500


if __name__ == '__main__':
    # 開發模式下直接運行
    app.run(
        host=config.API_HOST,
        port=config.API_PORT,
        debug=config.DEBUG
    )

