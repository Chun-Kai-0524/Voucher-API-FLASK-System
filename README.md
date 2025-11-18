# Voucher Management API 優惠券管理系統

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![API-FLASK](https://img.shields.io/badge/Framework-API--FLASK-green.svg)](https://apiflask.com/)
[![SQLAlchemy 2.0](https://img.shields.io/badge/ORM-SQLAlchemy%202.0-red.svg)](https://www.sqlalchemy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

完整的優惠券管理系統 RESTful API，使用現代 Python 技術棧開發。

## ✨ 特點

- 🚀 **現代技術棧**: Python 3.11 + API-FLASK + SQLAlchemy 2.0
- 📝 **完整 CRUD**: 優惠券的創建、查詢、修改、刪除
- 🔍 **高級查詢**: 支援多條件篩選和分頁
- ⚡ **批次操作**: 使用 asyncio 處理大量資料（百萬級別）
- 🧪 **測試覆蓋**: pytest 單元測試，覆蓋率 > 80%
- 🐳 **容器化**: Docker 和 Docker Compose 支援
- 📚 **自動文檔**: OpenAPI/Swagger 自動生成
- 🏗️ **分層架構**: API/Service/Repository/Model 清晰分層

## 📋 需求

- Python 3.11+
- PostgreSQL 15+ 或 SQLite 3.35+ (開發)
- Docker 20.10+ (可選，推薦)

## 🚀 快速開始

### 使用 Docker（推薦）

```bash
# 1. Clone 專案
git clone https://github.com/your-username/voucher_test.git
cd voucher_test

# 2. 啟動服務
docker-compose up -d

# 3. 訪問 API
# API: http://localhost:5000/api/v1
# 文檔: http://localhost:5000/docs
```

### 本地開發

```bash
# 1. 建立虛擬環境
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 設定環境變數
cp .env.example .env
# 編輯 .env 檔案設定資料庫等配置

# 4. 初始化資料庫
python scripts/init_db.py

# 5. 啟動應用
flask run
# 或使用: python app/main.py
```

## 📖 API 文檔

啟動後訪問：
- Swagger UI: http://localhost:5000/docs
- ReDoc: http://localhost:5000/redoc
- OpenAPI JSON: http://localhost:5000/openapi.json

## 🔌 API 端點

| Method | Endpoint | 描述 |
|--------|----------|------|
| `GET` | `/api/v1/vouchers` | 查詢優惠券列表 |
| `POST` | `/api/v1/vouchers` | 創建優惠券 |
| `GET` | `/api/v1/vouchers/{id}` | 查詢單一優惠券 |
| `PATCH` | `/api/v1/vouchers/{id}` | 修改優惠券 |
| `DELETE` | `/api/v1/vouchers/{id}` | 刪除優惠券 |
| `POST` | `/api/v1/vouchers/batch` | 批次創建 |
| `PATCH` | `/api/v1/vouchers/batch/update` | 批次修改 |

### 範例請求

#### 創建優惠券

```bash
curl -X POST http://localhost:5000/api/v1/vouchers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "新用戶優惠券",
    "price": 100.00,
    "discount_percentage": 20.00,
    "expiry_date": "2025-12-31T23:59:59Z"
  }'
```

#### 查詢優惠券（篩選）

```bash
curl "http://localhost:5000/api/v1/vouchers?status=unused&min_discount=15&page=1&per_page=20"
```

#### 批次創建

```bash
curl -X POST http://localhost:5000/api/v1/vouchers/batch \
  -H "Content-Type: application/json" \
  -d '{
    "vouchers": [
      {"name": "券1", "price": 100, "discount_percentage": 10, "expiry_date": "2025-12-31T23:59:59Z"},
      {"name": "券2", "price": 200, "discount_percentage": 20, "expiry_date": "2025-12-31T23:59:59Z"}
    ]
  }'
```

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

# 顯示覆蓋率
pytest --cov=app --cov-report=html

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
refactor: 重構
style: 程式碼格式
chore: 建置/工具相關
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

本專案使用 SQLAlchemy 2.0 的現代語法：

```python
from sqlalchemy.orm import Mapped, mapped_column

class Voucher(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    # ...
```

### 批次操作 (Asyncio)

使用 asyncio 提升大量資料處理效能：

```python
async def batch_create_vouchers(vouchers_data):
    # 並行處理邏輯
    results = await asyncio.gather(*tasks)
```

### 分層架構

- **API Layer**: 處理 HTTP 請求/響應
- **Service Layer**: 業務邏輯和驗證
- **Repository Layer**: 資料庫操作
- **Model Layer**: SQLAlchemy 模型

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

## 🐛 故障排除

### 資料庫連接失敗

檢查 `DATABASE_URL` 配置和資料庫服務狀態。

### 模組導入錯誤

確保虛擬環境已啟動：

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Docker 啟動失敗

```bash
docker-compose logs
docker-compose down
docker-compose up --build
```

## 📚 相關文檔

- [API-FLASK 官方文檔](https://apiflask.com/)
- [SQLAlchemy 2.0 文檔](https://docs.sqlalchemy.org/en/20/)
- [功能規格](specs/001-voucher-api-system/spec.md)
- [資料模型設計](specs/001-voucher-api-system/data-model.md)
- [API 合約](specs/001-voucher-api-system/contracts/openapi.yaml)

## 📄 授權

MIT License

## 👤 作者

面試作業專案 - Voucher Management API

---

**Built with ❤️ using Python 3.11, API-FLASK & SQLAlchemy 2.0**

