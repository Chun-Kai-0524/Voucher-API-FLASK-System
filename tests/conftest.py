"""
Pytest Configuration
測試配置
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app as flask_app
from app.models.base import Base
from app.database import get_db


@pytest.fixture
def app():
    """Flask 應用fixture"""
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    yield flask_app


@pytest.fixture
def client(app):
    """測試客戶端"""
    return app.test_client()


@pytest.fixture
def db_session():
    """資料庫 session fixture"""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def sample_voucher_data():
    """範例優惠券資料"""
    from datetime import datetime, timedelta
    from decimal import Decimal
    
    return {
        'name': '測試優惠券',
        'price': Decimal('100.00'),
        'discount_percentage': Decimal('20.00'),
        'expiry_date': datetime.utcnow() + timedelta(days=30)
    }

