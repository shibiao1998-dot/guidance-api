# Guidance API 完整端点清单

本文档列出 Guidance API 的所有端点，共 **50 个端点**（27 个唯一路径）。

## 端点总览

| 模块 | 端点数量 | 功能说明 |
|------|---------|---------|
| **Bundles** | 5 | 材料包管理 |
| **Evidence Cards** | 4 | 证据卡管理 |
| **Glossary** | 6 | 术语表管理 |
| **Directions** | 5 | 方向管理 |
| **Dimensions** | 5 | 维度管理 |
| **Opinions** | 5 | 观点管理 |
| **Review Queue** | 7 | 审核队列管理 |
| **Snapshots** | 6 | 快照管理 |
| **Publish** | 2 | 发布操作 |
| **Guidance** | 3 | 完整文档聚合 |
| **Health** | 1 | 健康检查 |
| **总计** | **50** | |

---

## 详细端点列表

### 1. Bundles（材料包）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/bundles` | 创建材料包 |
| GET | `/bundles` | 获取材料包列表 |
| GET | `/bundles/{id}` | 获取指定材料包 |
| PUT | `/bundles/{id}` | 更新材料包 |
| DELETE | `/bundles/{id}` | 删除材料包 |

---

### 2. Evidence Cards（证据卡）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/evidence-cards` | 创建证据卡 |
| GET | `/evidence-cards` | 查询证据卡（支持 `?bundle_id=` 筛选） |
| GET | `/evidence-cards/{id}` | 获取指定证据卡 |
| DELETE | `/evidence-cards/{id}` | 删除证据卡 |

---

### 3. Glossary（术语表）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/glossary` | 创建/更新术语 |
| GET | `/glossary` | 获取术语列表 |
| GET | `/glossary/version/{version}` | 按版本获取术语表 |
| GET | `/glossary/{id}` | 获取指定术语 |
| PUT | `/glossary/{id}` | 更新术语 |
| DELETE | `/glossary/{id}` | 删除术语 |

---

### 4. Directions（方向）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/directions` | 创建方向 |
| GET | `/directions` | 获取方向列表 |
| GET | `/directions/{id}` | 获取指定方向 |
| PUT | `/directions/{id}` | 更新方向 |
| DELETE | `/directions/{id}` | 删除方向 |

---

### 5. Dimensions（维度）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/dimensions` | 创建维度 |
| GET | `/dimensions` | 获取维度列表 |
| GET | `/dimensions/direction/{direction_id}` | 按方向获取维度 |
| GET | `/dimensions/{id}` | 获取指定维度 |
| PUT | `/dimensions/{id}` | 更新维度 |
| DELETE | `/dimensions/{id}` | 删除维度 |

---

### 6. Opinions（观点）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/opinions` | 创建观点 |
| GET | `/opinions` | 获取观点列表 |
| GET | `/opinions/dimension/{dimension_id}` | 按维度获取观点 |
| GET | `/opinions/{id}` | 获取指定观点 |
| PUT | `/opinions/{id}` | 更新观点 |
| DELETE | `/opinions/{id}` | 删除观点 |

---

### 7. Review Queue（审核队列）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/review-queue` | 创建审核项 |
| GET | `/review-queue` | 查询审核队列（支持 `?status=` `?item_type=` `?limit=` 筛选） |
| GET | `/review-queue/{id}` | 获取指定审核项 |
| PATCH | `/review-queue/{id}` | 更新审核项状态 |
| DELETE | `/review-queue/{id}` | 删除审核项 |
| POST | `/review-queue/batch` | **批量创建审核项** |
| PATCH | `/review-queue/batch` | **批量更新审核状态** |

---

### 8. Snapshots（快照）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/snapshots` | 创建快照 |
| GET | `/snapshots` | 获取快照列表 |
| GET | `/snapshots/published/latest` | 获取最新已发布快照 |
| GET | `/snapshots/{id}` | 获取指定快照 |
| DELETE | `/snapshots/{id}` | 删除快照 |
| POST | `/snapshots/{id}/publish` | 发布快照 |

---

### 9. Publish（发布）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/publish` | 触发发布操作 |
| GET | `/publish/logs` | 获取发布日志（支持 `?snapshot_id=` 筛选） |

---

### 10. Guidance（完整文档）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/guidance/full/{snapshot_id}` | 获取完整指导文档（方向 + 维度 + 观点 + 术语表） |
| GET | `/guidance/tree` | 获取当前文档树（实时工作状态） |

---

### 11. Health（健康检查）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查端点 |

---

## 新增端点说明（对比初始版本）

### 本次补充的端点

1. **批量操作端点**（Review Queue）
   - `POST /review-queue/batch` - 批量创建审核项
   - `PATCH /review-queue/batch` - 批量更新审核状态

2. **多条件筛选端点**（Review Queue）
   - `GET /review-queue?status=&item_type=&limit=` - 支持按状态和类型同时筛选

3. **完整文档端点**（Guidance）
   - `GET /guidance/full/{snapshot_id}` - 按快照获取完整文档
   - `GET /guidance/tree` - 获取当前文档树

4. **PUT 更新端点**（所有核心实体）
   - `PUT /directions/{id}` - 更新方向
   - `PUT /dimensions/{id}` - 更新维度
   - `PUT /opinions/{id}` - 更新观点
   - `PUT /glossary/{id}` - 更新术语
   - `PUT /bundles/{id}` - 更新材料包

---

## 查询参数说明

### Review Queue 筛选参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `status` | string | "pending" | pending / approved / rejected / needs_revision |
| `item_type` | string | null | direction / dimension / opinion |
| `limit` | integer | 100 | 返回数量限制 |

### 其他筛选参数

| 端点 | 参数 | 说明 |
|------|------|------|
| `GET /evidence-cards` | `bundle_id` | 按材料包 ID 筛选 |
| `GET /glossary/version/{version}` | - | 路径参数指定版本 |
| `GET /dimensions/direction/{direction_id}` | - | 路径参数指定方向 |
| `GET /opinions/dimension/{dimension_id}` | - | 路径参数指定维度 |
| `GET /publish/logs` | `snapshot_id` | 按快照 ID 筛选 |

---

## API 文档访问

启动服务后访问：
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

---

## 服务状态

- **运行状态:** ✅ 正常运行中
- **服务地址:** http://localhost:8000
- **端点总数:** 50 个
