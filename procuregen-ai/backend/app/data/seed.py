"""
种子数据：初始化默认模板、条款库和风险规则。
"""
import os
from pathlib import Path
from app.database import get_connection


def seed_all():
    """插入所有种子数据（幂等）。"""
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) FROM templates").fetchone()[0]
    if count > 0:
        conn.close()
        print("[Seed] 数据库已初始化，跳过种子数据。")
        return

    _seed_templates(conn)
    _seed_clauses(conn)
    _seed_risk_rules(conn)
    conn.commit()
    conn.close()
    print("[Seed] 种子数据初始化完成（1 个模板 + 9 个条款 + 7 条规则）。")


def _seed_templates(conn):
    # 模板目录：backend/../templates/
    template_dir = Path(__file__).resolve().parent.parent.parent.parent / "templates"
    template_path = template_dir / "tender_template.md"

    if template_path.exists():
        template_content = template_path.read_text(encoding="utf-8")
    else:
        template_content = _default_template_content()

    conn.execute(
        "INSERT INTO templates (name, template_type, content, variables) VALUES (?, ?, ?, ?)",
        ("标准招标书模板", "tender", template_content,
         "project_name,purchase_type,procurement_method,budget,delivery_period,qualification,technical_specs,evaluation_factors,payment_terms,acceptance_criteria,warranty_period,selected_clauses,risks")
    )


def _default_template_content() -> str:
    return """# {{project_name or '采购项目'}} 招标文件

## 第一章 采购公告

| 项目 | 内容 |
|------|------|
| 项目名称 | {{project_name or '（待填写）'}} |
| 采购类型 | {{purchase_type or '（待填写）'}} |
| 采购方式 | {{procurement_method or '公开招标'}} |
| 预算金额 | {{budget or '（待填写）'}} 元 |

## 第二章 供应商资格要求

{% if qualification %}{% for item in qualification %}
- {{item}}
{% endfor %}{% else %}
- （暂无资格要求）
{% endif %}

## 第三章 采购需求

{% if technical_specs %}{% for item in technical_specs %}
- {{item}}
{% endfor %}{% else %}
- （暂无技术参数）
{% endif %}

## 第四章 合同主要条款

{% if selected_clauses %}{% for clause in selected_clauses %}
### {{clause.title}}
{{clause.content}}
{% endfor %}{% endif %}

## 第五章 风险提示

{% if risks %}{% for risk in risks %}
- **{{risk.level}}**: {{risk.message}} → {{risk.suggestion}}
{% endfor %}{% endif %}
"""


def _seed_clauses(conn):
    clauses = [
        {
            "title": "交付与验收条款",
            "category": "通用",
            "content": "1. 乙方应于合同签订后__日内完成全部货物/服务的交付。\n2. 甲方应在收到货物后__个工作日内完成验收，验收标准以本合同附件技术规格为准。\n3. 验收合格后双方签署验收报告。",
            "applicable_condition": "货物"
        },
        {
            "title": "质量保证条款",
            "category": "通用",
            "content": "1. 乙方保证所提供的产品为全新、未使用过的原装正品，符合国家相关质量标准。\n2. 质保期为验收合格之日起__年，质保期内乙方免费提供维修、更换服务。",
            "applicable_condition": "货物"
        },
        {
            "title": "履约保证金条款",
            "category": "财务",
            "content": "1. 乙方应在合同签订后__个工作日内向甲方缴纳合同总金额__%的履约保证金。\n2. 项目验收合格后，甲方应在__个工作日内无息退还履约保证金。",
            "applicable_condition": "预算较高"
        },
        {
            "title": "付款节点条款",
            "category": "财务",
            "content": "1. 合同签订后__个工作日内支付合同总金额的__%作为预付款。\n2. 全部货物交付并验收合格后支付合同总金额的__%。\n3. 质保期满后支付剩余__%的尾款。",
            "applicable_condition": "预算较高"
        },
        {
            "title": "知识产权条款",
            "category": "法律",
            "content": "1. 乙方保证所提供的软件、技术方案不侵犯第三方知识产权。\n2. 项目产生的知识产权归属由双方另行约定。\n3. 如因知识产权纠纷给甲方造成损失，乙方应承担全部赔偿责任。",
            "applicable_condition": "软件"
        },
        {
            "title": "数据安全条款",
            "category": "法律",
            "content": "1. 乙方应严格遵守国家数据安全相关法律法规。\n2. 未经甲方书面同意，乙方不得将甲方数据用于本合同约定之外的其他用途。\n3. 乙方应采取必要的技术措施保障数据安全。",
            "applicable_condition": "软件"
        },
        {
            "title": "延期交付违约责任条款",
            "category": "通用",
            "content": "1. 乙方未按合同约定时间交付的，每逾期一日应向甲方支付合同总金额__%的违约金。\n2. 逾期超过__日的，甲方有权单方解除合同，并要求乙方赔偿损失。",
            "applicable_condition": "交付周期紧张"
        },
        {
            "title": "售后服务条款",
            "category": "通用",
            "content": "1. 乙方应提供__小时技术支持热线。\n2. 乙方应在接到报修后__小时内响应，__小时内到达现场。\n3. 乙方应提供不少于__年的备品备件供应。",
            "applicable_condition": "货物"
        },
        {
            "title": "保密条款",
            "category": "法律",
            "content": "1. 双方应对在合同履行过程中知悉的对方商业秘密和技术秘密承担保密义务。\n2. 保密期限自合同签订之日起至合同终止后__年。\n3. 违反保密义务的一方应赔偿对方因此造成的全部损失。",
            "applicable_condition": "通用"
        },
    ]
    for c in clauses:
        conn.execute(
            "INSERT INTO clauses (title, category, content, applicable_condition) VALUES (?, ?, ?, ?)",
            (c["title"], c["category"], c["content"], c["applicable_condition"])
        )


