"""Glossary 端点 - 术语表管理"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemas
from database import get_db

router = APIRouter(prefix="/glossary", tags=["glossary"])


@router.post("", response_model=schemas.GlossaryTermResponse, summary="创建/更新术语")
def create_or_update_glossary(term_data: schemas.GlossaryTermCreate, db: Session = Depends(get_db)):
    """创建新术语或更新现有术语（根据 term 名称匹配）"""
    existing = db.query(models.GlossaryTerm).filter(
        models.GlossaryTerm.term == term_data.term
    ).first()

    if existing:
        # 更新现有术语
        existing.definition = term_data.definition
        existing.category = term_data.category
        existing.version = term_data.version
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # 创建新术语
        db_term = models.GlossaryTerm(**term_data.model_dump())
        db.add(db_term)
        db.commit()
        db.refresh(db_term)
        return db_term


@router.get("/{term_id}", response_model=schemas.GlossaryTermResponse, summary="获取术语")
def get_glossary_term(term_id: int, db: Session = Depends(get_db)):
    """根据 ID 获取术语"""
    term = db.query(models.GlossaryTerm).filter(models.GlossaryTerm.id == term_id).first()
    if not term:
        raise HTTPException(status_code=404, detail="Glossary term not found")
    return term


@router.get("/version/{version}", response_model=List[schemas.GlossaryTermResponse], summary="获取指定版本的术语表")
def get_glossary_by_version(version: str, db: Session = Depends(get_db)):
    """获取指定版本的所有术语"""
    terms = db.query(models.GlossaryTerm).filter(
        models.GlossaryTerm.version == version
    ).all()
    return terms


@router.get("", response_model=List[schemas.GlossaryTermResponse], summary="获取术语列表")
def list_glossary_terms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取术语列表"""
    terms = db.query(models.GlossaryTerm).order_by(models.GlossaryTerm.term).offset(skip).limit(limit).all()
    return terms


@router.put("/{term_id}", response_model=schemas.GlossaryTermResponse, summary="更新术语")
def update_glossary_term(term_id: int, term_update: schemas.GlossaryTermUpdate, db: Session = Depends(get_db)):
    """更新术语"""
    db_term = db.query(models.GlossaryTerm).filter(models.GlossaryTerm.id == term_id).first()
    if not db_term:
        raise HTTPException(status_code=404, detail="Glossary term not found")

    update_data = term_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_term, field, value)

    db.commit()
    db.refresh(db_term)
    return db_term


@router.delete("/{term_id}", status_code=204, summary="删除术语")
def delete_glossary_term(term_id: int, db: Session = Depends(get_db)):
    """删除术语"""
    db_term = db.query(models.GlossaryTerm).filter(models.GlossaryTerm.id == term_id).first()
    if not db_term:
        raise HTTPException(status_code=404, detail="Glossary term not found")

    db.delete(db_term)
    db.commit()
    return None
