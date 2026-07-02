"""
模板与条款管理路由（含 CRUD）。
"""
from fastapi import APIRouter
from app.models.schemas import TemplateCreateRequest, ClauseCreateRequest
from app.services.docx_service import get_all_templates, get_template_by_id, create_template, delete_template
from app.services.clause_service import get_all_clauses, get_clause_by_id, create_clause, delete_clause
from app.database import get_connection

router = APIRouter()


# ── 模板 CRUD ──

@router.get("/templates")
def list_templates(template_type: str = None):
    try:
        data = get_all_templates(template_type)
        return {"success": True, "data": data, "message": "获取模板列表成功"}
    except Exception as e:
        return {"success": False, "data": [], "message": str(e)}


@router.get("/templates/{template_id}")
def get_template(template_id: int):
    try:
        data = get_template_by_id(template_id)
        return {"success": True, "data": data, "message": "获取模板成功"}
    except Exception as e:
        return {"success": False, "data": None, "message": str(e)}


@router.post("/templates")
def add_template(req: TemplateCreateRequest):
    try:
        tid = create_template(req.name, req.template_type, req.content, req.variables)
        return {"success": True, "data": {"id": tid}, "message": "模板创建成功"}
    except Exception as e:
        return {"success": False, "data": None, "message": str(e)}


@router.put("/templates/{template_id}")
def update_template(template_id: int, req: TemplateCreateRequest):
    try:
        conn = get_connection()
        conn.execute(
            "UPDATE templates SET name=?, template_type=?, content=?, variables=? WHERE id=?",
            (req.name, req.template_type, req.content, req.variables, template_id)
        )
        conn.commit()
        conn.close()
        return {"success": True, "data": None, "message": "模板更新成功"}
    except Exception as e:
        return {"success": False, "data": None, "message": str(e)}


@router.delete("/templates/{template_id}")
def remove_template(template_id: int):
    try:
        delete_template(template_id)
        return {"success": True, "data": None, "message": "模板已删除"}
    except Exception as e:
        return {"success": False, "data": None, "message": str(e)}


# ── 条款 CRUD ──

@router.get("/clauses")
def list_clauses(category: str = None):
    try:
        data = get_all_clauses(category)
        return {"success": True, "data": data, "message": "获取条款列表成功"}
    except Exception as e:
        return {"success": False, "data": [], "message": str(e)}


@router.get("/clauses/{clause_id}")
def get_clause(clause_id: int):
    try:
        data = get_clause_by_id(clause_id)
        return {"success": True, "data": data, "message": "获取条款成功"}
    except Exception as e:
        return {"success": False, "data": None, "message": str(e)}


@router.post("/clauses")
def add_clause(req: ClauseCreateRequest):
    try:
        cid = create_clause(req.title, req.category, req.content, req.applicable_condition)
        return {"success": True, "data": {"id": cid}, "message": "条款创建成功"}
    except Exception as e:
        return {"success": False, "data": None, "message": str(e)}


@router.put("/clauses/{clause_id}")
def update_clause(clause_id: int, req: ClauseCreateRequest):
    try:
        conn = get_connection()
        conn.execute(
            "UPDATE clauses SET title=?, category=?, content=?, applicable_condition=? WHERE id=?",
            (req.title, req.category, req.content, req.applicable_condition, clause_id)
        )
        conn.commit()
        conn.close()
        return {"success": True, "data": None, "message": "条款更新成功"}
    except Exception as e:
        return {"success": False, "data": None, "message": str(e)}


@router.delete("/clauses/{clause_id}")
def remove_clause(clause_id: int):
    try:
        delete_clause(clause_id)
        return {"success": True, "data": None, "message": "条款已删除"}
    except Exception as e:
        return {"success": False, "data": None, "message": str(e)}
