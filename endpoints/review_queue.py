"""ReviewQueue 端点 - 审核队列管理"""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemas
from database import get_db
from schemas import ReviewStatusEnum

router = APIRouter(prefix="/review-queue", tags=["review_queue"])


@router.post("", response_model=schemas.ReviewQueueResponse, summary="创建审核项")
def create_review_item(item: schemas.ReviewQueueCreate, db: Session = Depends(get_db)):
    """创建一个新的审核项"""
    db_item = models.ReviewQueue(
        item_type=item.item_type,
        item_id=item.item_id,
        action=item.action,
        payload=item.payload
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/{queue_id}", response_model=schemas.ReviewQueueResponse, summary="获取审核项")
def get_review_item(queue_id: int, db: Session = Depends(get_db)):
    """根据 ID 获取审核项"""
    item = db.query(models.ReviewQueue).filter(models.ReviewQueue.id == queue_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Review queue item not found")
    return item


@router.get("", response_model=List[schemas.ReviewQueueResponse], summary="查询审核队列")
def list_review_queue(
    status: Optional[str] = Query("pending", description="状态筛选：pending/approved/rejected/needs_revision"),
    item_type: Optional[str] = Query(None, description="类型筛选：direction/dimension/opinion"),
    limit: Optional[int] = Query(100, description="返回数量限制"),
    db: Session = Depends(get_db)
):
    """获取审核队列列表，支持按状态和类型筛选"""
    query = db.query(models.ReviewQueue)
    if status:
        query = query.filter(models.ReviewQueue.status == status)
    if item_type:
        query = query.filter(models.ReviewQueue.item_type == item_type)
    items = query.order_by(models.ReviewQueue.created_at).limit(limit).all()
    return items


@router.patch("/{queue_id}", response_model=schemas.ReviewQueueResponse, summary="更新审核状态")
def update_review_item(queue_id: int, item_update: schemas.ReviewQueueUpdate, db: Session = Depends(get_db)):
    """更新审核项状态"""
    db_item = db.query(models.ReviewQueue).filter(models.ReviewQueue.id == queue_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Review queue item not found")

    update_data = item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)

    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/{queue_id}", status_code=204, summary="删除审核项")
def delete_review_item(queue_id: int, db: Session = Depends(get_db)):
    """删除审核项"""
    db_item = db.query(models.ReviewQueue).filter(models.ReviewQueue.id == queue_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Review queue item not found")

    db.delete(db_item)
    db.commit()
    return None


class ReviewQueueBatchCreate(BaseModel):
    items: List[schemas.ReviewQueueCreate]


class ReviewQueueBatchUpdate(BaseModel):
    ids: List[int]
    status: ReviewStatusEnum
    reviewer: Optional[str] = None
    comment: Optional[str] = None


@router.post("/batch", response_model=List[schemas.ReviewQueueResponse], summary="批量创建审核项")
def batch_create_review_items(batch: ReviewQueueBatchCreate, db: Session = Depends(get_db)):
    """批量创建多个审核项"""
    db_items = []
    for item in batch.items:
        db_item = models.ReviewQueue(
            item_type=item.item_type,
            item_id=item.item_id,
            action=item.action,
            payload=item.payload
        )
        db.add(db_item)
        db_items.append(db_item)
    db.commit()
    for item in db_items:
        db.refresh(item)
    return db_items


@router.patch("/batch", response_model=List[schemas.ReviewQueueResponse], summary="批量更新审核状态")
def batch_update_review_items(batch: ReviewQueueBatchUpdate, db: Session = Depends(get_db)):
    """批量更新多个审核项状态"""
    db_items = db.query(models.ReviewQueue).filter(
        models.ReviewQueue.id.in_(batch.ids)
    ).all()

    for db_item in db_items:
        db_item.status = batch.status
        if batch.reviewer:
            db_item.reviewer = batch.reviewer
        if batch.comment:
            db_item.comment = batch.comment

    db.commit()
    for item in db_items:
        db.refresh(item)
    return db_items
