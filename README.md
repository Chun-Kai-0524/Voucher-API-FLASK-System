# Voucher API System

優惠券管理系統 RESTful API - Python 3.11 + API-FLASK + SQLAlchemy 2.0 + PostgreSQL

## 📋 API 功能

### CRUD 操作
- **創建優惠券** - `POST /api/v1/vouchers/`
- **查詢單一優惠券** - `GET /api/v1/vouchers/{id}`
- **查詢優惠券列表** - `GET /api/v1/vouchers/`（支援多條件篩選與分頁）
- **修改優惠券** - `PATCH /api/v1/vouchers/{id}`
- **刪除優惠券** - `DELETE /api/v1/vouchers/{id}`

### 批次操作
- **批次創建** - `POST /api/v1/batch/create`
- **批次修改** - `PATCH /api/v1/batch/update`

### 查詢篩選
支援名稱、狀態、價格區間、折扣區間、有效期、分頁等條件篩選

### 其他
- Swagger UI 互動式文檔（`/docs`）
- 狀態自動管理（unused/used/expired）
- 異步批次處理（asyncio）

## 🛠️ 技術棧

| 技術 | 版本 |
|------|------|
| Python | 3.11 |
| API-FLASK | 2.1.0 |
| SQLAlchemy | 2.0.23 |
| PostgreSQL | 15-alpine |
| Marshmallow | 3.20.1 |
| Gunicorn | 21.2.0 |
| Pytest | 7.4.3 |
| Docker Compose | Latest |

## 🚀 如何啟動

### 使用 Docker（推薦）

**無需安裝 Python 虛擬環境，一鍵啟動**

```bash
# 1. Clone 專案
git clone https://github.com/Chun-Kai-0524/Voucher-API-FLASK-System.git
cd Voucher-API-FLASK-System

# 2. 啟動 Docker Desktop

# 3. 啟動服務
docker-compose up -d

# 4. 訪問 API
# Swagger UI: http://localhost:5000/docs
# API 端點: http://localhost:5000/api/v1/vouchers/
```

### 本地開發（需要虛擬環境）

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

## 🧪 測試

```bash
# Docker 環境測試
docker-compose up -d
# 訪問 http://localhost:5000/docs 進行 API 測試

# 本地環境測試
pytest
pytest --cov=app  # 顯示覆蓋率
```

## 📖 API 文檔

- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc
- **Health Check**: http://localhost:5000/health

## 📂 專案結構

```
├── app/                  # 應用程式
│   ├── models/          # SQLAlchemy 2.0 模型
│   ├── repositories/    # 資料存取層
│   ├── services/        # 業務邏輯層
│   ├── api/             # API 路由
│   └── schemas/         # Marshmallow Schema
├── tests/               # 測試
├── database/            # 資料庫腳本
├── docker-compose.yml   # Docker 配置
└── requirements.txt     # Python 依賴
```

## 📝 範例請求

```bash
# 創建優惠券
curl -X POST http://localhost:5000/api/v1/vouchers/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "測試優惠券",
    "price": 100,
    "discount_percentage": 20,
    "expiry_date": "2025-12-31T23:59:00"
  }'

# 查詢列表（篩選）
curl "http://localhost:5000/api/v1/vouchers/?status=unused&min_discount=15"
```

## 🏗️ 架構設計

- **分層架構**: API → Service → Repository → Model
- **SQLAlchemy 2.0**: 使用現代型別提示語法
- **異步處理**: 批次操作使用 asyncio
- **Docker 部署**: 包含 PostgreSQL 資料庫

---

**Built with Python 3.11, API-FLASK & SQLAlchemy 2.0**
