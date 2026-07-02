"""
风险预审服务：规则引擎 + 大模型解释。
"""
from app.database import get_connection
from app.services.llm_adapter import llm_adapter


def get_all_risk_rules() -> list[dict]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM risk_rules ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def check_risks(parsed_spec: dict, selected_clauses: list[dict] = None) -> dict:
    """
    执行风险规则校验，输出风险报告。
    先走规则引擎做硬匹配，再交由大模型生成可读解释。
    """
    rules = get_all_risk_rules()
    triggered = []

    for rule in rules:
        condition = rule["condition_expr"]
        if evaluate_condition(condition, parsed_spec, selected_clauses or []):
            # 替换消息模板中的变量
            message = rule["message_template"]
            for key, val in parsed_spec.items():
                if val is None or val == "" or val == []:
                    message = message.replace(f"{{{key}}}", "（缺失）")
                elif isinstance(val, list):
                    message = message.replace(f"{{{key}}}", "、".join(str(v) for v in val))
                else:
                    message = message.replace(f"{{{key}}}", str(val))

            triggered.append({
                "rule_name": rule["rule_name"],
                "rule_type": rule["rule_type"],
                "severity": rule["severity"],
                "message_template": message,
                "suggestion": rule["suggestion"],
            })

    if not triggered:
        return {"overall_level": "low", "risks": []}

    # 大模型生成可读解释
    report = llm_adapter.explain_risks(parsed_spec, triggered)
    return report


def evaluate_condition(condition_expr: str, parsed_spec: dict, selected_clauses: list[dict]) -> bool:
    """
    简单的规则条件求值。
    支持的表达式格式：
      - is_empty:budget  →  字段为空时触发
      - contains:qualification:品牌  →  数组字段包含关键词时触发
      - is_empty:payment_terms|acceptance_criteria  →  多个字段任一为空
    """
    if not condition_expr:
        return False

    parts = condition_expr.split(":", 1)
    if len(parts) < 2:
        return False

    op = parts[0].strip()
    args = parts[1].strip()

    if op == "is_empty":
        fields = [f.strip() for f in args.split("|")]
        for field in fields:
            val = parsed_spec.get(field)
            if val is None or val == "" or val == []:
                return True
        return False

    if op == "contains":
        sub_parts = args.split(":", 1)
        if len(sub_parts) < 2:
            return False
        field = sub_parts[0].strip()
        keyword = sub_parts[1].strip()
        val = parsed_spec.get(field)
        if isinstance(val, list):
            return any(keyword in str(item) for item in val)
        if isinstance(val, str):
            return keyword in val
        return False

    return False
