"""管理端点 - 数据库管理操作"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text, inspect
import logging

import models
from database import get_db, engine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["admin"])


@router.delete("/clear-all", summary="清空所有数据")
def clear_all_data(db: Session = Depends(get_db)):
    """
    清空所有表数据（用于测试/重置）

    注意：
    1. 只删除数据，不删除表结构
    2. 会级联删除所有关联数据
    3. 生产环境慎用！
    """
    try:
        # 按顺序删除（避免外键约束问题）
        # 1. 先删除子表
        db.query(models.PublishLog).delete()
        db.query(models.ReviewQueue).delete()
        db.query(models.Opinion).delete()
        db.query(models.Dimension).delete()
        db.query(models.EvidenceCard).delete()

        # 2. 再删除主表
        db.query(models.Snapshot).delete()
        db.query(models.GlossaryTerm).delete()
        db.query(models.Direction).delete()
        db.query(models.Bundle).delete()

        db.commit()

        return {
            "status": "success",
            "message": "所有数据已清空"
        }
    except Exception as e:
        db.rollback()
        logger.error(f"清空数据失败：{e}")
        raise HTTPException(status_code=500, detail=f"清空数据失败：{str(e)}")


@router.delete("/clear-session/{session_id}", summary="清空指定会话数据")
def clear_session_data(session_id: str, db: Session = Depends(get_db)):
    """清空指定会话的所有数据"""
    try:
        # 删除该会话的所有数据
        bundles = db.query(models.Bundle).filter(models.Bundle.session_id == session_id).all()
        bundle_ids = [b.id for b in bundles]

        if bundle_ids:
            # 删除关联数据
            db.query(models.EvidenceCard).filter(models.EvidenceCard.bundle_id.in_(bundle_ids)).delete(synchronize_session=False)
            db.query(models.Bundle).filter(models.Bundle.session_id == session_id).delete()

        db.query(models.ReviewQueue).filter(models.ReviewQueue.session_id == session_id).delete()
        db.query(models.GlossaryTerm).filter(models.GlossaryTerm.session_id == session_id).delete()
        db.query(models.Direction).filter(models.Direction.session_id == session_id).delete()
        db.query(models.Dimension).filter(models.Dimension.session_id == session_id).delete()
        db.query(models.Opinion).filter(models.Opinion.session_id == session_id).delete()
        db.query(models.Snapshot).filter(models.Snapshot.session_id == session_id).delete()

        db.commit()

        return {
            "status": "success",
            "message": f"会话 {session_id} 的数据已清空"
        }
    except Exception as e:
        db.rollback()
        logger.error(f"清空会话数据失败：{e}")
        raise HTTPException(status_code=500, detail=f"清空数据失败：{str(e)}")


@router.delete("/clear-user/{user_id}", summary="清空指定用户数据")
def clear_user_data(user_id: str, db: Session = Depends(get_db)):
    """清空指定用户的所有数据"""
    try:
        bundles = db.query(models.Bundle).filter(models.Bundle.user_id == user_id).all()
        bundle_ids = [b.id for b in bundles]

        if bundle_ids:
            db.query(models.EvidenceCard).filter(models.EvidenceCard.bundle_id.in_(bundle_ids)).delete(synchronize_session=False)
            db.query(models.Bundle).filter(models.Bundle.user_id == user_id).delete()

        db.query(models.ReviewQueue).filter(models.ReviewQueue.user_id == user_id).delete()
        db.query(models.GlossaryTerm).filter(models.GlossaryTerm.user_id == user_id).delete()
        db.query(models.Direction).filter(models.Direction.user_id == user_id).delete()
        db.query(models.Dimension).filter(models.Dimension.user_id == user_id).delete()
        db.query(models.Opinion).filter(models.Opinion.user_id == user_id).delete()
        db.query(models.Snapshot).filter(models.Snapshot.user_id == user_id).delete()

        db.commit()

        return {
            "status": "success",
            "message": f"用户 {user_id} 的数据已清空"
        }
    except Exception as e:
        db.rollback()
        logger.error(f"清空用户数据失败：{e}")
        raise HTTPException(status_code=500, detail=f"清空数据失败：{str(e)}")


@router.get("/stats", summary="查看数据统计")
def get_stats(db: Session = Depends(get_db)):
    """查看各表数据量"""
    return {
        "bundles": db.query(models.Bundle).count(),
        "evidence_cards": db.query(models.EvidenceCard).count(),
        "glossary": db.query(models.GlossaryTerm).count(),
        "directions": db.query(models.Direction).count(),
        "dimensions": db.query(models.Dimension).count(),
        "opinions": db.query(models.Opinion).count(),
        "review_queue": db.query(models.ReviewQueue).count(),
        "snapshots": db.query(models.Snapshot).count(),
    }


@router.post("/migrate", summary="执行数据库迁移")
def run_migration_endpoint(db: Session = Depends(get_db)):
    """
    手动触发数据库迁移（添加 identity_tags 字段）

    用于在应用启动时自动迁移失败时手动执行
    """
    try:
        inspector = inspect(engine)
        is_postgres = not str(engine.url).startswith('sqlite')

        results = {"migrated": [], "skipped": [], "errors": []}

        # 为 dimensions 和 opinions 表添加 identity_tags 字段
        for table in ["dimensions", "opinions"]:
            try:
                columns = [col['name'] for col in inspector.get_columns(table)]
                if "identity_tags" in columns:
                    results["skipped"].append(f"{table}.identity_tags 已存在")
                else:
                    with engine.connect() as conn:
                        if is_postgres:
                            conn.execute(text(f"ALTER TABLE {table} ADD COLUMN identity_tags JSONB DEFAULT '[]'::jsonb"))
                        else:
                            conn.execute(text(f"ALTER TABLE {table} ADD COLUMN identity_tags JSON"))
                        conn.commit()
                    results["migrated"].append(f"{table}.identity_tags 已添加")
            except Exception as e:
                results["errors"].append(f"{table}: {str(e)}")

        return {
            "status": "success",
            "message": "迁移完成",
            "details": results
        }
    except Exception as e:
        logger.error(f"迁移失败：{e}")
        raise HTTPException(status_code=500, detail=f"迁移失败：{str(e)}")
