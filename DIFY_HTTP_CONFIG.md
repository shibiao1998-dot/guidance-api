# Dify HTTP Request 节点配置指南

本文档提供完整的 Dify HTTP Request 节点配置，用于调用 Guidance API。

## 基础配置

### 📌 重要：配置应用变量（只需配置一次）

在 Dify Chatflow 的**「变量」**面板中，添加一个应用级变量：

| 变量名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `base_url` | String | `https://pink-camels-notice.loca.lt` | Guidance API 的 Base URL |

**之后所有 HTTP Request 节点的 URL 都使用 `{{#base_url#}}/端点路径` 格式**

这样当 localtunnel URL 变更时，只需修改变量默认值，不需要修改每个节点！

---

**通用 Headers:**
```
Content-Type: application/json
```

---

### 当前 URL 状态

| 状态 | URL | 更新时间 |
|------|-----|----------|
| ✅ 当前可用 | `https://pink-camels-notice.loca.lt` | 2026-03-19 |
| ❌ 已失效 | `https://lemon-kids-write.loca.lt` | - |
| ❌ 已失效 | `https://solid-planets-camp.loca.lt` | - |
| ❌ 已失效 | `https://nine-shoes-wash.loca.lt` | - |

> ⚠️ **注意**：localtunnel 每次重启会生成新 URL，请在 Dify 变量中更新 `base_url` 为最新值

---

---

## 1. Bundle 端点

### 1.1 创建材料包

| 配置项 | 值 |
|--------|-----|
| 方法 | POST |
| URL | `{{#base_url#}}/bundles` |
| Body | JSON |

**Body 内容:**
```json
{
  "name": "{{bundle_name}}",
  "description": "{{bundle_description}}",
  "metadata_json": {{bundle_metadata}}
}
```

**输出变量映射:**
- `bundle_id` → `$.id`
- `bundle_name` → `$.name`

---

### 1.2 获取材料包

| 配置项 | 值 |
|--------|-----|
| 方法 | GET |
| URL | `{{#base_url#}}/bundles/{{bundle_id}}` |

---

## 2. Evidence Cards 端点

### 2.1 创建证据卡

| 配置项 | 值 |
|--------|-----|
| 方法 | POST |
| URL | `{{#base_url#}}/evidence-cards` |
| Body | JSON |

**Body 内容:**
```json
{
  "bundle_id": {{bundle_id}},
  "content": "{{evidence_content}}",
  "source_type": "{{source_type}}",
  "source_ref": "{{source_ref}}",
  "tags": {{tags_json}}
}
```

---

### 2.2 查询证据卡（按 bundle_id）

| 配置项 | 值 |
|--------|-----|
| 方法 | GET |
| URL | `{{#base_url#}}/evidence-cards?bundle_id={{bundle_id}}` |

---

## 3. Glossary 端点

### 3.1 创建/更新术语

| 配置项 | 值 |
|--------|-----|
| 方法 | POST |
| URL | `{{#base_url#}}/glossary` |
| Body | JSON |

**Body 内容:**
```json
{
  "term": "{{term_name}}",
  "definition": "{{term_definition}}",
  "category": "{{term_category}}",
  "version": "{{term_version}}"
}
```

---

### 3.2 获取术语表（按版本）

| 配置项 | 值 |
|--------|-----|
| 方法 | GET |
| URL | `{{#base_url#}}/glossary/version/{{version}}` |

---

## 4. Directions 端点

### 4.1 创建方向

| 配置项 | 值 |
|--------|-----|
| 方法 | POST |
| URL | `{{#base_url#}}/directions` |
| Body | JSON |

**Body 内容:**
```json
{
  "name": "{{direction_name}}",
  "description": "{{direction_description}}",
  "rationale": "{{direction_rationale}}",
  "sort_order": {{direction_sort_order}},
  "version": "{{direction_version}}"
}
```

**输出变量映射:**
- `direction_id` → `$.id`
- `direction_name` → `$.name`

---

### 4.2 获取方向列表

| 配置项 | 值 |
|--------|-----|
| 方法 | GET |
| URL | `{{#base_url#}}/directions` |

---

## 5. Dimensions 端点

### 5.1 创建维度

| 配置项 | 值 |
|--------|-----|
| 方法 | POST |
| URL | `{{#base_url#}}/dimensions` |
| Body | JSON |

