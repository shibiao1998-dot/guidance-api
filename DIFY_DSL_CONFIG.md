# Dify DSL 配置说明

由于 Dify DSL 文件格式较为复杂且可能随版本变化，建议使用以下方式配置：

## 方式一：手动配置（推荐）

1. 打开 Dify 平台，创建新的 Chatflow
2. 按照 [`DIFY_HTTP_CONFIG.md`](./DIFY_HTTP_CONFIG.md) 文档逐个添加 HTTP Request 节点
3. 每个节点的配置都已详细列出

## 方式二：使用配置脚本（待开发）

可以开发一个脚本自动生成 Dify DSL 文件。

## 必需的环境变量

在 Dify 中配置以下环境变量：

```
GUIDANCE_API_BASE_URL=http://localhost:8000
```

## 会话变量设计（Create 模式）

| 变量名 | 类型 | 说明 |
|--------|------|------|
| `session_mode` | string | create / scaffold_completion / update / discuss |
| `ui_stage` | string | 当前交互阶段 |
| `glossary_data` | string | 术语表 JSON 字符串 |
| `directions_data` | string | 方向数据 JSON 字符串 |
| `dimensions_data` | string | 维度数据 JSON 字符串 |
| `opinions_data` | string | 观点数据 JSON 字符串 |
| `review_queue` | string | 待审项队列 JSON 字符串 |
| `review_cursor` | string | 当前审核进度 |
| `current_scope` | string | 当前操作范围 |
| `pending_changes` | string | 待确认变更 JSON 字符串 |
| `original_doc` | string | update 模式下的原始文档 JSON 字符串 |
| `doc_completeness` | string | none / directions_only / directions_dimensions / full |

## 外部存储策略

### MVP 阶段（会话变量暂存）

所有数据暂时存储在会话变量中，适合：
- 单次会话完成创建/更新
- 文档规模较小
- 快速验证核心流程

### 完整方案（外部 API 存储）

正文数据存储在外部 API 中，会话变量只存引用 ID：

```
session.direction_ids = [1, 2, 3]  # 只存 ID
→ 通过 HTTP GET /directions 获取完整数据
```

优势：
- 突破 500K 会话变量限制
- 支持跨会话持久化
- 支持多人协作审核

## 下一步

1. ✅ 运行 Guidance API 服务
2. ✅ 测试 API 端点（访问 http://localhost:8000/docs）
3. ⏭️ 在 Dify 中配置 HTTP Request 节点
4. ⏭️ 搭建主 Chatflow 节点图
