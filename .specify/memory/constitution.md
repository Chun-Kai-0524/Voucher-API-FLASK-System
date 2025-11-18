# Voucher API System Constitution

## Core Principles

### I. API-First Design
API 合約優先設計：
- 使用 API-FLASK 框架及其建議的最佳實踐
- 所有 API 必須包含 Schema 驗證（使用 marshmallow/pydantic）
- 遵循 RESTful 設計原則，正確使用 HTTP methods (GET/POST/PATCH/PUT/DELETE)
- API 文檔自動生成（OpenAPI/Swagger）

**理由**: API-FLASK 框架本身強調 API 優先，需確保 API 設計的一致性和可維護性

### II. Layered Architecture (分層架構)
專案必須採用清晰的分層架構：
- **API Layer**: 路由、請求/響應處理
- **Service Layer**: 業務邏輯
- **Repository Layer**: 資料存取
- **Model Layer**: 資料模型（SQLAlchemy）
- 每層職責明確，避免跨層直接調用

**理由**: 符合面試要求「可靠且高可用的專案架構分層」，提高程式碼可測試性和可維護性

### III. Test-Driven Development (TDD)
測試驅動開發（非強制但強烈建議）：
- 使用 pytest 撰寫單元測試（加分項）
- 測試覆蓋率目標 > 80%
- 關鍵業務邏輯必須有測試
- 測試與實作程式碼同步提交

**理由**: 加分項明確要求 pytest unittest，TDD 確保程式碼品質

### IV. Performance & Scalability (效能與擴展性)
考慮大量資料處理場景：
- 實作 asyncio 或多執行緒處理大量創建/修改（加分項）
- 注意並發競爭問題（race condition）
- 資料庫查詢優化（避免 N+1 問題）
- 批次操作應考慮效能影響

**理由**: 加分項要求處理百萬級別資料的效能優化

### V. Code Quality & Readability (程式碼品質)
高可讀性與良好的設計模式：
- 遵循 PEP 8 風格指南
- 使用有意義的變數和函數命名
- 適當使用設計模式（Repository、Service Pattern 等）
- 必須至少使用一次 *args 或 **kwargs（面試要求）
- 程式碼註解與 docstring

**理由**: 面試明確要求「合理的設計模式與高可讀的 coding style」

## Development Workflow

### Git Commit Standards
- Commit 以最小或獨立的顆粒度拆分（面試要求）
- Commit message 格式：`<type>: <description>`
  - Types: feat, fix, refactor, test, docs, style, chore
- 範例: `feat: add voucher creation API`

### Code Review Gates
- 所有功能開發需經過自我審查
- 確保符合分層架構原則
- 測試通過才能合併

## Technical Constraints

### Technology Stack
- **Python Version**: 3.11.x
- **Web Framework**: API-FLASK (https://apiflask.com/)
- **ORM**: SQLAlchemy 2.0 語法
- **Testing**: pytest
- **Database**: PostgreSQL / SQLite (開發)
- **Async**: asyncio (加分項)

### Deployment Requirements
- 提供 Docker 支援（優先）
- 或提供 SQL 建表腳本與測試資料
- README.md 必須包含啟動說明

## Domain Requirements

### Voucher Entity
優惠券必須包含以下欄位：
- 唯一編號 (UUID/Auto-increment)
- 優惠券名稱
- 價格 (Decimal)
- 折扣百分比 (0-100)
- 有效期 (datetime)
- 是否可用 (boolean)
- 狀態 (enum: 已使用/未使用/過期)

### Business Rules
- 刪除優惠券必須包含必要檢核
- 過期優惠券狀態自動更新
- 查詢支援多欄位條件篩選
- 批次操作需考慮交易一致性

## Governance

### Amendment Process
本憲章如需修改，需記錄變更原因和影響範圍

### Compliance Review
所有 PR 必須驗證：
1. 是否符合分層架構
2. 是否包含必要測試
3. API Schema 驗證是否完整
4. Commit message 是否清晰

**Version**: 1.0.0 | **Ratified**: 2025-11-14 | **Last Amended**: 2025-11-14