**Body 内容:**
```json
{
  "direction_id": {{direction_id}},
  "name": "{{dimension_name}}",
  "description": "{{dimension_description}}",
  "key_points": {{key_points_json}},
  "sort_order": {{dimension_sort_order}},
  "version": "{{dimension_version}}"
}
```

**输出变量映射:**
- `dimension_id` → `$.id`

---

### 5.2 按方向获取维度

| 配置项 | 值 |
|--------|-----|
| 方法 | GET |
| URL | `{{#base_url#}}/dimensions/direction/{{direction_id}}` |

---

## 6. Opinions 端点

### 6.1 创建观点

| 配置项 | 值 |
|--------|-----|
| 方法 | POST |
| URL | `{{#base_url#}}/opinions` |
| Body | JSON |

**Body 内容:**
```json
{
  "dimension_id": {{dimension_id}},
  "content": "{{opinion_content}}",
  "reasoning": "{{opinion_reasoning}}",
  "evidence_refs": {{evidence_refs_json}},
  "sort_order": {{opinion_sort_order}},
  "version": "{{opinion_version}}"
}
```

**输出变量映射:**
- `opinion_id` → `$.id`

---

### 6.2 按维度获取观点

| 配置项 | 值 |
|--------|-----|
| 方法 | GET |
| URL | `{{#base_url#}}/opinions/dimension/{{dimension_id}}` |

---

## 7. Review Queue 端点

### 7.1 创建审核项

| 配置项 | 值 |
|--------|-----|
| 方法 | POST |
| URL | `{{#base_url#}}/review-queue` |
| Body | JSON |

**Body 内容:**
```json
{
  "item_type": "{{item_type}}",
  "item_id": {{item_id}},
  "action": "{{action}}",
  "payload": {{payload_json}}
}
```

**输出变量映射:**
- `review_item_id` → `$.id`

---

### 7.2 获取待审核项

| 配置项 | 值 |
|--------|-----|
| 方法 | GET |
| URL | `{{#base_url#}}/review-queue?status=pending&limit=5` |

---

### 7.3 更新审核状态

| 配置项 | 值 |
|--------|-----|
| 方法 | PATCH |
| URL | `{{#base_url#}}/review-queue/{{review_item_id}}` |
| Body | JSON |

**Body 内容:**
```json
{
  "status": "{{review_status}}",
  "reviewer": "{{reviewer_name}}",
  "comment": "{{review_comment}}"
}
```

---

## 8. Snapshots 端点

### 8.1 创建快照

| 配置项 | 值 |
|--------|-----|
| 方法 | POST |
| URL | `{{#base_url#}}/snapshots` |
| Body | JSON |

**Body 内容:**
```json
{
  "version": "{{doc_version}}",
  "guidance_doc": "{{guidance_doc_md}}",
  "guidance_contract": {{guidance_contract_json}},
  "change_log": "{{change_log}}",
  "created_by": "{{created_by}}"
}
```

**输出变量映射:**
- `snapshot_id` → `$.id`

---

### 8.2 获取最新已发布快照

| 配置项 | 值 |
|--------|-----|
| 方法 | GET |
| URL | `{{#base_url#}}/snapshots/published/latest` |

---

### 8.3 发布快照

| 配置项 | 值 |
|--------|-----|
| 方法 | POST |
| URL | `{{#base_url#}}/snapshots/{{snapshot_id}}/publish` |

---

## 9. Publish 端点

### 9.1 触发发布操作

| 配置项 | 值 |
|--------|-----|
| 方法 | POST |
| URL | `{{#base_url#}}/publish` |
| Body | JSON |

**Body 内容:**
```json
{
  "snapshot_id": {{snapshot_id}},
  "action": "publish",
  "triggered_by": "{{triggered_by}}",
  "metadata_json": {{metadata_json}}
}
```

---

## 10. Guidance 端点（完整文档）

### 10.1 获取完整指导文档（按快照 ID）

| 配置项 | 值 |
|--------|-----|
| 方法 | GET |
| URL | `{{#base_url#}}/guidance/full/{{snapshot_id}}` |

**用途：** update 模式加载原文档、发布时编译完整文档

**返回结构：**
```json
{
  "version": "1.0.0",
  "created_at": "2026-03-18T12:00:00",
  "directions": [...],
  "dimensions": [...],
  "opinions": [...],
  "glossary": [...]
}
```

---

