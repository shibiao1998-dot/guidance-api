"""数据模型定义"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from database import Base


class MaterialType(str, enum.Enum):
    """材料类型"""
    DOCUMENT = "document"
    TEXT = "text"
    URL = "url"


class ReviewStatus(str, enum.Enum):
    """审核状态"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"


class Bundle(Base):
    """材料包 - 存储用户上传的原始材料"""
    __tablename__ = "bundles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    metadata_json = Column(JSON, nullable=True)  # 额外元数据
    # 多租户隔离字段
    user_id = Column(String, index=True, nullable=True)  # 用户 ID
    session_id = Column(String, index=True, nullable=True)  # 会话 ID

    # 关联证据卡
    evidence_cards = relationship("EvidenceCard", back_populates="bundle", cascade="all, delete-orphan")


class EvidenceCard(Base):
    """证据卡 - 存储从材料中提取的证据片段"""
    __tablename__ = "evidence_cards"

    id = Column(Integer, primary_key=True, index=True)
    bundle_id = Column(Integer, ForeignKey("bundles.id"), nullable=False)
    content = Column(Text, nullable=False)  # 证据内容
    source_type = Column(String, default="material")  # 来源类型
    source_ref = Column(String, nullable=True)  # 来源引用（如页码、段落号）
    tags = Column(JSON, nullable=True)  # 标签列表
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # 多租户隔离字段（冗余存储，便于独立查询）
    user_id = Column(String, index=True, nullable=True)  # 用户 ID
    session_id = Column(String, index=True, nullable=True)  # 会话 ID

    # 关联材料包
    bundle = relationship("Bundle", back_populates="evidence_cards")


class GlossaryTerm(Base):
    """术语表 - 存储企业术语定义"""
    __tablename__ = "glossary"

    id = Column(Integer, primary_key=True, index=True)
    term = Column(String, index=True, nullable=False)  # 术语名称
    definition = Column(Text, nullable=False)  # 定义
    category = Column(String, nullable=True)  # 分类
    version = Column(String, default="1.0.0")  # 版本号
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # 多租户隔离字段
    user_id = Column(String, index=True, nullable=True)  # 用户 ID
    session_id = Column(String, index=True, nullable=True)  # 会话 ID


class Direction(Base):
    """方向 - 企业顶层指导的一级结构"""
    __tablename__ = "directions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # 方向名称
    description = Column(Text, nullable=False)  # 方向描述
    rationale = Column(Text, nullable=True)  # 制定理由
    sort_order = Column(Integer, default=0)  # 排序顺序
    version = Column(String, default="1.0.0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # 多租户隔离字段
    user_id = Column(String, index=True, nullable=True)  # 用户 ID
    session_id = Column(String, index=True, nullable=True)  # 会话 ID

    # 关联维度
    dimensions = relationship("Dimension", back_populates="direction", cascade="all, delete-orphan")


class Dimension(Base):
    """维度 - 企业顶层指导的二级结构"""
    __tablename__ = "dimensions"

    id = Column(Integer, primary_key=True, index=True)
    direction_id = Column(Integer, ForeignKey("directions.id"), nullable=False)
    name = Column(String, nullable=False)  # 维度名称
    description = Column(Text, nullable=False)  # 维度描述
    key_points = Column(JSON, nullable=True)  # 关键点列表
    sort_order = Column(Integer, default=0)
    version = Column(String, default="1.0.0")
    identity_tags = Column(JSON, nullable=True, default=list)  # 三重身份标签：platform, ecosystem, organization
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # 多租户隔离字段（冗余存储，便于独立查询）
    user_id = Column(String, index=True, nullable=True)  # 用户 ID
    session_id = Column(String, index=True, nullable=True)  # 会话 ID

    # 关联方向
    direction = relationship("Direction", back_populates="dimensions")
    # 关联观点
    opinions = relationship("Opinion", back_populates="dimension", cascade="all, delete-orphan")


class Opinion(Base):
    """观点 - 企业顶层指导的三级结构"""
    __tablename__ = "opinions"

    id = Column(Integer, primary_key=True, index=True)
    dimension_id = Column(Integer, ForeignKey("dimensions.id"), nullable=False)
    content = Column(Text, nullable=False)  # 观点内容
    reasoning = Column(Text, nullable=True)  # 推理依据
    evidence_refs = Column(JSON, nullable=True)  # 证据引用（包含 opinion_type, tech_mode, confidence 等）
    sort_order = Column(Integer, default=0)
    version = Column(String, default="1.0.0")
    identity_tags = Column(JSON, nullable=True, default=list)  # 三重身份标签：platform, ecosystem, organization
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # 多租户隔离字段（冗余存储，便于独立查询）
    user_id = Column(String, index=True, nullable=True)  # 用户 ID
    session_id = Column(String, index=True, nullable=True)  # 会话 ID

    # 关联维度
    dimension = relationship("Dimension", back_populates="opinions")


class ReviewQueue(Base):
    """审核队列 - 存储待审核的项目"""
    __tablename__ = "review_queue"

    id = Column(Integer, primary_key=True, index=True)
    item_type = Column(String, nullable=False)  # 项目类型：direction/dimension/opinion
    item_id = Column(Integer, nullable=False)  # 项目 ID
    action = Column(String, nullable=False)  # 操作类型：create/update/delete
    payload = Column(JSON, nullable=False)  # 变更内容
    status = Column(SQLEnum(ReviewStatus), default=ReviewStatus.PENDING)
    reviewer = Column(String, nullable=True)  # 审核人
    comment = Column(Text, nullable=True)  # 审核意见
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    # 多租户隔离字段
    user_id = Column(String, index=True, nullable=True)  # 用户 ID
    session_id = Column(String, index=True, nullable=True)  # 会话 ID


class Snapshot(Base):
    """快照 - 存储发布的文档快照"""
    __tablename__ = "snapshots"

    id = Column(Integer, primary_key=True, index=True)
    version = Column(String, nullable=False)
    guidance_doc = Column(Text, nullable=False)  # 完整文档 Markdown
    guidance_contract = Column(JSON, nullable=False)  # 结构化合同 JSON
    change_log = Column(Text, nullable=True)  # 变更日志
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, nullable=True)
    is_published = Column(Integer, default=0)  # 是否已发布
    # 多租户隔离字段
    user_id = Column(String, index=True, nullable=True)  # 用户 ID
    session_id = Column(String, index=True, nullable=True)  # 会话 ID


class PublishLog(Base):
    """发布日志 - 记录发布历史"""
    __tablename__ = "publish_logs"

    id = Column(Integer, primary_key=True, index=True)
    snapshot_id = Column(Integer, ForeignKey("snapshots.id"), nullable=False)
    action = Column(String, nullable=False)  # publish/unpublish
    triggered_by = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    metadata_json = Column(JSON, nullable=True)

    snapshot = relationship("Snapshot")
