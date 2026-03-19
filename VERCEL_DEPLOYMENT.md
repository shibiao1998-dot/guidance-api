# Vercel 部署指南（免费，无需服务器权限）

适合 Dify 普通用户，无需服务器权限，5 分钟完成部署。

---

## 🚀 快速部署步骤

### 步骤 1：准备代码

确保你的 `guidance-api` 目录包含以下文件：

```
guidance-api/
├── main.py
├── requirements.txt
├── vercel.json          # 新增：Vercel 配置
└── api/                 # 新增：Vercel Serverless 函数目录
    └── index.py
```

### 步骤 2：创建 Vercel 配置文件

在项目根目录创建 `vercel.json`：

```json
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

### 步骤 3：注册 Vercel

1. 访问 https://vercel.com
2. 用 GitHub 账号登录
3. 点击 "New Project"

### 步骤 4：导入项目

1. 选择 "Import Git Repository"
2. 选择你的代码仓库（或上传代码到 GitHub）
3. 点击 "Deploy"

### 步骤 5：获取部署后的 URL

部署完成后，你会得到类似这样的 URL：
```
https://guidance-api-xxx.vercel.app
```

### 步骤 6：在 Dify 中配置

更新 `base_url` 变量：
```
base_url = https://guidance-api-xxx.vercel.app
```

---

## ⚠️ 注意事项

1. **数据库持久化**：Vercel 是 Serverless，本地 SQLite 无法持久化
   - 解决方案：使用免费的 **Supabase**（PostgreSQL）或 **Neon**（Serverless Postgres）

2. **冷启动**：免费服务有冷启动延迟（约 3-5 秒）
   - 可以接受的话没问题

3. **请求限制**：Vercel 免费计划每月 100GB 带宽，足够测试用

---

## 🔧 如果需要数据库

### 使用 Supabase（免费 PostgreSQL）

1. 访问 https://supabase.com
2. 创建免费项目
3. 获取数据库连接字符串
4. 在 Vercel 环境变量中设置：
   ```
   DATABASE_URL=postgresql://xxx.supabase.co/...
   ```

---

## 📞 需要帮助？

如果部署遇到问题，可以：
1. 查看 Vercel 部署日志
2. 检查环境变量配置
3. 测试 `/health` 端点是否正常