def _seed_risk_rules(conn):
    rules = [
        {
            "rule_name": "预算缺失风险",
            "rule_type": "缺失项风险",
            "severity": "high",
            "condition_expr": "is_empty:budget",
            "message_template": "采购需求中未明确预算金额，无法判断采购规模。",
            "suggestion": "请补充预算金额，确保采购计划在预算范围内。"
        },
        {
            "rule_name": "交付周期缺失风险",
            "rule_type": "缺失项风险",
            "severity": "medium",
            "condition_expr": "is_empty:delivery_period",
            "message_template": "采购需求中未明确交付周期。",
            "suggestion": "请补充交付周期，明确项目时间节点。"
        },
        {
            "rule_name": "验收标准缺失风险",
            "rule_type": "缺失项风险",
            "severity": "medium",
            "condition_expr": "is_empty:acceptance_criteria",
            "message_template": "采购需求中未明确验收标准，可能导致交付争议。",
            "suggestion": "请补充验收标准，包括验收主体、验收流程和验收指标。"
        },
        {
            "rule_name": "付款方式缺失风险",
            "rule_type": "缺失项风险",
            "severity": "medium",
            "condition_expr": "is_empty:payment_terms",
            "message_template": "采购需求中未明确付款方式，合同执行存在不确定性。",
            "suggestion": "请补充付款节点、付款比例和付款条件。"
        },
        {
            "rule_name": "质保缺失风险",
            "rule_type": "缺失项风险",
            "severity": "low",
            "condition_expr": "is_empty:warranty_period",
            "message_template": "采购需求中未明确质保期限。",
            "suggestion": "建议补充质保期限和质保范围，保护采购方权益。"
        },
        {
            "rule_name": "指定品牌风险",
            "rule_type": "限制性条款风险",
            "severity": "high",
            "condition_expr": "contains:qualification:品牌",
            "message_template": "供应商资格条件中可能存在指定品牌或唯一供应商的排他性表述。",
            "suggestion": "建议将品牌要求改为性能指标或技术参数要求，避免限制公平竞争。"
        },
        {
            "rule_name": "资格条件缺失风险",
            "rule_type": "缺失项风险",
            "severity": "medium",
            "condition_expr": "is_empty:qualification",
            "message_template": "未设置供应商资格条件，可能导致不合格供应商参与投标。",
            "suggestion": "建议补充供应商资质要求，如业绩案例、资质证书、人员配置等。"
        },
    ]
    for r in rules:
        conn.execute(
            "INSERT INTO risk_rules (rule_name, rule_type, severity, condition_expr, message_template, suggestion) VALUES (?, ?, ?, ?, ?, ?)",
            (r["rule_name"], r["rule_type"], r["severity"], r["condition_expr"], r["message_template"], r["suggestion"])
        )