### 10.2 获取当前文档树

| 配置项 | 值 |
|--------|-----|
| 方法 | GET |
| URL | `{{#base_url#}}/guidance/tree` |

**用途：** 实时查看当前工作状态

---

## 11. Review Queue 增强端点

### 11.1 按类型和状态筛选审核项

| 配置项 | 值 |
|--------|-----|
| 方法 | GET |
| URL | `{{#base_url#}}/review-queue?status={{status}}&item_type={{item_type}}&limit={{limit}}` |

**参数说明：**
- `status`: pending / approved / rejected / needs_revision
- `item_type`: direction / dimension / opinion
- `limit`: 返回数量限制（默认 100）

**示例 URL:**
- `GET /review-queue?status=pending&item_type=direction` - 获取待审核的方向级变更
- `GET /review-queue?status=approved&item_type=dimension&limit=50` - 获取已批准的维度变更

---

### 11.2 批量创建审核项

| 配置项 | 值 |
|--------|-----|
| 方法 | POST |
| URL | `{{#base_url#}}/review-queue/batch` |
| Body | JSON |

**Body 内容:**
```json
{
  "items": [
    {
      "item_type": "direction",
      "item_id": 1,
      "action": "update",
      "payload": {"name": "新方向名", "description": "新描述"}
    },
    {
      "item_type": "dimension",
      "item_id": 2,
      "action": "create",
      "payload": {"name": "新维度", "description": "..."}
    }
  ]
}
```

**用途：** 影响分析后一次性写入完整 change set

---

### 11.3 批量更新审核状态

| 配置项 | 值 |
|--------|-----|
| 方法 | PATCH |
| URL | `{{#base_url#}}/review-queue/batch` |
| Body | JSON |

**Body 内容:**
```json
{
  "ids": [1, 2, 3, 4, 5],
  "status": "approved",
  "reviewer": "{{reviewer_name}}",
  "comment": "{{review_comment}}"
}
```

**用途：** 用户批量确认审核项

---

## 12. 更新端点（PUT）

### 12.1 更新方向

| 配置项 | 值 |
|--------|-----|
| 方法 | PUT |
| URL | `{{#base_url#}}/directions/{{direction_id}}` |
| Body | JSON |

**Body 内容:**
```json
{
  "name": "{{new_name}}",
  "description": "{{new_description}}",
  "rationale": "{{new_rationale}}",
  "sort_order": {{new_sort_order}},
  "version": "{{new_version}}"
}
```

---

### 12.2 更新维度

| 配置项 | 值 |
|--------|-----|
| 方法 | PUT |
| URL | `{{#base_url#}}/dimensions/{{dimension_id}}` |
| Body | JSON |

**Body 内容:**
```json
{
  "name": "{{new_name}}",
  "description": "{{new_description}}",
  "key_points": {{key_points_json}},
  "sort_order": {{new_sort_order}},
  "version": "{{new_version}}"
}
```

---

### 12.3 更新观点

| 配置项 | 值 |
|--------|-----|
| 方法 | PUT |
| URL | `{{#base_url#}}/opinions/{{opinion_id}}` |
| Body | JSON |

**Body 内容:**
```json
{
  "content": "{{new_content}}",
  "reasoning": "{{new_reasoning}}",
  "evidence_refs": {{evidence_refs_json}},
  "sort_order": {{new_sort_order}},
  "version": "{{new_version}}"
}
```

---

## 变量类型说明

在 Dify 中引用变量时注意：

| 变量类型 | 示例 | 说明 |
|---------|------|------|
| String | `"{{variable}}"` | 需要引号 |
| Number | `{{variable}}` | 不需要引号 |
| JSON Object/Array | `{{variable}}` | 直接引用，不加引号 |

**Code 节点转换模板**（如需将对象转为 JSON 字符串）：

```python
import json

def main(input_object: dict) -> dict:
    return {
        "json_string": json.dumps(input_object, ensure_ascii=False)
    }
```

---

## 错误处理建议

在每个 HTTP Request 节点后添加 IF/ELSE 分支：

```
IF: {{http_response.status_code}} == 200 或 201
  → 继续正常流程
ELSE:
  → 走错误处理分支（记录日志/返回错误信息）
```

---

## API 文档

启动服务后访问：
- Swagger UI: `{{#base_url#}}/docs`
- ReDoc: `{{#base_url#}}/redoc`
