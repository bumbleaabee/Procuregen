"""
需求解析路由：POST /api/parse  + GET /api/parse-stream (SSE)
"""
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from app.models.schemas import ParseRequest
from app.services.parse_service import parse_requirement
from app.services.llm_adapter import llm_adapter
import json

router = APIRouter()


@router.post("/parse")
def parse_requirement_api(req: ParseRequest):
    """解析采购需求为结构化 JSON。"""
    try:
        result = parse_requirement(req.input_text, req.mode)
        return {"success": True, "data": result, "message": "解析成功"}
    except Exception as e:
        return {"success": False, "data": None, "message": f"解析失败: {str(e)}"}


@router.get("/parse-stream")
async def parse_stream(input_text: str = ""):
    """SSE 流式解析采购需求，逐 token 推送。"""
    if not input_text.strip():
        return StreamingResponse(
            iter(["data: " + json.dumps({"error": "输入为空"}, ensure_ascii=False) + "\n\n"]),
            media_type="text/event-stream"
        )

    system_prompt = """你是采购文件生成助手。请从用户输入的采购需求中抽取结构化字段。
要求：只输出 JSON，不要输出解释性文字。字段缺失时填写 null，并在 missing_fields 中列出。
输出 JSON 字段：project_name, purchase_type, procurement_method, budget, delivery_period,
qualification, technical_specs, evaluation_factors, payment_terms,
acceptance_criteria, warranty_period, missing_fields, confidence。"""

    def generate():
        full_text = ""
        for token in llm_adapter.stream_llm(system_prompt, f"用户需求：{input_text}"):
            full_text += token
            yield f"data: {json.dumps({'token': token, 'full': full_text}, ensure_ascii=False)}\n\n"
        yield f"data: {json.dumps({'done': True, 'full': full_text}, ensure_ascii=False)}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
