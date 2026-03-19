"""Guidance 端点 - 完整文档聚合"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db

router = APIRouter(prefix="/guidance", tags=["guidance"])


@router.get("/full/{snapshot_id}", response_model=schemas.GuidanceContract, summary="获取完整指导文档")
def get_full_guidance(snapshot_id: int, db: Session = Depends(get_db)):
    """
    获取完整的企业指导文档（方向 + 维度 + 观点 + 术语表）

    用于 update 模式加载原文档或发布时编译完整文档
    """
    # 验证快照是否存在
    snapshot = db.query(models.Snapshot).filter(models.Snapshot.id == snapshot_id).first()
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    # 获取所有方向
    directions = db.query(models.Direction).order_by(models.Direction.sort_order).all()

    # 获取所有维度（按方向分组）
    dimensions = db.query(models.Dimension).order_by(models.Dimension.sort_order).all()

    # 获取所有观点
    opinions = db.query(models.Opinion).order_by(models.Opinion.sort_order).all()

    # 获取术语表
    glossary = db.query(models.GlossaryTerm).order_by(models.GlossaryTerm.term).all()

    return schemas.GuidanceContract(
        version=snapshot.version,
        created_at=snapshot.created_at,
        directions=directions,
        dimensions=dimensions,
        opinions=opinions,
        glossary=glossary
    )


@router.get("/tree", response_model=schemas.GuidanceDocument, summary="获取当前完整文档树")
def get_guidance_tree(db: Session = Depends(get_db)):
    """
    获取当前数据库中的完整文档树（不包含已发布快照的）

    用于实时查看当前工作状态
    """
    directions = db.query(models.Direction).order_by(models.Direction.sort_order).all()
    dimensions = db.query(models.Dimension).order_by(models.Dimension.sort_order).all()
    opinions = db.query(models.Opinion).order_by(models.Opinion.sort_order).all()

    return schemas.GuidanceDocument(
        directions=directions,
        dimensions=dimensions,
        opinions=opinions
    )
