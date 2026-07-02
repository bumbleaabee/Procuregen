"""
文档生成与任务管理路由。
"""
import json
from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.models.schemas import GenerateRequest
from app.services.docx_service import render_document, export_to_docx
from app.services.clause_service import recommend_clauses
from app.database import get_connection

router = APIRouter()


@router.post("/generate")
def generate_document(req: GenerateRequest):
    """生成招标文件 Word 文档。"""
    try:
        # 1. 条款推荐
        clauses = recommend_clauses(req.parsed_spec)
        if req.selected_clauses:
            clauses = req.selected_clauses

        # 2. 风险报告（从 parsed_spec 中提取或重新计算）
        risk_report = req.parsed_spec.get("_risk_report", {"overall_level": "low", "risks": []})

        # 3. 渲染模板
        rendered = render_document(req.parsed_spec, clauses, risk_report, req.template_id or 1)

        # 4. 导出 Word
        project_name = req.parsed_spec.get("project_name", "采购文件")
        filepath, filename = export_to_docx(rendered, project_name)

        # 5. 保存任务记录
        conn = get_connection()
        cursor = conn.execute(
            "INSERT INTO generation_tasks (input_text, parsed_spec, selected_clauses, risk_report, file_path, file_name, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                req.parsed_spec.get("_input_text", ""),
                json.dumps(req.parsed_spec, ensure_ascii=False),
                json.dumps(clauses, ensure_ascii=False),
                json.dumps(risk_report, ensure_ascii=False),
                filepath,
                filename,
                "completed"
            )
        )
        task_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return {
            "success": True,
            "data": {
                "task_id": task_id,
                "file_name": filename,
                "clauses": clauses,
                "preview": rendered[:2000]
            },
            "message": "文档生成成功"
        }
    except Exception as e:
        return {"success": False, "data": None, "message": f"文档生成失败: {str(e)}"}


@router.get("/tasks")
def list_tasks(page: int = 1, size: int = 20, keyword: str = None):
    """获取历史生成任务列表，支持关键词搜索。"""
    try:
        conn = get_connection()
        offset = (page - 1) * size

        if keyword:
            search = f"%{keyword}%"
            count_row = conn.execute(
                "SELECT COUNT(*) FROM generation_tasks WHERE input_text LIKE ? OR parsed_spec LIKE ?",
                (search, search)
            ).fetchone()
            total = count_row[0]
            rows = conn.execute(
                "SELECT id, input_text, parsed_spec, risk_report, file_path, file_name, status, created_at FROM generation_tasks WHERE input_text LIKE ? OR parsed_spec LIKE ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (search, search, size, offset)
            ).fetchall()
        else:
            count_row = conn.execute("SELECT COUNT(*) FROM generation_tasks").fetchone()
            total = count_row[0]
            rows = conn.execute(
                "SELECT id, input_text, parsed_spec, risk_report, file_path, file_name, status, created_at FROM generation_tasks ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (size, offset)
            ).fetchall()
        conn.close()

        tasks = []
        for r in rows:
            task = dict(r)
            # 提取项目名称
            try:
                spec = json.loads(task.get("parsed_spec", "{}"))
                task["project_name"] = spec.get("project_name", "")
            except Exception:
                task["project_name"] = ""
            # 提取风险等级
            try:
                risk = json.loads(task.get("risk_report", "{}"))
                task["overall_level"] = risk.get("overall_level", "")
            except Exception:
                task["overall_level"] = ""
            tasks.append(task)

        return {"success": True, "data": {"items": tasks, "total": total}, "message": "获取历史记录成功"}
    except Exception as e:
        return {"success": False, "data": {"items": [], "total": 0}, "message": str(e)}


@router.get("/tasks/{task_id}")
def get_task(task_id: int):
    """获取单个任务详情。"""
    try:
        conn = get_connection()
        row = conn.execute("SELECT * FROM generation_tasks WHERE id = ?", (task_id,)).fetchone()
        conn.close()
        if not row:
            return {"success": False, "data": None, "message": "任务不存在"}
        return {"success": True, "data": dict(row), "message": "获取任务详情成功"}
    except Exception as e:
        return {"success": False, "data": None, "message": str(e)}


@router.get("/export/{task_id}")
def export_file(task_id: int):
    """下载生成的 Word 文件。"""
    try:
        conn = get_connection()
        row = conn.execute("SELECT file_path, file_name FROM generation_tasks WHERE id = ?", (task_id,)).fetchone()
        conn.close()
        if not row or not row["file_path"]:
            return {"success": False, "data": None, "message": "文件不存在"}

        filepath = row["file_path"]
        filename = row["file_name"]
        return FileResponse(
            path=filepath,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        return {"success": False, "data": None, "message": str(e)}


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """删除历史任务及关联文件。"""
    try:
        conn = get_connection()
        row = conn.execute("SELECT file_path FROM generation_tasks WHERE id = ?", (task_id,)).fetchone()
        if row and row["file_path"]:
            import os
            if os.path.exists(row["file_path"]):
                os.remove(row["file_path"])
        conn.execute("DELETE FROM generation_tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        return {"success": True, "data": None, "message": "任务已删除"}
    except Exception as e:
        return {"success": False, "data": None, "message": str(e)}
