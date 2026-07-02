"""
Pydantic 请求/响应模型定义。
"""
from pydantic import BaseModel, Field
from typing import Optional


# ── 请求模型 ──

class ParseRequest(BaseModel):
    input_text: str = Field(..., description="采购需求自然语言文本", min_length=1, max_length=5000)
    mode: Optional[str] = Field(default="llm", description="llm 或 mock")


class RiskCheckRequest(BaseModel):
    parsed_spec: dict = Field(..., description="结构化采购参数")
    selected_clauses: Optional[list[dict]] = Field(default=[], description="已选条款列表")


class GenerateRequest(BaseModel):
    parsed_spec: dict = Field(..., description="结构化采购参数")
    template_id: Optional[int] = Field(default=1, description="模板ID")
    selected_clauses: Optional[list[dict]] = Field(default=[], description="已选条款列表")


class TemplateCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    template_type: str = Field(..., description="tender / contract / risk_report")
    content: str = Field(..., min_length=1)
    variables: Optional[str] = Field(default="")


class ClauseCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    category: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)
    applicable_condition: Optional[str] = Field(default="")


# ── 响应模型 ──

class ParseResult(BaseModel):
    project_name: Optional[str] = None
    purchase_type: Optional[str] = None
    procurement_method: Optional[str] = None
    budget: Optional[float] = None
    delivery_period: Optional[str] = None
    qualification: list[str] = []
    technical_specs: list[str] = []
    evaluation_factors: list[str] = []
    payment_terms: Optional[str] = None
    acceptance_criteria: Optional[str] = None
    warranty_period: Optional[str] = None
    missing_fields: list[str] = []
    confidence: float = 0.0


class RiskItem(BaseModel):
    level: str
    type: str
    message: str
    suggestion: str


class RiskReport(BaseModel):
    overall_level: str
    risks: list[dict]


class TaskSummary(BaseModel):
    id: int
    project_name: str = ""
    status: str
    overall_level: str = ""
    created_at: str
    file_name: str = ""
