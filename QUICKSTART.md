# 快速啟動指南

## ✅ 專案已完成並測試通過！

所有功能均已實現並測試成功：
- ✅ SQLAlchemy 2.0 模型層
- ✅ Repository 資料存取層
- ✅ Service 業務邏輯層
- ✅ API-FLASK RESTful API
- ✅ 批次操作 (asyncio)
- ✅ 資料庫初始化
- ✅ Docker 支援
- ✅ 完整測試

---

## 🚀 立即啟動

### 方式 1：本地運行（已配置）

專案已經完成設定，直接啟動即可：

```bash
# 1. 啟動應用（虛擬環境已啟動）
python app/main.py
```

應用將在 http://localhost:5000 啟動

### 方式 2：使用 Flask CLI

```bash
flask run
```

---

## 📝 API 端點測試

### 健康檢查

```bash
curl http://localhost:5000/health
```

### 創建優惠券

```powershell
$body = @{
    name = "測試優惠券"
    price = 100.00
    discount_percentage = 20.00
    expiry_date = "2025-12-31T23:59:59Z"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/v1/vouchers/" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

### 查詢優惠券列表

```bash
curl http://localhost:5000/api/v1/vouchers/
```

### 查詢單一優惠券

```bash
curl http://localhost:5000/api/v1/vouchers/1
```

### 修改優惠券

```powershell
$body = @{
    name = "更新後的名稱"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/v1/vouchers/1" `
    -Method PATCH `
    -Body $body `
    -ContentType "application/json"
```

### 刪除優惠券

```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/v1/vouchers/1" `
    -Method DELETE
```

### 批次創建

```powershell
$body = @{
    vouchers = @(
        @{
            name = "批次券1"
            price = 100.00
            discount_percentage = 10.00
            expiry_date = "2025-12-31T23:59:59Z"
        },
        @{
            name = "批次券2"
            price = 200.00
            discount_percentage = 20.00
            expiry_date = "2025-12-31T23:59:59Z"
        }
    )
} | ConvertTo-Json -Depth 3

Invoke-WebRequest -Uri "http://localhost:5000/api/v1/vouchers/batch" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

---

## 📚 API 文檔

啟動應用後，訪問：

- **Swagger UI**: http://localhost:5000/docs
- **OpenAPI JSON**: http://localhost:5000/openapi.json

---

## 🗄️ 資料庫

當前使用 **SQLite**（`voucher.db`），資料庫已初始化。

如需切換到 PostgreSQL，修改 `.env`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/voucher_db
```

---

## 🐳 Docker 部署

```bash
# 使用 Docker Compose 啟動（包含 PostgreSQL）
docker-compose up -d

# 查看日誌
docker-compose logs -f

# 停止服務
docker-compose down
```

---

## 🧪 執行測試

```bash
# 執行所有測試
pytest

# 顯示覆蓋率
pytest --cov=app --cov-report=html

# 查看覆蓋率報告
start htmlcov/index.html  # Windows
```

---

## 📁 專案結構

```
voucher_test/
├── app/
│   ├── models/          # SQLAlchemy 2.0 模型
│   ├── repositories/    # 資料存取層
│   ├── services/        # 業務邏輯層（含批次操作）
│   ├── api/             # API 路由
│   ├── schemas/         # 驗證 Schema
│   └── main.py          # 應用入口
├── tests/               # 測試
├── database/            # SQL 腳本
├── specs/               # 設計文檔
├── voucher.db           # SQLite 資料庫
├── .env                 # 環境變數
└── README.md            # 完整文檔
```

---

## ✨ 技術亮點

1. **SQLAlchemy 2.0 語法**: 使用最新的 `Mapped` 和 `mapped_column`
2. **分層架構**: API → Service → Repository → Model
3. **批次操作**: 使用 `asyncio` 處理大量資料
4. **完整驗證**: marshmallow Schema 驗證
5. **自動文檔**: OpenAPI/Swagger 自動生成
6. **Docker 支援**: 一鍵部署

---

## 🎯 功能檢查清單

- [x] CRUD API 完整實現
- [x] 查詢篩選和分頁
- [x] 狀態管理（unused/used/expired）
- [x] 批次創建/修改（asyncio）
- [x] 輸入驗證
- [x] 錯誤處理
- [x] 資料庫初始化
- [x] API 文檔
- [x] Docker 配置
- [x] 測試框架
- [x] Git 版本控制

---

## 💡 下一步

1. **啟動應用**: `python app/main.py`
2. **訪問文檔**: http://localhost:5000/docs
3. **測試 API**: 使用上面的範例請求
4. **執行測試**: `pytest`
5. **查看程式碼**: 瀏覽專案結構

---

## 📞 支援

- 完整文檔: `README.md`
- 設計規格: `specs/001-voucher-api-system/`
- API 合約: `specs/001-voucher-api-system/contracts/openapi.yaml`

---

**🎉 專案已完成並可直接使用！**

