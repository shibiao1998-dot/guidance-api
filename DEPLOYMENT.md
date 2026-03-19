# Guidance API 部署指南（火山云）

本文档提供 Guidance API 部署到火山云的完整方案，实现与 Dify 的稳定对接。

---

## 🎯 方案对比

| 方案 | 适用场景 | 成本 | 稳定性 | 推荐度 |
|------|---------|------|--------|--------|
| **火山云 ECS** | 有云服务器资源 | 中 | ⭐⭐⭐⭐⭐ | ✅ 首选 |
| **火山云 VeContainer** | 有容器服务 | 低 | ⭐⭐⭐⭐⭐ | ✅ 推荐 |
| **localtunnel 内网穿透** | 临时测试 | 免费 | ⭐⭐ | ️ 临时 |

---

## 方案一：火山云 ECS 部署（推荐）

### 前置条件

- 火山云 ECS 云服务器（Ubuntu 20.04 / CentOS 7+）
- 已安装 Python 3.9+
- 已安装 Docker（可选）

### 步骤 1：准备服务器

```bash
# SSH 登录服务器
ssh root@<你的服务器 IP>

# 更新系统
sudo apt update && sudo apt upgrade -y  # Ubuntu
# 或
sudo yum update -y  # CentOS

# 安装 Python 3.9+
sudo apt install python3 python3-pip -y  # Ubuntu
# 或
sudo yum install python3 python3-pip -y  # CentOS
```

### 步骤 2：上传代码

```bash
# 在服务器上创建目录
mkdir -p /opt/guidance-api
cd /opt/guidance-api

# 方式 1：使用 git clone（如果有代码仓库）
git clone <你的仓库地址> .

# 方式 2：使用 scp 从本地上传
# 在本地执行：
# scp -r D:/code/guidance-api/* root@<服务器 IP>:/opt/guidance-api/
```

### 步骤 3：安装依赖

```bash
cd /opt/guidance-api

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 步骤 4：配置环境变量

```bash
# 创建 .env 文件
cat > .env << EOF
DATABASE_URL=sqlite:///./guidance.db
HOST=0.0.0.0
PORT=8000
DEBUG=false
EOF
```

### 步骤 5：配置防火墙

**火山云安全组配置：**

1. 登录火山云控制台
2. 进入「安全组」配置
3. 添加入站规则：
   - 端口：`8000`
   - 协议：`TCP`
   - 源地址：`0.0.0.0/0`（或限制为 Dify 服务器 IP）

**系统防火墙：**

```bash
# Ubuntu (ufw)
sudo ufw allow 8000/tcp
sudo ufw reload

# CentOS (firewalld)
sudo firewall-cmd --add-port=8000/tcp --permanent
sudo firewall-cmd --reload
```

### 步骤 6：配置 systemd 服务（开机自启）

```bash
# 创建 systemd 服务文件
sudo cat > /etc/systemd/system/guidance-api.service << EOF
[Unit]
Description=Guidance API Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/guidance-api
Environment="PATH=/opt/guidance-api/venv/bin"
ExecStart=/opt/guidance-api/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 启动服务
sudo systemctl daemon-reload
sudo systemctl start guidance-api
sudo systemctl enable guidance-api

# 检查状态
sudo systemctl status guidance-api
```

### 步骤 7：验证部署

```bash
# 测试本地访问
curl http://localhost:8000/health

# 测试公网访问（从其他机器）
curl http://<服务器公网 IP>:8000/health
```

预期输出：
```json
{"status":"healthy","version":"1.0.0"}
```

---

## 方案二：火山云 VeContainer 部署

### 前置条件

- 火山云账号已开通 VeContainer 服务
- 本地已安装 Docker

### 步骤 1：构建 Docker 镜像

```bash
cd D:\code\guidance-api

