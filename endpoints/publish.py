"""Publish 端点 - 发布管理"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemas
from database import get_db

router = APIRouter(prefix="/publish", tags=["publish"])


@router.post("", response_model=schemas.PublishResponse, summary="触发发布操作")
def create_publish_action(publish: schemas.PublishCreate, db: Session = Depends(get_db)):
    """创建发布操作（publish/unpublish）"""
    # 验证 snapshot 是否存在
    snapshot = db.query(models.Snapshot).filter(models.Snapshot.id == publish.snapshot_id).first()
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    if publish.action not in ["publish", "unpublish"]:
        raise HTTPException(status_code=400, detail="Invalid action. Must be 'publish' or 'unpublish'")

    # 更新快照状态
    if publish.action == "publish":
        snapshot.is_published = 1
    else:
        snapshot.is_published = 0

    # 创建发布日志
    db_publish = models.PublishLog(
        snapshot_id=publish.snapshot_id,
        action=publish.action,
        triggered_by=publish.triggered_by,
        metadata_json=publish.metadata_json
    )
    db.add(db_publish)
    db.commit()
    db.refresh(db_publish)

    return db_publish


@router.get("/logs", response_model=List[schemas.PublishResponse], summary="获取发布日志")
def list_publish_logs(
    snapshot_id: Optional[int] = Query(None, description="按快照 ID 筛选"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取发布日志列表"""
    query = db.query(models.PublishLog)
    if snapshot_id is not None:
        query = query.filter(models.PublishLog.snapshot_id == snapshot_id)
    logs = query.order_by(
        models.PublishLog.created_at.desc()
    ).offset(skip).limit(limit).all()
    return logs
