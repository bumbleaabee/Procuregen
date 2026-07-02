"""
需求解析路由：POST /api/parse
"""
from fastapi import APIRouter
from app.models.schemas import ParseRequest
from app.services.parse_service import parse_requirement

router = APIRouter()


@router.post("/parse")
def parse_requirement_api(req: ParseRequest):
    """解析采购需求为结构化 JSON。"""
    try:
        result = parse_requirement(req.input_text, req.mode)
        return {"success": True, "data": result, "message": "解析成功"}
    except Exception as e:
        return {"success": False, "data": None, "message": f"解析失败: {str(e)}"}
