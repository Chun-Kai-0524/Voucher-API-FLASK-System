"""
Base Model Configuration
SQLAlchemy 基礎配置
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    所有模型的基礎類別
    使用 SQLAlchemy 2.0 的 DeclarativeBase
    """
    pass

