# Dify HTTP 节点配置指南 - 多租户隔离

## 前置说明

Dify Chatflow 自带以下系统变量（无需额外配置）：

| 系统变量 | 说明 | 示例值 |
|---------|------|--------|
| `sys.conversation_id` | 会话 ID（每轮对话唯一） | `abc123-def456` |
| `sys.user_id` | 用户 ID（如果 Dify 配置了用户系统） | `user_001` |
| `sys.app_id` | 应用 ID | `app_123` |

**注意：** 如果 Dify 没有配置用户系统，`sys.user_id` 可能为空。此时建议使用 `sys.app_id` 或固定值作为 `user_id`。

---

## 方案一：完整隔离（推荐）

**适用场景：** 多用户 + 多会话隔离

### 步骤 1：在「开始」节点确认输入字段

确保「开始」节点包含以下系统变量（默认就有）：
- ✅ `sys.conversation_id`
- ✅ `sys.user_id`（如果没有用户系统，可能为空）

---

### 步骤 2：配置 HTTP Request 节点

#### 2.1 创建材料包（POST /bundles）

**节点配置：**

| 配置项 | 值 |
|--------|-----|
| 方法 | POST |
| URL | `{{#base_url#}}/bundles` |
| Body 类型 | JSON |

**Body 内容：**
```json
{
  "name": "auto_bundle",
  "description": "{{InputClassifier.structured_output.analysis_summary}}",
  "metadata_json": {
    "mode_signal": "{{InputClassifier.structured_output.mode_signal}}",
    "input_type": "{{InputClassifier.structured_output.input_type}}",
    "has_structured_doc": "{{InputClassifier.structured_output.has_structured_doc}}",
    "material_types": "{{InputClassifier.structured_output.material_types_detected}}"
  },
  "user_id": "{{#sys.user_id#}}",
  "session_id": "{{#sys.conversation_id#}}"
}
```

**关键点：**
- `user_id` 使用 `{{#sys.user_id#}}`
- `session_id` 使用 `{{#sys.conversation_id#}}`

---

#### 2.2 查询材料包列表（GET /bundles）

**节点配置：**

| 配置项 | 值 |
|--------|-----|
| 方法 | GET |
| URL | `{{#base_url#}}/bundles?user_id={{#sys.user_id#}}&session_id={{#sys.conversation_id#}}` |

**效果：** 只返回当前用户、当前会话的材料包

---

#### 2.3 创建证据卡（POST /evidence-cards）

**节点配置：**

| 配置项 | 值 |
|--------|-----|
| 方法 | POST |
| URL | `{{#base_url#}}/evidence-cards` |
| Body 类型 | JSON |

**Body 内容：**
```json
{
  "bundle_id": {{bundle_id}},
  "content": "{{evidence_content}}",
  "source_type": "material",
  "source_ref": null,
  "tags": [],
  "user_id": "{{#sys.user_id#}}",
  "session_id": "{{#sys.conversation_id#}}"
}
```

**注意：** 如果证据卡属于某个 Bundle，可以省略 `user_id` 和 `session_id`，会自动继承 Bundle 的值。

---

#### 2.4 查询证据卡列表（GET /evidence-cards）

**节点配置：**

| 配置项 | 值 |
|--------|-----|
| 方法 | GET |
| URL | `{{#base_url#}}/evidence-cards?user_id={{#sys.user_id#}}&session_id={{#sys.conversation_id#}}` |

---

#### 2.5 创建方向（POST /directions）

**节点配置：**

| 配置项 | 值 |
|--------|-----|
| 方法 | POST |
| URL | `{{#base_url#}}/directions` |
| Body 类型 | JSON |

**Body 内容：**
```json
{
  "name": "{{direction_name}}",
  "description": "{{direction_description}}",
  "rationale": "{{direction_rationale}}",
  "sort_order": {{sort_order}},
  "version": "1.0.0",
  "user_id": "{{#sys.user_id#}}",
  "session_id": "{{#sys.conversation_id#}}"
}
```

---

#### 2.6 查询方向列表（GET /directions）

**节点配置：**

| 配置项 | 值 |
|--------|-----|
| 方法 | GET |
| URL | `{{#base_url#}}/directions?user_id={{#sys.user_id#}}&session_id={{#sys.conversation_id#}}` |

---

### 步骤 3：变量映射（可选）

