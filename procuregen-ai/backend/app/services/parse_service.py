"""
需求解析服务：调用 LLM Adapter 完成采购需求解析。
"""
from app.services.llm_adapter import llm_adapter
from app.models.schemas import ParseResult


def parse_requirement(input_text: str, mode: str = "llm") -> dict:
    """解析采购需求文本为结构化字段。"""
    result = llm_adapter.parse_requirement(input_text)

    # 用 Pydantic 模型规范化输出
    parsed = ParseResult(
        project_name=result.get("project_name"),
        purchase_type=result.get("purchase_type"),
        procurement_method=result.get("procurement_method"),
        budget=result.get("budget"),
        delivery_period=result.get("delivery_period"),
        qualification=result.get("qualification") or [],
        technical_specs=result.get("technical_specs") or [],
        evaluation_factors=result.get("evaluation_factors") or [],
        payment_terms=result.get("payment_terms"),
        acceptance_criteria=result.get("acceptance_criteria"),
        warranty_period=result.get("warranty_period"),
        missing_fields=result.get("missing_fields") or [],
        confidence=result.get("confidence", 0.0),
    )
    return parsed.model_dump()
