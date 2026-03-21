"""PostgreSQL 数据库迁移脚本 - 为 dimensions 和 opinions 表添加 identity_tags 字段

使用方法：
1. 确保 Railway PostgreSQL 已连接（DATABASE_URL 环境变量已设置）
2. 在 Railway 上执行：python migrate_postgres_identity_tags.py
3. 重启服务

"""
from sqlalchemy import create_engine, text, inspect
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("错误：未设置 DATABASE_URL 环境变量")
    print("请确保 Railway PostgreSQL 已连接")
    exit(1)

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

def column_exists(table_name, column_name):
    """检查列是否已存在"""
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def add_column_if_not_exists(table_name, column_name, column_type, default="'[]'::jsonb"):
    """如果列不存在则添加"""
    if column_exists(table_name, column_name):
        print(f"  [OK] 列 {table_name}.{column_name} 已存在")
        return

    with engine.connect() as conn:
        conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type} DEFAULT {default}"))
        conn.commit()
    print(f"  [OK] 已添加列 {table_name}.{column_name}")

def main():
    print("=" * 60)
    print("开始迁移：添加 identity_tags 字段")
    print("=" * 60)

    print("\n处理表：dimensions")
    add_column_if_not_exists("dimensions", "identity_tags", "JSONB", "'[]'::jsonb")

    print("\n处理表：opinions")
    add_column_if_not_exists("opinions", "identity_tags", "JSONB", "'[]'::jsonb")

    print("\n" + "=" * 60)
    print("迁移完成！")
    print("=" * 60)
    print("\n下一步：")
    print("1. 重启 Railway 服务（代码已自动部署）")
    print("2. 验证 API 返回包含新字段")

if __name__ == "__main__":
    main()
