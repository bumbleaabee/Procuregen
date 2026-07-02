"""
条款推荐服务：规则优先 + 大模型解释。
"""
from app.database import get_connection
from app.services.llm_adapter import llm_adapter


def get_all_clauses(category: str = None) -> list[dict]:
    """获取条款列表，可按类别筛选。"""
    conn = get_connection()
    if category:
        rows = conn.execute("SELECT * FROM clauses WHERE category = ? ORDER BY id", (category,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM clauses ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_clause_by_id(clause_id: int) -> dict:
    conn = get_connection()
    row = conn.execute("SELECT * FROM clauses WHERE id = ?", (clause_id,)).fetchone()
    conn.close()
    return dict(row) if row else {}


def create_clause(title: str, category: str, content: str, applicable_condition: str = "") -> int:
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO clauses (title, category, content, applicable_condition) VALUES (?, ?, ?, ?)",
        (title, category, content, applicable_condition)
    )
    conn.commit()
    clause_id = cursor.lastrowid
    conn.close()
    return clause_id


def delete_clause(clause_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM clauses WHERE id = ?", (clause_id,))
    conn.commit()
    conn.close()


def recommend_clauses(parsed_spec: dict) -> list[dict]:
    """
    条款推荐：规则优先匹配 + 大模型生成推荐理由。
    """
    # 1. 规则优先：根据采购类型、预算等硬匹配
    all_clauses = get_all_clauses()
    matched = []
    purchase_type = (parsed_spec.get("purchase_type") or "").strip()
    budget = parsed_spec.get("budget") or 0
    tech_specs = parsed_spec.get("technical_specs") or []

    for clause in all_clauses:
        condition = (clause.get("applicable_condition") or "").strip()
        if not condition:
            continue
        # 简单规则匹配
        if _match_condition(condition, purchase_type, budget, tech_specs):
            matched.append({
                "clause_id": clause["id"],
                "title": clause["title"],
                "content": clause["content"],
                "reason": condition,
                "risk_level": "low"
            })

    # 2. 大模型补充推荐理由（可选，Mock 模式下跳过）
    if matched and not llm_adapter.mode == "mock":
        try:
            ai_reasons = llm_adapter.recommend_clauses(parsed_spec, matched)
            if isinstance(ai_reasons, list):
                reason_map = {item.get("clause_id"): item.get("reason", "") for item in ai_reasons}
                for m in matched:
                    if m["clause_id"] in reason_map and reason_map[m["clause_id"]]:
                        m["reason"] = reason_map[m["clause_id"]]
        except Exception:
            pass

    return matched


def _match_condition(condition: str, purchase_type: str, budget: float, tech_specs: list[str]) -> bool:
    """规则条件匹配引擎。"""
    purchase_lower = purchase_type.lower()
    tech_text = " ".join(tech_specs).lower() if tech_specs else ""

    conditions = [c.strip() for c in condition.replace("，", ",").split(",")]

    for cond in conditions:
        cond_lower = cond.lower()
        # 采购类型匹配
        if cond in ("货物", "服务", "工程") and cond in purchase_type:
            return True
        # 预算较高：>=50万
        if cond in ("预算较高", "高预算") and isinstance(budget, (int, float)) and budget >= 500000:
            return True
        # 软件 / 信息化相关
        if cond in ("软件", "信息化", "数据安全") and any(
            kw in tech_text for kw in ["软件", "系统", "平台", "数据", "信息化", "ai", "gpu", "服务器"]
        ):
            return True
        # 交付周期紧张
        if cond == "交付周期紧张":
            return True
        # 通用条款：始终匹配
        if cond == "通用":
            return True

    return False
