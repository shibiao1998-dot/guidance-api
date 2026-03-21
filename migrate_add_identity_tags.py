"""数据库迁移脚本 - 为 dimensions 和 opinions 表添加 identity_tags 字段"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "guidance.db"


def migrate():
    """执行迁移"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 为 dimensions 表添加 identity_tags 字段
        print("Adding identity_tags column to dimensions table...")
        cursor.execute("""
            ALTER TABLE dimensions ADD COLUMN identity_tags JSON
        """)
        print("[OK] dimensions.identity_tags added")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("[SKIP] dimensions.identity_tags already exists")
        else:
            raise

    try:
        # 为 opinions 表添加 identity_tags 字段
        print("Adding identity_tags column to opinions table...")
        cursor.execute("""
            ALTER TABLE opinions ADD COLUMN identity_tags JSON
        """)
        print("[OK] opinions.identity_tags added")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("[SKIP] opinions.identity_tags already exists")
        else:
            raise

    conn.commit()
    print("\n[OK] Migration completed successfully!")


if __name__ == "__main__":
    migrate()
