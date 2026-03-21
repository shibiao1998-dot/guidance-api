"""Pydantic Schema 定义 - 用于请求/响应验证"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ReviewStatusEnum(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"


# ==================== Bundle ====================
class BundleBase(BaseModel):
    name: str = Field(..., description="材料包名称")
    description: Optional[str] = Field(None, description="描述")
    metadata_json: Optional[Dict[str, Any]] = Field(None, description="元数据")
    # 多租户隔离字段
    user_id: Optional[str] = Field(None, description="用户 ID")
    session_id: Optional[str] = Field(None, description="会话 ID")


class BundleCreate(BundleBase):
    pass


class BundleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None


class BundleResponse(BundleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== EvidenceCard ====================
class EvidenceCardBase(BaseModel):
    content: str = Field(..., description="证据内容")
    source_type: Optional[str] = Field("material", description="来源类型")
    source_ref: Optional[str] = Field(None, description="来源引用")
    tags: Optional[List[str]] = Field(None, description="标签列表")
    # 多租户隔离字段
    user_id: Optional[str] = Field(None, description="用户 ID")
    session_id: Optional[str] = Field(None, description="会话 ID")


class EvidenceCardCreate(EvidenceCardBase):
    bundle_id: int = Field(..., description="关联的材料包 ID")


class EvidenceCardResponse(EvidenceCardBase):
    id: int
    bundle_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Glossary ====================
class GlossaryTermBase(BaseModel):
    term: str = Field(..., description="术语名称")
    definition: str = Field(..., description="定义")
    category: Optional[str] = Field(None, description="分类")
    version: Optional[str] = Field("1.0.0", description="版本号")
    # 多租户隔离字段
    user_id: Optional[str] = Field(None, description="用户 ID")
    session_id: Optional[str] = Field(None, description="会话 ID")


class GlossaryTermCreate(GlossaryTermBase):
    pass


class GlossaryTermUpdate(BaseModel):
    definition: Optional[str] = None
    category: Optional[str] = None
    version: Optional[str] = None


class GlossaryTermResponse(GlossaryTermBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== Direction ====================
class DirectionBase(BaseModel):
    name: str = Field(..., description="方向名称")
    description: str = Field(..., description="方向描述")
    rationale: Optional[str] = Field(None, description="制定理由")
    sort_order: Optional[int] = Field(0, description="排序顺序")
    version: Optional[str] = Field("1.0.0", description="版本号")
    # 多租户隔离字段
    user_id: Optional[str] = Field(None, description="用户 ID")
    session_id: Optional[str] = Field(None, description="会话 ID")


class DirectionCreate(DirectionBase):
    pass


class DirectionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    rationale: Optional[str] = None
    sort_order: Optional[int] = None
    version: Optional[str] = None


class DirectionResponse(DirectionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== Dimension ====================
class DimensionBase(BaseModel):
    name: str = Field(..., description="维度名称")
    description: str = Field(..., description="维度描述")
    key_points: Optional[List[str]] = Field(None, description="关键点列表")
    sort_order: Optional[int] = Field(0, description="排序顺序")
    version: Optional[str] = Field("1.0.0", description="版本号")
    identity_tags: Optional[List[str]] = Field(default_factory=list, description="三重身份标签：platform, ecosystem, organization")
    # 多租户隔离字段
    user_id: Optional[str] = Field(None, description="用户 ID")
    session_id: Optional[str] = Field(None, description="会话 ID")


class DimensionCreate(DimensionBase):
    direction_id: int = Field(..., description="关联的方向 ID")


class DimensionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    key_points: Optional[List[str]] = None
    sort_order: Optional[int] = None
    version: Optional[str] = None


class DimensionResponse(DimensionBase):
    id: int
    direction_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== Opinion ====================
class EvidenceRefs(BaseModel):
    """观点证据引用结构"""
    opinion_type: str = Field(..., description="观点类型：goal|method|rule_positive|rule_negative|applied")
    tech_mode: Optional[str] = Field("na", description="技术模式：self_build|applied|na")
    confidence: Optional[str] = Field("high", description="置信度：high|moderate|low")
    source_type: Optional[str] = Field("material_extracted", description="来源类型：material_extracted|expert_supplemented")
    suggestion_source: Optional[str] = Field("na", description="AI 补充来源：internal_inference|external_knowledge|na")
    expected_action: Optional[str] = Field("na", description="期望动作：confirm|modify|supplement|ignore|na")


class OpinionBase(BaseModel):
    content: str = Field(..., description="观点内容")
    reasoning: Optional[str] = Field(None, description="推理依据")
    evidence_refs: Optional[EvidenceRefs] = Field(None, description="证据引用对象")
    sort_order: Optional[int] = Field(0, description="排序顺序")
    version: Optional[str] = Field("1.0.0", description="版本号")
    identity_tags: Optional[List[str]] = Field(default_factory=list, description="三重身份标签：platform, ecosystem, organization")
    # 多租户隔离字段
    user_id: Optional[str] = Field(None, description="用户 ID")
    session_id: Optional[str] = Field(None, description="会话 ID")


class OpinionCreate(OpinionBase):
    dimension_id: int = Field(..., description="关联的维度 ID")


class OpinionUpdate(BaseModel):
    content: Optional[str] = None
    reasoning: Optional[str] = None
    evidence_refs: Optional[List[int]] = None
    sort_order: Optional[int] = None
    version: Optional[str] = None


class OpinionResponse(OpinionBase):
    id: int
    dimension_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== ReviewQueue ====================
class ReviewQueueBase(BaseModel):
    item_type: str = Field(..., description="项目类型：direction/dimension/opinion")
    item_id: int = Field(..., description="项目 ID")
    action: str = Field(..., description="操作类型：create/update/delete")
    payload: Dict[str, Any] = Field(..., description="变更内容")
    # 多租户隔离字段
    user_id: Optional[str] = Field(None, description="用户 ID")
    session_id: Optional[str] = Field(None, description="会话 ID")


class ReviewQueueCreate(ReviewQueueBase):
    pass


class ReviewQueueUpdate(BaseModel):
    status: Optional[ReviewStatusEnum] = None
    reviewer: Optional[str] = None
    comment: Optional[str] = None


class ReviewQueueResponse(ReviewQueueBase):
    id: int
    status: ReviewStatusEnum
    reviewer: Optional[str] = None
    comment: Optional[str] = None
    created_at: datetime
    reviewed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== Snapshot ====================
class SnapshotBase(BaseModel):
    version: str = Field(..., description="版本号")
    guidance_doc: str = Field(..., description="完整文档 Markdown")
    guidance_contract: Dict[str, Any] = Field(..., description="结构化合同 JSON")
    change_log: Optional[str] = Field(None, description="变更日志")
    created_by: Optional[str] = Field(None, description="创建人")
    # 多租户隔离字段
    user_id: Optional[str] = Field(None, description="用户 ID")
    session_id: Optional[str] = Field(None, description="会话 ID")


class SnapshotCreate(SnapshotBase):
    pass


class SnapshotResponse(SnapshotBase):
    id: int
    created_at: datetime
    is_published: bool

    class Config:
        from_attributes = True


# ==================== Publish ====================
class PublishCreate(BaseModel):
    snapshot_id: int = Field(..., description="快照 ID")
    action: str = Field(..., description="操作：publish/unpublish")
    triggered_by: Optional[str] = Field(None, description="触发人")
    metadata_json: Optional[Dict[str, Any]] = Field(None, description="元数据")


class PublishResponse(BaseModel):
    id: int
    snapshot_id: int
    action: str
    created_at: datetime
    triggered_by: Optional[str] = None

    class Config:
        from_attributes = True


# ==================== Guidance (完整文档) ====================
class GuidanceDocument(BaseModel):
    """完整的指导文档结构（树状嵌套）"""
    directions: List["DirectionWithChildren"] = []


class DirectionWithChildren(BaseModel):
    """方向及其子维度和观点"""
    id: int
    name: str
    description: str
    rationale: Optional[str] = None
    sort_order: Optional[int] = 0
    version: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    dimensions: List["DimensionWithOpinions"] = []


class DimensionWithOpinions(BaseModel):
    """维度及其子观点"""
    id: int
    name: str
    description: str
    key_points: Optional[List[str]] = None
    sort_order: Optional[int] = 0
    version: Optional[str] = None
    identity_tags: Optional[List[str]] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    opinions: List[OpinionResponse] = []


class GuidanceContract(BaseModel):
    """结构化合同 - 用于 AI Agent 交互"""
    version: str
    created_at: datetime
    directions: List[DirectionResponse]
    dimensions: List[DimensionResponse]
    opinions: List[OpinionResponse]
    glossary: List[GlossaryTermResponse] = []
