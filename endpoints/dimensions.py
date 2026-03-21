"""Dimension 端点 - 维度管理"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db

router = APIRouter(prefix="/dimensions", tags=["dimensions"])


@router.post("", response_model=schemas.DimensionResponse, summary="创建维度")
def create_dimension(dimension: schemas.DimensionCreate, db: Session = Depends(get_db)):
    """创建一个新的维度"""
    # 验证 direction 是否存在
    direction = db.query(models.Direction).filter(models.Direction.id == dimension.direction_id).first()
    if not direction:
        raise HTTPException(status_code=404, detail="Direction not found")

    db_dimension = models.Dimension(
        direction_id=dimension.direction_id,
        name=dimension.name,
        description=dimension.description,
        key_points=dimension.key_points,
        sort_order=dimension.sort_order,
        version=dimension.version,
        identity_tags=dimension.identity_tags or []
    )
    db.add(db_dimension)
    db.commit()
    db.refresh(db_dimension)
    return db_dimension


@router.get("/{dimension_id}", response_model=schemas.DimensionResponse, summary="获取维度")
def get_dimension(dimension_id: int, db: Session = Depends(get_db)):
    """根据 ID 获取维度"""
    dimension = db.query(models.Dimension).filter(models.Dimension.id == dimension_id).first()
    if not dimension:
        raise HTTPException(status_code=404, detail="Dimension not found")
    return dimension


@router.get("", response_model=List[schemas.DimensionResponse], summary="获取维度列表")
def list_dimensions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取维度列表"""
    dimensions = db.query(models.Dimension).order_by(models.Dimension.sort_order).offset(skip).limit(limit).all()
    return dimensions


@router.get("/direction/{direction_id}", response_model=List[schemas.DimensionResponse], summary="按方向获取维度")
def list_dimensions_by_direction(direction_id: int, db: Session = Depends(get_db)):
    """获取指定方向下的所有维度"""
    dimensions = db.query(models.Dimension).filter(
        models.Dimension.direction_id == direction_id
    ).order_by(models.Dimension.sort_order).all()
    return dimensions


@router.put("/{dimension_id}", response_model=schemas.DimensionResponse, summary="更新维度")
def update_dimension(dimension_id: int, dimension_update: schemas.DimensionUpdate, db: Session = Depends(get_db)):
    """更新维度"""
    db_dimension = db.query(models.Dimension).filter(models.Dimension.id == dimension_id).first()
    if not db_dimension:
        raise HTTPException(status_code=404, detail="Dimension not found")

    update_data = dimension_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_dimension, field, value)

    db.commit()
    db.refresh(db_dimension)
    return db_dimension


@router.delete("/{dimension_id}", status_code=204, summary="删除维度")
def delete_dimension(dimension_id: int, db: Session = Depends(get_db)):
    """删除维度"""
    db_dimension = db.query(models.Dimension).filter(models.Dimension.id == dimension_id).first()
    if not db_dimension:
        raise HTTPException(status_code=404, detail="Dimension not found")

    db.delete(db_dimension)
    db.commit()
    return None