如果想在流程中复用 `user_id` 和 `session_id`，可以在「代码」节点中赋值给会话变量：

```python
def main(args: dict) -> dict:
    return {
        "result": {
            "user_id": args["sys.user_id"],
            "session_id": args["sys.conversation_id"]
        }
    }
```

---

## 方案二：简化隔离（如果没有用户系统）

**适用场景：** Dify 没有配置用户系统，`sys.user_id` 为空

### 使用 `sys.app_id` 作为 `user_id`

```json
{
  "name": "材料包",
  "user_id": "{{#sys.app_id#}}",
  "session_id": "{{#sys.conversation_id#}}"
}
```

**效果：**
- 同一个 Dify 应用的所有用户共享数据
- 每次会话（conversation）的数据独立

---

## 方案三：固定用户（单用户使用）

**适用场景：** 只有一个人使用，但需要区分多次会话

### 使用固定值作为 `user_id`

```json
{
  "name": "材料包",
  "user_id": "fixed_user_001",
  "session_id": "{{#sys.conversation_id#}}"
}
```

**效果：**
- 所有数据属于同一个"用户"
- 每次会话的数据独立

---

## 方案四：团队协作（共享数据）

**适用场景：** 团队共享一份指导文档

### 使用固定的 `user_id` 和 `session_id`

```json
{
  "name": "材料包",
  "user_id": "team_001",
  "session_id": "shared_session"
}
```

**效果：**
- 团队成员看到相同的数据
- 所有人都可以编辑同一份文档

---

## 完整 HTTP 节点配置示例

### 示例 1：创建材料包（带多租户）

```
┌─────────────────────────────────────────────────────────┐
│ HTTP Request 节点：CreateBundle                         │
├─────────────────────────────────────────────────────────┤
│ 方法：POST                                              │
│ URL: {{#base_url#}}/bundles                             │
│                                                         │
│ Body (JSON):                                            │
│ {                                                       │
│   "name": "auto_bundle",                                │
│   "description": "材料包描述",                            │
│   "metadata_json": {},                                  │
│   "user_id": "{{#sys.user_id#}}",                       │
│   "session_id": "{{#sys.conversation_id#}}"             │
│ }                                                       │
│                                                         │
│ 输出变量映射：                                          │
│ - bundle_id → $.id                                      │
│ - bundle_name → $.name                                  │
└─────────────────────────────────────────────────────────┘
```

---

### 示例 2：查询材料包（带隔离）

```
┌─────────────────────────────────────────────────────────┐
│ HTTP Request 节点：GetBundles                           │
├─────────────────────────────────────────────────────────┤
│ 方法：GET                                               │
│ URL: {{#base_url#}}/bundles?user_id={{#sys.user_id#}}&session_id={{#sys.conversation_id#}} │
│                                                         │
│ 输出变量映射：                                          │
│ - bundles → $                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 常见问题

### Q1: `sys.user_id` 为空怎么办？

**A:** 有三种解决方案：

1. **使用 `sys.app_id` 代替：**
   ```json
   "user_id": "{{#sys.app_id#}}"
   ```

2. **使用固定值：**
   ```json
   "user_id": "default_user"
   ```

3. **在 Dify 中配置用户系统**（需要 Dify 管理员权限）

---

### Q2: 如何验证隔离是否生效？

**A:** 在浏览器中访问以下 URL 测试：

```bash
# 查询特定用户的数据
https://guidance-api-production.up.railway.app/bundles?user_id=user_001

# 查询特定会话的数据
https://guidance-api-production.up.railway.app/bundles?session_id=abc123
```

---

### Q3: 旧数据怎么办？

**A:** 旧数据的 `user_id` 和 `session_id` 为 `NULL`。查询时会返回：
- 所有 `NULL` 记录
- 匹配 `user_id` 和 `session_id` 的记录

如果想只查询隔离后的数据，可以添加筛选条件。

---

## 检查清单

配置完成后，请检查：

- [ ] 所有 `POST` 请求都传入了 `user_id` 和 `session_id`
- [ ] 所有 `GET` 请求都添加了筛选参数
- [ ] 变量引用格式正确：`{{#sys.user_id#}}`（注意 `#` 号）
- [ ] 在 Dify 中测试创建和查询，验证数据隔离

---

## 联系支持

如有问题，请查阅：
- 完整文档：`MULTI_TENANCY_GUIDE.md`
- API 文档：https://guidance-api-production.up.railway.app/docs
