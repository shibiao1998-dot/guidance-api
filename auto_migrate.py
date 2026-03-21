"""数据库自动迁移 - 应用启动时运行

在 main.py 启动时自动执行数据库迁移
"""
from sqlalchemy import text, inspect
import logging

logger = logging.getLogger(__name__)

TABLES_WITH_TENANT_FIELDS = [
    "bundles",
    "evidence_cards",
    "glossary",
    "directions",
    "dimensions",
    "opinions",
    "review_queue",
    "snapshots",
]

# 需要添加 identity_tags 字段的表
TABLES_WITH_IDENTITY_TAGS = [
    "dimensions",
    "opinions",
]

def column_exists(inspector, table_name, column_name):
    """检查列是否已存在"""
    try:
        columns = [col['name'] for col in inspector.get_columns(table_name)]
        return column_name in columns
    except Exception:
        return False

def run_migration(engine):
    """运行数据库迁移"""
    try:
        inspector = inspect(engine)

        # 检查是否是 PostgreSQL（Railway 环境）
        is_postgres = not str(engine.url).startswith('sqlite')

        for table in TABLES_WITH_TENANT_FIELDS:
            for column in ["user_id", "session_id"]:
                if not column_exists(inspector, table, column):
                    with engine.connect() as conn:
                        if is_postgres:
                            conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} VARCHAR(255)"))
                        else:
                            conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} VARCHAR(255)"))
                        conn.commit()
                    logger.info(f"Added column {table}.{column}")

        # 添加 identity_tags 字段（JSONB 类型）
        for table in TABLES_WITH_IDENTITY_TAGS:
            if not column_exists(inspector, table, "identity_tags"):
                with engine.connect() as conn:
                    if is_postgres:
                        conn.execute(text(f"ALTER TABLE {table} ADD COLUMN identity_tags JSONB DEFAULT '[]'::jsonb"))
                    else:
                        conn.execute(text(f"ALTER TABLE {table} ADD COLUMN identity_tags JSON"))
                    conn.commit()
                logger.info(f"Added column {table}.identity_tags")

        logger.info("Database migration completed")
    except Exception as e:
        logger.warning(f"Migration skipped or failed: {e}")
