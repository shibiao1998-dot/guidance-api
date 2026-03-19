"""Snapshot 端点 - 快照管理"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemas
from database import get_db

router = APIRouter(prefix="/snapshots", tags=["snapshots"])


@router.post("", response_model=schemas.SnapshotResponse, summary="创建快照")
def create_snapshot(snapshot: schemas.SnapshotCreate, db: Session = Depends(get_db)):
    """创建一个新的文档快照"""
    db_snapshot = models.Snapshot(
        version=snapshot.version,
        guidance_doc=snapshot.guidance_doc,
        guidance_contract=snapshot.guidance_contract,
        change_log=snapshot.change_log,
        created_by=snapshot.created_by,
        is_published=0
    )
    db.add(db_snapshot)
    db.commit()
    db.refresh(db_snapshot)
    return db_snapshot


@router.get("/{snapshot_id}", response_model=schemas.SnapshotResponse, summary="获取快照")
def get_snapshot(snapshot_id: int, db: Session = Depends(get_db)):
    """根据 ID 获取快照"""
    snapshot = db.query(models.Snapshot).filter(models.Snapshot.id == snapshot_id).first()
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    return snapshot


@router.get("", response_model=List[schemas.SnapshotResponse], summary="获取快照列表")
def list_snapshots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取快照列表"""
    snapshots = db.query(models.Snapshot).order_by(
        models.Snapshot.created_at.desc()
    ).offset(skip).limit(limit).all()
    return snapshots


@router.get("/published/latest", response_model=schemas.SnapshotResponse, summary="获取最新已发布快照")
def get_latest_published_snapshot(db: Session = Depends(get_db)):
    """获取最新已发布的快照"""
    snapshot = db.query(models.Snapshot).filter(
        models.Snapshot.is_published == 1
    ).order_by(models.Snapshot.created_at.desc()).first()
    if not snapshot:
        raise HTTPException(status_code=404, detail="No published snapshot found")
    return snapshot


@router.post("/{snapshot_id}/publish", response_model=schemas.SnapshotResponse, summary="发布快照")
def publish_snapshot(snapshot_id: int, db: Session = Depends(get_db)):
    """发布快照"""
    snapshot = db.query(models.Snapshot).filter(models.Snapshot.id == snapshot_id).first()
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    snapshot.is_published = 1
    db.commit()
    db.refresh(snapshot)
    return snapshot


@router.delete("/{snapshot_id}", status_code=204, summary="删除快照")
def delete_snapshot(snapshot_id: int, db: Session = Depends(get_db)):
    """删除快照"""
    snapshot = db.query(models.Snapshot).filter(models.Snapshot.id == snapshot_id).first()
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    db.delete(snapshot)
    db.commit()
    return None