# 创建 Dockerfile
cat > Dockerfile << EOF
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# 构建镜像
docker build -t guidance-api:latest .
```

### 步骤 2：推送镜像到火山云镜像仓库

```bash
# 登录火山云镜像仓库
docker login <火山云镜像仓库地址>

# 打标签
docker tag guidance-api:latest <火山云镜像仓库地址>/guidance-api:latest

# 推送
docker push <火山云镜像仓库地址>/guidance-api:latest
```

### 步骤 3：在 VeContainer 创建服务

1. 登录火山云控制台
2. 进入「VeContainer」服务
3. 创建新容器组：
   - 镜像：选择刚推送的 `guidance-api:latest`
   - 端口：`8000`
   - 环境变量：
     - `DATABASE_URL=sqlite:///./guidance.db`
     - `HOST=0.0.0.0`
     - `PORT=8000`
4. 配置公网访问：
   - 开启「公网访问」
   - 记录分配的公网域名

### 步骤 4：验证部署

访问 `https://<VeContainer 分配的域名>/health`

---

## 方案三：Nginx 反向代理（可选，生产推荐）

如果需要 HTTPS 和更专业的部署：

### 安装 Nginx

```bash
sudo apt install nginx -y  # Ubuntu
# 或
sudo yum install nginx -y  # CentOS
```

### 配置 Nginx

```bash
sudo cat > /etc/nginx/sites-available/guidance-api << EOF
server {
    listen 80;
    server_name <你的域名>;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# 启用配置
sudo ln -s /etc/nginx/sites-available/guidance-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 配置 HTTPS（使用 Let's Encrypt）

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d <你的域名>
```

---

## 📋 Dify 配置

部署完成后，在 Dify 中配置：

### 1. 更新 base_url 变量

在 Dify Chatflow 的「变量」面板中：

| 变量名 | 类型 | 值 |
|--------|------|-----|
| `base_url` | String | `http://<服务器 IP>:8000` 或 `https://<你的域名>` |

### 2. 测试连接

创建一个简单的 HTTP Request 节点测试：

| 配置项 | 值 |
|--------|-----|
| 方法 | GET |
| URL | `{{#base_url#}}/health` |

---

## 🔧 本地开发 vs 生产部署

| 配置项 | 本地开发 | 生产部署 |
|--------|---------|---------|
| HOST | `0.0.0.0` | `0.0.0.0` |
| PORT | `8000` | `8000` |
| DEBUG | `true` | `false` |
| 数据库 | SQLite | 建议 PostgreSQL |
| 访问地址 | `http://localhost:8000` | `http://<公网 IP>:8000` 或 `https://<域名>` |

---

## 📞 常见问题

### Q: 部署后 Dify 仍然无法访问？

A: 检查以下几点：
1. 服务器防火墙是否开放 8000 端口
2. 火山云安全组是否添加入站规则
3. 服务是否正常运行：`sudo systemctl status guidance-api`
4. 从 Dify 服务器测试连通性：`curl http://<你的服务器 IP>:8000/health`

### Q: 如何查看日志？

A:
```bash
# systemd 服务日志
sudo journalctl -u guidance-api -f

# 应用日志
tail -f /opt/guidance-api/server.log
```

### Q: 如何更新代码？

A:
```bash
cd /opt/guidance-api
git pull  # 或手动更新文件
sudo systemctl restart guidance-api
```

---

## ✅ 部署检查清单

- [ ] 服务器已准备（ECS 或 VeContainer）
- [ ] 代码已上传到服务器
- [ ] 依赖已安装
- [ ] 环境变量已配置
- [ ] 防火墙已开放 8000 端口
- [ ] 服务已启动并设置开机自启
- [ ] 从外部可访问 `http://<IP>:8000/health`
- [ ] Dify 中 `base_url` 变量已更新
- [ ] Dify HTTP Request 节点测试通过

---

## 📞 下一步

部署完成后，在 Dify 中使用固定域名访问 Guidance API，不再依赖 localtunnel！
