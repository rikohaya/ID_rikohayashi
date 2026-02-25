from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MessageCreate(BaseModel):
    content: str
    conversation_id: Optional[int] = None


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime


class ConversationCreate(BaseModel):
    title: Optional[str] = "新しいチャット"


class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime


class ConversationWithMessages(ConversationResponse):
    messages: list[MessageResponse] = []


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None


class ChatResponse(BaseModel):
    conversation_id: int
    user_message: MessageResponse
    assistant_message: MessageResponse


# Media Plan Models
class MediaPlanCalculateRequest(BaseModel):
    age_group: str
    gender: str
    media: str
    reach_rate: float
    frequency: int = 2
    cpm: Optional[float] = None


class MediaPlanCalculateResponse(BaseModel):
    target_population: int
    reach_count: int
    total_impressions: int
    estimated_cost: int
    cpm_used: float


class MediaPlanReverseRequest(BaseModel):
    age_group: str
    gender: str
    media: str
    budget: int
    frequency: int = 2
    cpm: Optional[float] = None


class MediaPlanReverseResponse(BaseModel):
    target_population: int
    max_reach: int
    max_impressions: int
    reach_rate_achievable: float
    cpm_used: float


class MediaPlanOptionsResponse(BaseModel):
    age_groups: list[str]
    genders: list[str]
    media_types: list[str]
    default_cpm: dict[str, int]


# AI Target Estimation Models
class TargetEstimateRequest(BaseModel):
    target_description: str
    media: str


class TargetEstimateResponse(BaseModel):
    target_description: str
    estimated_population: int
    reasoning: str
    confidence: str


# Custom Target Calculation Models
class CustomMediaPlanCalculateRequest(BaseModel):
    target_description: str
    target_population: int
    media: str
    reach_rate: float
    frequency: int = 2
    cpm: Optional[float] = None


class CustomMediaPlanReverseRequest(BaseModel):
    target_description: str
    target_population: int
    media: str
    budget: int
    frequency: int = 2
    cpm: Optional[float] = None


# ターゲット → 広告費見積（「刺すためにかかる費用」一括算出）
class TargetAdCostRequest(BaseModel):
    target_description: str
    media: Optional[str] = None  # 未指定時は全媒体で試算
    reach_rate: float = 50.0
    frequency: int = 2
    cpm: Optional[float] = None


class TargetAdCostPerMedia(BaseModel):
    media: str
    estimated_cost: int
    reach_count: int
    total_impressions: int
    target_population: int
    cpm_used: float


class TargetAdCostResponse(BaseModel):
    target_description: str
    estimated_population: int
    reasoning: str
    confidence: str
    per_media: list[TargetAdCostPerMedia]
    summary_message: str
