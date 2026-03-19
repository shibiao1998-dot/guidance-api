"""Guidance API - 企业顶层指导文档管理系统

提供方向 - 维度 - 观点三层结构的企业指导文档存储服务，
支持材料包管理、证据卡管理、术语表管理、审核队列、快照发布等功能。
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from database import engine, Base

# 导入所有端点
from endpoints import (
    bundles,
    evidence_cards,
    glossary,
    directions,
    dimensions,
    opinions,
    review_queue,
    snapshots,
    publish,
    guidance
)

# 加载环境变量
load_dotenv()

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建 FastAPI 应用
app = FastAPI(
    title="Guidance API",
    description="企业顶层指导文档管理系统 - 方向 - 维度 - 观点三层结构存储",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS（允许 Dify 调用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 健康检查
@app.get("/health", tags=["health"])
def health_check():
    """健康检查端点"""
    return {"status": "healthy", "version": "1.0.0"}


# 注册所有端点
app.include_router(bundles.router)
app.include_router(evidence_cards.router)
app.include_router(glossary.router)
app.include_router(directions.router)
app.include_router(dimensions.router)
app.include_router(opinions.router)
app.include_router(review_queue.router)
app.include_router(snapshots.router)
app.include_router(publish.router)
app.include_router(guidance.router)


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "false").lower() == "true"

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug
    )
