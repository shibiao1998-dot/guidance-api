# Guidance API - 企业顶层指导文档管理系统

基于 FastAPI 构建的 RESTful API 服务，为企业顶层指导文档提供完整的存储和管理功能。

## 功能特性

- **材料包管理** - 存储用户上传的原始材料
- **证据卡管理** - 存储从材料中提取的证据片段
- **术语表管理** - 管理企业术语定义
- **方向管理** - 企业顶层指导的一级结构
- **维度管理** - 企业顶层指导的二级结构
- **观点管理** - 企业顶层指导的三级结构
- **审核队列** - 待审核项目队列管理
- **快照管理** - 文档快照存储和发布

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

编辑 `.env` 文件：

```env
DATABASE_URL=sqlite:///./guidance.db
HOST=0.0.0.0
PORT=8000
DEBUG=true
```

### 3. 启动服务

```bash
# 方式一：使用 uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 方式二：直接运行
python main.py
```

### 4. 访问 API 文档

服务启动后访问：
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **健康检查:** http://localhost:8000/health

## 项目结构

```
guidance-api/
├── main.py                 # FastAPI 主入口
├── database.py             # 数据库配置
├── models.py               # SQLAlchemy 数据模型
├── schemas.py              # Pydantic 验证 Schema
├── requirements.txt        # Python 依赖
├── .env                    # 环境变量配置
├── DIFY_HTTP_CONFIG.md     # Dify HTTP Request 节点配置指南
├── README.md               # 本文件
└── endpoints/              # API 端点模块
    ├── __init__.py
    ├── bundles.py          # 材料包端点
    ├── evidence_cards.py   # 证据卡端点
    ├── glossary.py         # 术语表端点
    ├── directions.py       # 方向端点
    ├── dimensions.py       # 维度端点
    ├── opinions.py         # 观点端点
    ├── review_queue.py     # 审核队列端点
    ├── snapshots.py        # 快照端点
    └── publish.py          # 发布端点
```

## API 端点一览

| 端点 | 方法 | 描述 |
|------|------|------|
| `/bundles` | POST | 创建材料包 |
| `/bundles/{id}` | GET | 获取材料包 |
| `/bundles/{id}` | PUT | 更新材料包 |
| `/bundles/{id}` | DELETE | 删除材料包 |
| `/evidence-cards` | POST | 创建证据卡 |
| `/evidence-cards` | GET | 查询证据卡（支持按 bundle_id 筛选） |
| `/glossary` | POST | 创建/更新术语 |
| `/glossary/version/{version}` | GET | 获取指定版本的术语表 |
| `/directions` | POST | 创建方向 |
| `/directions` | GET | 获取方向列表 |
| `/dimensions` | POST | 创建维度 |
| `/dimensions/direction/{direction_id}` | GET | 按方向获取维度 |
| `/opinions` | POST | 创建观点 |
| `/opinions/dimension/{dimension_id}` | GET | 按维度获取观点 |
| `/review-queue` | POST | 创建审核项 |
| `/review-queue` | GET | 获取待审核项 |
| `/review-queue/{id}` | PATCH | 更新审核状态 |
| `/snapshots` | POST | 创建快照 |
| `/snapshots/published/latest` | GET | 获取最新已发布快照 |
| `/snapshots/{id}/publish` | POST | 发布快照 |
| `/publish` | POST | 触发发布操作 |

## 数据模型关系

```
Bundle (材料包)
  └── EvidenceCard (证据卡) × N

Direction (方向)
  └── Dimension (维度) × N
        └── Opinion (观点) × N

GlossaryTerm (术语表)

ReviewQueue (审核队列)

Snapshot (快照)
  └── PublishLog (发布日志) × N
```

## 与 Dify 集成

详见 [`DIFY_HTTP_CONFIG.md`](./DIFY_HTTP_CONFIG.md) 文档，包含所有 HTTP Request 节点的完整配置。

### 快速配置步骤

1. 在 Dify Chatflow 中添加 HTTP Request 节点
2. 配置 Base URL 为 `http://localhost:8000` (或你的部署地址)
3. 按照 `DIFY_HTTP_CONFIG.md` 中的配置填写每个端点
4. 测试连接

## 部署建议

### 本地开发

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 生产环境

1. 使用 PostgreSQL 替代 SQLite
2. 配置反向代理（Nginx/Traefik）
3. 启用 HTTPS
4. 设置合适的 CORS 策略

修改 `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/guidance_db
DEBUG=false
```

## 技术栈

- **FastAPI** - 现代高性能 Web 框架
- **SQLAlchemy** - ORM 框架
- **Pydantic** - 数据验证
- **SQLite** - 默认数据库（支持 PostgreSQL）
- **Uvicorn** - ASGI 服务器

## 开发说明

### 添加新端点

1. 在 `endpoints/` 目录下创建新文件
2. 导入并注册到 `main.py`
3. 更新 `DIFY_HTTP_CONFIG.md` 文档

### 数据库迁移

目前使用 SQLAlchemy 的 `Base.metadata.create_all()` 自动创建表。生产环境建议使用 Alembic 进行迁移管理。

## 许可证

MIT License
