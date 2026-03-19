"""Opinion 端点 - 观点管理"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db

router = APIRouter(prefix="/opinions", tags=["opinions"])


@router.post("", response_model=schemas.OpinionResponse, summary="创建观点")
def create_opinion(opinion: schemas.OpinionCreate, db: Session = Depends(get_db)):
    """创建一个新的观点"""
    # 验证 dimension 是否存在
    dimension = db.query(models.Dimension).filter(models.Dimension.id == opinion.dimension_id).first()
    if not dimension:
        raise HTTPException(status_code=404, detail="Dimension not found")

    db_opinion = models.Opinion(
        dimension_id=opinion.dimension_id,
        content=opinion.content,
        reasoning=opinion.reasoning,
        evidence_refs=opinion.evidence_refs,
        sort_order=opinion.sort_order,
        version=opinion.version
    )
    db.add(db_opinion)
    db.commit()
    db.refresh(db_opinion)
    return db_opinion


@router.get("/{opinion_id}", response_model=schemas.OpinionResponse, summary="获取观点")
def get_opinion(opinion_id: int, db: Session = Depends(get_db)):
    """根据 ID 获取观点"""
    opinion = db.query(models.Opinion).filter(models.Opinion.id == opinion_id).first()
    if not opinion:
        raise HTTPException(status_code=404, detail="Opinion not found")
    return opinion


@router.get("", response_model=List[schemas.OpinionResponse], summary="获取观点列表")
def list_opinions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取观点列表"""
    opinions = db.query(models.Opinion).order_by(models.Opinion.sort_order).offset(skip).limit(limit).all()
    return opinions


@router.get("/dimension/{dimension_id}", response_model=List[schemas.OpinionResponse], summary="按维度获取观点")
def list_opinions_by_dimension(dimension_id: int, db: Session = Depends(get_db)):
    """获取指定维度下的所有观点"""
    opinions = db.query(models.Opinion).filter(
        models.Opinion.dimension_id == dimension_id
    ).order_by(models.Opinion.sort_order).all()
    return opinions


@router.put("/{opinion_id}", response_model=schemas.OpinionResponse, summary="更新观点")
def update_opinion(opinion_id: int, opinion_update: schemas.OpinionUpdate, db: Session = Depends(get_db)):
    """更新观点"""
    db_opinion = db.query(models.Opinion).filter(models.Opinion.id == opinion_id).first()
    if not db_opinion:
        raise HTTPException(status_code=404, detail="Opinion not found")

    update_data = opinion_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_opinion, field, value)

    db.commit()
    db.refresh(db_opinion)
    return db_opinion


@router.delete("/{opinion_id}", status_code=204, summary="删除观点")
def delete_opinion(opinion_id: int, db: Session = Depends(get_db)):
    """删除观点"""
    db_opinion = db.query(models.Opinion).filter(models.Opinion.id == opinion_id).first()
    if not db_opinion:
        raise HTTPException(status_code=404, detail="Opinion not found")

    db.delete(db_opinion)
    db.commit()
    return None
