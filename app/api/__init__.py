"""
API Routes
API 路由層
"""
from app.api.voucher_routes import bp as voucher_bp
from app.api.batch_routes import bp as batch_bp

def register_blueprints(app):
    """註冊所有藍圖"""
    app.register_blueprint(voucher_bp)
    app.register_blueprint(batch_bp)

