# Dify HTTP 节点配置 - 快速参考

## 核心配置（复制即用）

### 1. 创建材料包

```json
{
  "name": "auto_bundle",
  "description": "{{InputClassifier.structured_output.analysis_summary}}",
  "metadata_json": {},
  "user_id": "{{#sys.user_id#}}",
  "session_id": "{{#sys.conversation_id#}}"
}
```

### 2. 查询材料包

```
GET {{#base_url#}}/bundles?user_id={{#sys.user_id#}}&session_id={{#sys.conversation_id#}}
```

### 3. 创建证据卡

```json
{
  "bundle_id": {{bundle_id}},
  "content": "{{evidence_content}}",
  "user_id": "{{#sys.user_id#}}",
  "session_id": "{{#sys.conversation_id#}}"
}
```

### 4. 查询证据卡

```
GET {{#base_url#}}/evidence-cards?user_id={{#sys.user_id#}}&session_id={{#sys.conversation_id#}}
```

---

## Dify 系统变量

| 变量 | 用途 | 示例 |
|------|------|------|
| `{{#sys.user_id#}}` | 用户 ID | `user_001`（无用户系统时为空） |
| `{{#sys.conversation_id#}}` | 会话 ID | `abc-123-def`（每轮对话唯一） |
| `{{#sys.app_id#}}` | 应用 ID | `app_123`（可替代 user_id） |

---

## 如果没有用户系统

使用 `sys.app_id` 替代：

```json
"user_id": "{{#sys.app_id#}}"
```

---

## 变量格式

✅ 正确：`{{#sys.user_id#}}`
❌ 错误：`{{sys.user_id}}`
❌ 错误：`{{#user_id#}}`

**注意：** 系统变量必须带 `#` 号！
