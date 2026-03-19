# 多租户隔离使用指南

## 概述

Guidance API 现已支持多租户隔离，通过 `user_id` 和 `session_id` 两个字段实现：

| 字段 | 用途 | 示例 |
|------|------|------|
| `user_id` | 区分不同用户 | `user_123`, `zhangsan` |
| `session_id` | 区分同一用户的不同会话 | `session_abc`, `chatflow_run_001` |

---

## 数据隔离级别

### 级别 1：用户隔离（推荐）

不同用户的数据完全隔离，通过 `user_id` 实现。

**适用场景：** 多用户使用同一个 Dify 实例

**Dify 配置：**
```
user_id = {{#conversation.user_id#}}
```

---

### 级别 2：会话隔离

同一用户的不同会话数据隔离，通过 `user_id` + `session_id` 实现。

**适用场景：** 同一用户多次创建不同的指导文档

**Dify 配置：**
```
user_id = {{#conversation.user_id#}}
session_id = {{#conversation.id#}}
```

---

## 在 Dify 中配置

### 步骤 1：添加变量

在 Dify Chatflow 的「变量」面板中添加：

| 变量名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `base_url` | String | `https://guidance-api-production.up.railway.app` | API 地址 |
| `user_id` | String | `{{#conversation.user_id#}}` | 用户 ID（自动获取） |
| `session_id` | String | `{{#conversation.id#}}` | 会话 ID（自动获取） |

---

### 步骤 2：配置 HTTP Request 节点

#### 创建材料包（Create Bundle）

```
POST {{#base_url#}}/bundles

Body (JSON):
{
  "name": "材料包名称",
  "description": "描述",
  "metadata_json": {},
  "user_id": "{{#user_id#}}",
  "session_id": "{{#session_id#}}"
}
```

#### 查询材料包列表（List Bundles）

```
GET {{#base_url#}}/bundles?user_id={{#user_id#}}&session_id={{#session_id#}}
```

#### 创建证据卡（Create Evidence Card）

```
POST {{#base_url#}}/evidence-cards

Body (JSON):
{
  "bundle_id": 1,
  "content": "证据内容",
  "user_id": "{{#user_id#}}",
  "session_id": "{{#session_id#}}"
}
```

**注意：** 证据卡会自动继承所属 Bundle 的 `user_id` 和 `session_id`（如果没有显式传入）

---

## API 端点支持

以下端点支持 `user_id` 和 `session_id` 筛选：

| 端点 | 筛选参数 | 示例 |
|------|---------|------|
| `GET /bundles` | `?user_id=&session_id=` | `/bundles?user_id=user123` |
| `GET /evidence-cards` | `?user_id=&session_id=&bundle_id=` | `/evidence-cards?user_id=user123` |
| `GET /directions` | `?user_id=&session_id=` | 即将支持 |
| `GET /dimensions` | `?user_id=&session_id=` | 即将支持 |
| `GET /opinions` | `?user_id=&session_id=` | 即将支持 |

---

## 使用场景示例

### 场景 1：单用户多次使用

**需求：** 同一用户可以创建多份独立的指导文档

**配置：**
```
user_id = fixed_user_001
session_id = {{#conversation.id#}}  // 每次对话生成新 ID
```

**效果：**
- 用户每次对话的数据独立
- 可以通过 `session_id` 查询特定会话的数据

---

### 场景 2：多用户使用

**需求：** 多个用户使用同一个 Dify 应用，数据互不干扰

**配置：**
```
user_id = {{#conversation.user_id#}}  // Dify 自动分配
session_id = {{#conversation.id#}}
```

**效果：**
- 不同用户的数据完全隔离
- 每个用户的每次会话也独立

---

### 场景 3：团队协作

**需求：** 团队共享一份指导文档，多人协作编辑

**配置：**
```
user_id = team_001  // 团队共用一个 user_id
session_id = {{#conversation.id#}}  // 或者固定 session_id
```

**效果：**
- 团队成员看到相同的数据
- 可以通过固定的 `session_id` 共享同一份文档

---

## 数据库迁移

多租户字段已通过自动迁移脚本添加，无需手动操作。

如果你想在本地运行迁移：

```bash
cd guidance-api
python migrate_add_tenant_fields.py
```

---

## 常见问题

### Q: 如果不传 `user_id` 和 `session_id` 会怎样？

A: 数据仍然会保存，但无法通过用户/会话筛选查询。建议始终传入这两个字段。

### Q: 旧的数据库记录怎么办？

A: 旧记录的 `user_id` 和 `session_id` 为 `NULL`，查询时会返回所有 `NULL` 记录和匹配的记录。

### Q: 如何查询某个用户的所有数据？

A: 使用 `GET /bundles?user_id=xxx`，会返回该用户的所有材料包。

### Q: 如何删除某个会话的数据？

A:
1. 查询该会话的所有 bundles：`GET /bundles?session_id=xxx`
2. 逐个删除：`DELETE /bundles/{id}`

---

## 下一步

更多端点的多租户筛选支持即将推出：
- `GET /directions?user_id=&session_id=`
- `GET /dimensions?user_id=&session_id=`
- `GET /opinions?user_id=&session_id=`
