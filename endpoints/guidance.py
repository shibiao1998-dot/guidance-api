"""Guidance 端点 - 完整文档聚合"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from collections import defaultdict

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
    获取当前数据库中的完整文档树（树状嵌套结构）

    用于实时查看当前工作状态
    返回结构：directions -> dimensions -> opinions
    """
    # 获取所有方向
    directions = db.query(models.Direction).order_by(models.Direction.sort_order).all()

    # 获取所有维度，按 direction_id 分组
    dimensions = db.query(models.Dimension).order_by(models.Dimension.sort_order).all()
    dimensions_by_direction = defaultdict(list)
    for dim in dimensions:
        dimensions_by_direction[dim.direction_id].append(dim)

    # 获取所有观点，按 dimension_id 分组
    opinions = db.query(models.Opinion).order_by(models.Opinion.sort_order).all()
    opinions_by_dimension = defaultdict(list)
    for opn in opinions:
        opinions_by_dimension[opn.dimension_id].append(opn)

    # 构建树状结构
    tree_directions = []
    for direction in directions:
        dims = dimensions_by_direction.get(direction.id, [])
        dim_with_opinions = []
        for dim in dims:
            opn_list = opinions_by_dimension.get(dim.id, [])
            dim_with_opinions.append(schemas.DimensionWithOpinions(
                id=dim.id,
                name=dim.name,
                description=dim.description,
                key_points=dim.key_points,
                sort_order=dim.sort_order,
                version=dim.version,
                identity_tags=dim.identity_tags or [],
                created_at=dim.created_at,
                updated_at=dim.updated_at,
                opinions=opn_list
            ))
        tree_directions.append(schemas.DirectionWithChildren(
            id=direction.id,
            name=direction.name,
            description=direction.description,
            rationale=direction.rationale,
            sort_order=direction.sort_order,
            version=direction.version,
            created_at=direction.created_at,
            updated_at=direction.updated_at,
            dimensions=dim_with_opinions
        ))

    return schemas.GuidanceDocument(directions=tree_directions)
