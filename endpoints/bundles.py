"""Bundle 端点 - 材料包管理"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db

router = APIRouter(prefix="/bundles", tags=["bundles"])


@router.post("", response_model=schemas.BundleResponse, summary="创建材料包")
def create_bundle(bundle: schemas.BundleCreate, db: Session = Depends(get_db)):
    """创建一个新的材料包"""
    db_bundle = models.Bundle(
        name=bundle.name,
        description=bundle.description,
        metadata_json=bundle.metadata_json
    )
    db.add(db_bundle)
    db.commit()
    db.refresh(db_bundle)
    return db_bundle


@router.get("/{bundle_id}", response_model=schemas.BundleResponse, summary="获取材料包")
def get_bundle(bundle_id: int, db: Session = Depends(get_db)):
    """根据 ID 获取材料包"""
    bundle = db.query(models.Bundle).filter(models.Bundle.id == bundle_id).first()
    if not bundle:
        raise HTTPException(status_code=404, detail="Bundle not found")
    return bundle


@router.get("", response_model=List[schemas.BundleResponse], summary="获取材料包列表")
def list_bundles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取材料包列表"""
    bundles = db.query(models.Bundle).offset(skip).limit(limit).all()
    return bundles


@router.put("/{bundle_id}", response_model=schemas.BundleResponse, summary="更新材料包")
def update_bundle(bundle_id: int, bundle_update: schemas.BundleUpdate, db: Session = Depends(get_db)):
    """更新材料包"""
    db_bundle = db.query(models.Bundle).filter(models.Bundle.id == bundle_id).first()
    if not db_bundle:
        raise HTTPException(status_code=404, detail="Bundle not found")

    update_data = bundle_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_bundle, field, value)

    db.commit()
    db.refresh(db_bundle)
    return db_bundle


@router.delete("/{bundle_id}", status_code=204, summary="删除材料包")
def delete_bundle(bundle_id: int, db: Session = Depends(get_db)):
    """删除材料包"""
    db_bundle = db.query(models.Bundle).filter(models.Bundle.id == bundle_id).first()
    if not db_bundle:
        raise HTTPException(status_code=404, detail="Bundle not found")

    db.delete(db_bundle)
    db.commit()
    return None
