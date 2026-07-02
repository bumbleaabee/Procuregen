"""
风险预审路由：POST /api/risk-check
"""
from fastapi import APIRouter
from app.models.schemas import RiskCheckRequest
from app.services.risk_service import check_risks

router = APIRouter()


@router.post("/risk-check")
def risk_check_api(req: RiskCheckRequest):
    """执行合规风险预审。"""
    try:
        report = check_risks(req.parsed_spec, req.selected_clauses)
        return {"success": True, "data": report, "message": "风险预审完成"}
    except Exception as e:
        return {"success": False, "data": None, "message": f"风险预审失败: {str(e)}"}
