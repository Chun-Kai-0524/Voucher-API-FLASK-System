# Voucher Management API 優惠券管理系統

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![API-FLASK](https://img.shields.io/badge/Framework-API--FLASK-green.svg)](https://apiflask.com/)
[![SQLAlchemy 2.0](https://img.shields.io/badge/ORM-SQLAlchemy%202.0-red.svg)](https://www.sqlalchemy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

優惠券管理系統 RESTful API

## ✨ 特點

- 🚀 **技術**: Python 3.11 + API-FLASK + SQLAlchemy 2.0 + Docker Compose🐳 + OpenAPI/Swagger
- ⚡ **API**: 優惠券的CRUD/支援多條件篩選和分頁/批次操作(asyncio)
- 🧪 **測試**: pytest 單元測試，覆蓋率 > 80%
- 🏗️ **架構分層**: API/Service/Repository/Model

## 🚀 快速開始

### 使用 Docker

```bash
# 1. Clone 專案
git clone https://github.com/Chun-Kai-0524/Voucher-API-FLASK-System.git
cd Voucher-API-FLASK-System

# 2. 啟動服務
docker-compose up -d

# 3. API Swagger
# 文檔: http://localhost:5000/docs
```

### 本地 Venv

```bash
# 1. 建立虛擬環境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 初始化資料庫
python scripts/init_db.py

# 4. 啟動服務
python app/main.py

# 訪問: http://localhost:5000/docs
```

## 📖 API 文檔

啟動後訪問：

- Swagger UI: http://localhost:5000/docs
- ReDoc: http://localhost:5000/redoc
- OpenAPI JSON: http://localhost:5000/openapi.json

## 🔌 API 端點

| Method | Endpoint | 描述 |
|--------|----------|------|
| GET | /api/v1/vouchers | 查詢優惠券列表 |
| POST | /api/v1/vouchers | 創建優惠券 |
| GET | /api/v1/vouchers/{id} | 查詢單一優惠券 |
| PATCH | /api/v1/vouchers/{id} | 修改優惠券 |
| DELETE | /api/v1/vouchers/{id} | 刪除優惠券 |
| POST | /api/v1/vouchers/batch | 批次創建 |
| PATCH | /api/v1/vouchers/batch/update | 批次修改 |

## 🏗️ 專案結構

```
voucher_test/
├── app/                      # 應用程式主目錄
│   ├── models/              # SQLAlchemy 2.0 模型
│   ├── repositories/        # 資料存取層
│   ├── services/            # 業務邏輯層
│   ├── api/                 # API 路由層
│   ├── schemas/             # 驗證 Schema
│   ├── config.py            # 配置管理
│   ├── database.py          # 資料庫連接
│   └── main.py              # 應用程式入口
├── tests/                   # 測試目錄
├── database/                # 資料庫腳本
├── scripts/                 # 工具腳本
├── specs/                   # 設計文檔
├── docker-compose.yml       # Docker Compose 配置
├── Dockerfile               # Docker 映像
├── requirements.txt         # Python 依賴
└── README.md               # 本文檔
```

## 🧪 測試

```bash
# 執行所有測試
pytest

# 執行特定測試
pytest tests/test_voucher_api.py
```

## 🔧 開發

### Git Commit 規範

```bash
feat: 新功能
fix: Bug 修復
docs: 文檔更新
test: 測試相關
```

### 程式碼品質

```bash
# 格式化
black app/

# Lint 檢查
flake8 app/

# 型別檢查
mypy app/
```

## 📊 效能

- 單筆查詢: < 100ms (10,000 筆資料)
- 批次創建: 10,000 筆 < 30 秒
- 並發支援: 使用 asyncio 處理並發操作

## 🛠️ 技術細節

### SQLAlchemy 2.0 語法

```python
from sqlalchemy.orm import Mapped, mapped_column

class Voucher(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    # ...
```

### 批次操作 (Asyncio)

```python
async def batch_create_vouchers(vouchers_data):
    # 並行處理邏輯
    results = await asyncio.gather(*tasks)
```

## 📝 資料庫

### Schema

```sql
CREATE TABLE vouchers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    discount_percentage NUMERIC(5, 2) NOT NULL,
    expiry_date TIMESTAMP NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    status VARCHAR(10) DEFAULT 'unused',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    used_at TIMESTAMP NULL
);
```

### 切換資料庫

修改 `.env`:

```bash
# SQLite (開發)
DATABASE_URL=sqlite:///voucher.db

# PostgreSQL (生產)
DATABASE_URL=postgresql://user:pass@localhost:5432/voucher_db
```

## 📚 相關文檔

- [API-FLASK 官方文檔](https://apiflask.com/)
- [SQLAlchemy 2.0 文檔](https://docs.sqlalchemy.org/en/20/)
- [功能規格](specs/001-voucher-api-system/spec.md)
- [資料模型設計](specs/001-voucher-api-system/data-model.md)
- [API 合約](specs/001-voucher-api-system/contracts/openapi.yaml)

## 👤 作者 Aaron Syu
