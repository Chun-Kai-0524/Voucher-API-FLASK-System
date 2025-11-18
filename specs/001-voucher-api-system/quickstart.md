# Quick Start Guide: Voucher Management API

## 系統需求

- **Python**: 3.11.x
- **資料庫**: PostgreSQL 15+ 或 SQLite 3.35+（開發環境）
- **Docker**: 20.10+ (選用，推薦使用)
- **Git**: 2.30+

## 快速啟動（Docker 方式 - 推薦）

### 1. Clone 專案

```bash
git clone https://github.com/[your-username]/voucher_test.git
cd voucher_test
```

### 2. 使用 Docker Compose 啟動

```bash
docker-compose up -d
```

### 3. 訪問 API

- **API 基礎 URL**: http://localhost:5000/api/v1
- **API 文檔**: http://localhost:5000/docs (Swagger UI)
- **健康檢查**: http://localhost:5000/health

### 4. 測試 API

```bash
# 創建優惠券
curl -X POST http://localhost:5000/api/v1/vouchers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "測試優惠券",
    "price": 100.00,
    "discount_percentage": 20.00,
    "expiry_date": "2025-12-31T23:59:59Z"
  }'

# 查詢優惠券列表
curl http://localhost:5000/api/v1/vouchers
```

---

## 本地開發啟動（無 Docker）

### 1. 環境設定

```bash
# 建立虛擬環境
python3.11 -m venv venv

# 啟動虛擬環境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt
```

### 2. 配置環境變數

建立 `.env` 檔案：

```bash
# 資料庫設定
DATABASE_URL=sqlite:///voucher.db
# 或使用 PostgreSQL
# DATABASE_URL=postgresql://user:password@localhost:5432/voucher_db

# 應用程式設定
FLASK_APP=app.main:app
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-in-production

# API 設定
API_HOST=0.0.0.0
API_PORT=5000
```

### 3. 初始化資料庫

```bash
# 使用 SQLite（開發環境）
python scripts/init_db.py

# 或執行 SQL 腳本
sqlite3 voucher.db < database/init.sql
```

**PostgreSQL 使用者：**

```bash
# 建立資料庫
createdb voucher_db

# 執行初始化腳本
psql -d voucher_db -f database/init.sql
```

### 4. 啟動應用程式

```bash
# 使用 Flask 開發伺服器
flask run

# 或使用 gunicorn (生產環境)
gunicorn -w 4 -b 0.0.0.0:5000 app.main:app
```

### 5. 執行測試

```bash
# 執行所有測試
pytest

# 執行測試並顯示覆蓋率
pytest --cov=app --cov-report=html

# 執行特定測試
pytest tests/test_voucher_api.py
```

---

## 專案結構

```
voucher_test/
├── app/                          # 應用程式主目錄
│   ├── __init__.py              # Flask 應用初始化
│   ├── main.py                  # 應用程式入口
│   ├── config.py                # 配置管理
│   ├── models/                  # SQLAlchemy 模型
│   │   ├── __init__.py
│   │   └── voucher.py           # Voucher 模型
│   ├── repositories/            # 資料存取層
│   │   ├── __init__.py
│   │   └── voucher_repository.py
│   ├── services/                # 業務邏輯層
│   │   ├── __init__.py
│   │   ├── voucher_service.py
│   │   └── batch_service.py     # 批次操作服務
│   ├── api/                     # API 路由
│   │   ├── __init__.py
│   │   ├── voucher_routes.py
│   │   └── batch_routes.py      # 批次操作路由
│   └── schemas/                 # API-FLASK Schemas
│       ├── __init__.py
│       └── voucher_schema.py
├── tests/                       # 測試目錄
│   ├── __init__.py
│   ├── conftest.py             # pytest 配置
│   ├── test_models.py
│   ├── test_repositories.py
│   ├── test_services.py
│   ├── test_voucher_api.py
│   └── test_batch_api.py
├── database/                    # 資料庫腳本
│   ├── init.sql                # 初始化腳本
│   └── seed.sql                # 測試數據
├── scripts/                     # 工具腳本
│   └── init_db.py              # 資料庫初始化
├── specs/                       # 設計文檔
│   └── 001-voucher-api-system/
├── docker-compose.yml           # Docker Compose 配置
├── Dockerfile                   # Docker 映像配置
├── requirements.txt             # Python 依賴
├── pytest.ini                   # pytest 配置
├── .env.example                 # 環境變數範例
├── .gitignore                   # Git 忽略檔案
└── README.md                    # 專案說明
```

