"""Direction 端点 - 方向管理"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db

router = APIRouter(prefix="/directions", tags=["directions"])


@router.post("", response_model=schemas.DirectionResponse, summary="创建方向")
def create_direction(direction: schemas.DirectionCreate, db: Session = Depends(get_db)):
    """创建一个新的方向"""
    db_direction = models.Direction(
        name=direction.name,
        description=direction.description,
        rationale=direction.rationale,
        sort_order=direction.sort_order,
        version=direction.version
    )
    db.add(db_direction)
    db.commit()
    db.refresh(db_direction)
    return db_direction


@router.get("/{direction_id}", response_model=schemas.DirectionResponse, summary="获取方向")
def get_direction(direction_id: int, db: Session = Depends(get_db)):
    """根据 ID 获取方向"""
    direction = db.query(models.Direction).filter(models.Direction.id == direction_id).first()
    if not direction:
        raise HTTPException(status_code=404, detail="Direction not found")
    return direction


@router.get("", response_model=List[schemas.DirectionResponse], summary="获取方向列表")
def list_directions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取方向列表"""
    directions = db.query(models.Direction).order_by(models.Direction.sort_order).offset(skip).limit(limit).all()
    return directions


@router.put("/{direction_id}", response_model=schemas.DirectionResponse, summary="更新方向")
def update_direction(direction_id: int, direction_update: schemas.DirectionUpdate, db: Session = Depends(get_db)):
    """更新方向"""
    db_direction = db.query(models.Direction).filter(models.Direction.id == direction_id).first()
    if not db_direction:
        raise HTTPException(status_code=404, detail="Direction not found")

    update_data = direction_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_direction, field, value)

    db.commit()
    db.refresh(db_direction)
    return db_direction


@router.delete("/{direction_id}", status_code=204, summary="删除方向")
def delete_direction(direction_id: int, db: Session = Depends(get_db)):
    """删除方向"""
    db_direction = db.query(models.Direction).filter(models.Direction.id == direction_id).first()
    if not db_direction:
        raise HTTPException(status_code=404, detail="Direction not found")

    db.delete(db_direction)
    db.commit()
    return None
