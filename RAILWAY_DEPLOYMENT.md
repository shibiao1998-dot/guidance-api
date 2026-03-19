# Railway 部署指南（5 分钟完成）

无需服务器权限，一键部署 Guidance API 到云端。

---

## 📋 部署前准备

### 1. 确保代码在 GitHub 上

如果你的代码还不在 GitHub 上，先上传：

```bash
cd D:\code\guidance-api

# 初始化 git（如果还没有）
git init

# 添加所有文件
git add .

# 创建提交
git commit -m "Initial commit - Guidance API for Railway"

# 创建 GitHub 仓库并推送
# 访问 https://github.com/new 创建仓库
# 然后执行：
git remote add origin https://github.com/<你的用户名>/<仓库名>.git
git branch -M main
git push -u origin main
```

---

## 🚀 Railway 部署步骤

### 步骤 1：访问 Railway

1. 打开 https://railway.app
2. 点击 **"Start a New Project"**
3. 选择 **"Login with GitHub"**

### 步骤 2：创建新项目

1. 点击 **"New Project"**
2. 选择 **"Deploy from GitHub repo"**
3. 选择你的 `guidance-api` 仓库

### 步骤 3：配置环境变量

在 Railway 控制台的 **"Variables"** 标签页，添加以下变量：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `HOST` | `0.0.0.0` | 监听所有网卡 |
| `PORT` | `8000` | 端口（Railway 会自动分配） |
| `DEBUG` | `false` | 生产环境关闭调试 |

> 💡 **数据库不需要配置！** Railway 会自动检测并创建 PostgreSQL 数据库，`DATABASE_URL` 会自动注入。

### 步骤 4：添加 PostgreSQL 数据库

1. 在项目中点击 **"New"** → **"Database"** → **"Add PostgreSQL"**
2. Railway 会自动创建并连接数据库
3. 数据库连接字符串会自动注入到环境变量 `DATABASE_URL`

### 步骤 5：部署

1. Railway 会自动开始构建和部署
2. 等待约 2-3 分钟
3. 部署完成后，你会看到一个域名：
   ```
   https://guidance-api-production.up.railway.app
   ```

### 步骤 6：测试部署

访问：
```
https://<你的 railway 域名>/health
```

应该看到：
```json
{"status":"healthy","version":"1.0.0"}
```

---

## 🔧 在 Dify 中配置

### 更新 base_url 变量

在 Dify Chatflow 的「变量」面板中：

| 变量名 | 类型 | 值 |
|--------|------|-----|
| `base_url` | String | `https://<你的 railway 域名>` |

**示例：**
```
base_url = https://guidance-api-production.up.railway.app
```

### 测试连接

创建一个简单的 HTTP Request 节点：

| 配置项 | 值 |
|--------|-----|
| 方法 | GET |
| URL | `{{#base_url#}}/health` |

---

## 💰 费用说明

Railway 免费计划：
- **$5/月 信用额度**（约等于 500 小时运行时间）
- **足够个人使用和测试**
- 如果超出，会邮件通知你

Guidance API 是轻量应用，$5 额度基本够用！

---

## 🔧 常见问题

### Q: 部署失败怎么办？

A: 查看部署日志：
1. 在 Railway 项目页面点击 **"Deployments"**
2. 点击最近的部署记录
3. 查看 **"Build Logs"** 和 **"Deploy Logs"**

常见错误：
- `requirements.txt` 格式错误 → 检查是否有空格/缩进
- 端口配置错误 → 确保使用 `$PORT` 环境变量

### Q: 如何更新代码？

A:
1. 在本地修改代码
2. `git push` 到 GitHub
3. Railway 会自动重新部署（约 2 分钟）

### Q: 如何查看数据库？

A:
1. 在 Railway 项目页面点击 PostgreSQL 服务
2. 点击 **"Connect"** → **"View connection string"**
3. 使用本地数据库工具连接（如 DBeaver、pgAdmin）

### Q: 服务会休眠吗？

A: Railway 免费计划**不会休眠**（这是和 Render/Heroku 的区别）

---

## 📋 部署检查清单

- [ ] 代码已上传到 GitHub
- [ ] Railway 账号已登录
- [ ] 项目已从 GitHub 导入
- [ ] PostgreSQL 数据库已添加
- [ ] 环境变量已配置（HOST, PORT, DEBUG）
- [ ] 部署成功完成
- [ ] `/health` 端点测试通过
- [ ] Dify 中 `base_url` 变量已更新
- [ ] Dify HTTP Request 节点测试通过

---

## 🎯 部署后的 URL

部署完成后，你将拥有固定的 API 地址：

```
https://<你的项目名>.production.up.railway.app
```

这个 URL 是**永久的**，不会像 localtunnel 那样变化！

---

## 📞 需要帮助？

如果部署遇到问题：
1. 查看 Railway 文档：https://docs.railway.app
2. 检查部署日志
3. 确认环境变量配置正确
