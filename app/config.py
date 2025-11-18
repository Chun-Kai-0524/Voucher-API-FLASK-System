"""
Application Configuration
應用程式配置管理
"""
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()


class Config:
    """基礎配置類別"""
    
    # Flask 配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # 資料庫配置
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///voucher.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'False') == 'True'
    
    # API 配置
    API_TITLE = 'Voucher Management API'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.3'
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', '5000'))
    
    # OpenAPI/Swagger 配置
    OPENAPI_JSON_INDENT = 2
    OPENAPI_URL_PREFIX = '/'
    OPENAPI_SWAGGER_UI_PATH = '/docs'
    OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
    OPENAPI_REDOC_PATH = '/redoc'
    OPENAPI_REDOC_URL = 'https://cdn.jsdelivr.net/npm/redoc/bundles/redoc.standalone.js'
    
    # CORS 配置
    CORS_ENABLED = os.getenv('CORS_ENABLED', 'True') == 'True'
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
    
    # 分頁配置
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    
    # 批次操作配置
    BATCH_SIZE_LIMIT = 10000  # 批次操作最大數量
    BATCH_CHUNK_SIZE = 100    # 每次處理的批次大小
    
    # 測試模式
    TESTING = False


class DevelopmentConfig(Config):
    """開發環境配置"""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    """測試環境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """生產環境配置"""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    
    # 生產環境必須使用環境變數設定的 SECRET_KEY
    @property
    def SECRET_KEY(self):
        secret = os.getenv('SECRET_KEY')
        if not secret:
            raise ValueError('SECRET_KEY must be set in production environment')
        return secret


# 配置字典
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config():
    """取得當前配置"""
    env = os.getenv('FLASK_ENV', 'development')
    return config_by_name.get(env, DevelopmentConfig)

