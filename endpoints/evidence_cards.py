"""EvidenceCard 端点 - 证据卡管理"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemas
from database import get_db

router = APIRouter(prefix="/evidence-cards", tags=["evidence_cards"])


@router.post("", response_model=schemas.EvidenceCardResponse, summary="创建证据卡")
def create_evidence_card(card: schemas.EvidenceCardCreate, db: Session = Depends(get_db)):
    """创建一个新的证据卡"""
    # 验证 bundle 是否存在
    bundle = db.query(models.Bundle).filter(models.Bundle.id == card.bundle_id).first()
    if not bundle:
        raise HTTPException(status_code=404, detail="Bundle not found")

    db_card = models.EvidenceCard(
        bundle_id=card.bundle_id,
        content=card.content,
        source_type=card.source_type,
        source_ref=card.source_ref,
        tags=card.tags,
        user_id=card.user_id or bundle.user_id,  # 如果没有传入，使用 bundle 的 user_id
        session_id=card.session_id or bundle.session_id  # 如果没有传入，使用 bundle 的 session_id
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


@router.get("/{card_id}", response_model=schemas.EvidenceCardResponse, summary="获取证据卡")
def get_evidence_card(card_id: int, db: Session = Depends(get_db)):
    """根据 ID 获取证据卡"""
    card = db.query(models.EvidenceCard).filter(models.EvidenceCard.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Evidence card not found")
    return card


@router.get("", response_model=List[schemas.EvidenceCardResponse], summary="查询证据卡")
def list_evidence_cards(
    bundle_id: Optional[int] = Query(None, description="按材料包 ID 筛选"),
    user_id: Optional[str] = Query(None, description="按用户 ID 筛选"),
    session_id: Optional[str] = Query(None, description="按会话 ID 筛选"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取证据卡列表，支持按 bundle/user/session 筛选"""
    query = db.query(models.EvidenceCard)
    if bundle_id is not None:
        query = query.filter(models.EvidenceCard.bundle_id == bundle_id)
    if user_id:
        query = query.filter(models.EvidenceCard.user_id == user_id)
    if session_id:
        query = query.filter(models.EvidenceCard.session_id == session_id)
    cards = query.offset(skip).limit(limit).all()
    return cards


@router.delete("/{card_id}", status_code=204, summary="删除证据卡")
def delete_evidence_card(card_id: int, db: Session = Depends(get_db)):
    """删除证据卡"""
    card = db.query(models.EvidenceCard).filter(models.EvidenceCard.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Evidence card not found")

    db.delete(card)
    db.commit()
    return None
