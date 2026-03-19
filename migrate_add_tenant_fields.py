"""数据库迁移脚本 - 添加 user_id 和 session_id 字段

使用方法：
1. 确保数据库连接正常
2. 运行：python migrate_add_tenant_fields.py
3. 迁移完成后重启服务
"""
from sqlalchemy import create_engine, text, inspect
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./guidance.db")

# 创建数据库引擎
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

# 需要添加 tenant 字段的表
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

def column_exists(table_name, column_name):
    """检查列是否已存在"""
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def add_column_if_not_exists(table_name, column_name, column_type, default=None):
    """如果列不存在则添加"""
    if column_exists(table_name, column_name):
        print(f"  [OK] 列 {table_name}.{column_name} 已存在")
        return

    with engine.connect() as conn:
        if DATABASE_URL.startswith("sqlite"):
            # SQLite 添加列语法
            if default is not None:
                conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type} DEFAULT '{default}'"))
            else:
                conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"))
        else:
            # PostgreSQL 添加列语法
            if default is not None:
                conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type} DEFAULT '{default}'"))
            else:
                conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"))
        conn.commit()
    print(f"  [OK] 已添加列 {table_name}.{column_name}")

def main():
    print("=" * 60)
    print("开始迁移：添加多租户隔离字段")
    print("=" * 60)

    for table in TABLES_WITH_TENANT_FIELDS:
        print(f"\n处理表：{table}")
        add_column_if_not_exists(table, "user_id", "VARCHAR(255)")
        add_column_if_not_exists(table, "session_id", "VARCHAR(255)")

    print("\n" + "=" * 60)
    print("迁移完成！")
    print("=" * 60)
    print("\n下一步：")
    print("1. 重启 Railway 服务（代码已自动部署）")
    print("2. 在 Dify 中传递 user_id 和 session_id 参数")

if __name__ == "__main__":
    main()