---

## 依賴套件

主要依賴（見 `requirements.txt`）：

```txt
# Web Framework
apiflask==2.1.0
Flask==3.0.0

# Database
SQLAlchemy==2.0.23
psycopg2-binary==2.9.9  # PostgreSQL
alembic==1.13.1          # Database migrations

# Validation
marshmallow==3.20.1

# Testing
pytest==7.4.3
pytest-cov==4.1.0
pytest-asyncio==0.21.1

# Async Support
aiohttp==3.9.1

# Utilities
python-dotenv==1.0.0
gunicorn==21.2.0
```

---

## API 端點總覽

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/vouchers` | 查詢優惠券列表（支援篩選和分頁） |
| POST | `/api/v1/vouchers` | 創建單一優惠券 |
| GET | `/api/v1/vouchers/{id}` | 查詢單一優惠券 |
| PATCH | `/api/v1/vouchers/{id}` | 修改優惠券（部分更新） |
| DELETE | `/api/v1/vouchers/{id}` | 刪除優惠券 |
| POST | `/api/v1/vouchers/batch` | 批次創建優惠券 |
| PATCH | `/api/v1/vouchers/batch/update` | 批次修改優惠券 |

完整 API 文檔請參考：[OpenAPI 規格](./contracts/openapi.yaml)

---

## 常見問題

### Q1: 如何切換資料庫？

修改 `.env` 檔案中的 `DATABASE_URL`：

```bash
# SQLite (開發)
DATABASE_URL=sqlite:///voucher.db

# PostgreSQL (生產)
DATABASE_URL=postgresql://user:password@localhost:5432/voucher_db
```

### Q2: 如何執行批次操作？

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

### Q3: 如何查看測試覆蓋率？

```bash
pytest --cov=app --cov-report=html
# 然後開啟 htmlcov/index.html
```

### Q4: 如何停止 Docker 容器？

```bash
docker-compose down
```

---

## 開發工作流程

### 1. 建立新功能分支

```bash
git checkout -b feature/your-feature-name
```

### 2. 開發並測試

```bash
# 開發程式碼
# ...

# 執行測試
pytest

# 檢查程式碼風格
flake8 app/
black app/
```

### 3. Commit 並推送

```bash
git add .
git commit -m "feat: add your feature description"
git push origin feature/your-feature-name
```

---

## 效能測試（加分項）

使用 locust 進行負載測試：

```bash
# 安裝 locust
pip install locust

# 執行負載測試
locust -f tests/load_test.py --host=http://localhost:5000
```

---

## 進階配置

### 啟用 CORS

修改 `app/main.py`：

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
```

### 啟用 API 限流

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route("/api/v1/vouchers")
@limiter.limit("100/hour")
def list_vouchers():
    # ...
```

---

## 故障排除

### 資料庫連接失敗

檢查 `DATABASE_URL` 是否正確，資料庫服務是否啟動。

### 模組導入錯誤

確認虛擬環境已啟動，依賴已安裝：

```bash
pip list
pip install -r requirements.txt
```

### Docker 啟動失敗

檢查 Docker 服務是否運行：

```bash
docker ps
docker-compose logs
```

---

## 相關資源

- [API-FLASK 官方文檔](https://apiflask.com/)
- [SQLAlchemy 2.0 文檔](https://docs.sqlalchemy.org/en/20/)
- [pytest 文檔](https://docs.pytest.org/)
- [OpenAPI 規範](./contracts/openapi.yaml)
- [資料模型設計](./data-model.md)

---

## 支援與聯繫

如有問題，請提交 Issue 或聯繫開發團隊。

