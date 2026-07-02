# {{project_name or '采购项目'}} 招标文件

---

## 第一章 采购公告

### 1.1 项目概况

| 项目 | 内容 |
|------|------|
| 项目名称 | {{project_name or '（待填写）'}} |
| 采购类型 | {{purchase_type or '（待填写）'}} |
| 采购方式 | {{procurement_method or '公开招标'}} |
| 预算金额 | {{budget or '（待填写）'}} 元 |
| 交付周期 | {{delivery_period or '（待填写）'}} |

---

## 第二章 供应商须知

### 2.1 供应商资格要求

{% if qualification %}
{% for item in qualification %}
- {{item}}
{% endfor %}
{% else %}
- （暂无资格要求，请补充）
{% endif %}

---

## 第三章 采购需求

### 3.1 技术参数

{% if technical_specs %}
{% for item in technical_specs %}
- {{item}}
{% endfor %}
{% else %}
- （暂无技术参数，请补充）
{% endif %}

### 3.2 交付与验收

- 交付周期：{{delivery_period or '（待填写）'}}
- 验收标准：{{acceptance_criteria or '（待填写）'}}
- 质保期限：{{warranty_period or '（待填写）'}}

---

## 第四章 评标办法

### 4.1 评分因素

{% if evaluation_factors %}
{% for item in evaluation_factors %}
- {{item}}
{% endfor %}
{% else %}
- 价格
- 技术
- 商务
- 售后服务
{% endif %}

---

## 第五章 合同主要条款

{% if selected_clauses %}
{% for clause in selected_clauses %}
### {{clause.title}}

{{clause.content}}

> 推荐理由：{{clause.reason}}

{% endfor %}
{% else %}
（暂无推荐条款）
{% endif %}

### 付款方式

{{payment_terms or '（待填写）'}}

---

## 第六章 风险提示附录

> 风险等级：**{{overall_level or 'low'}}**

{% if risks %}
{% for risk in risks %}
### {{risk.level | upper}} 风险：{{risk.type}}

- **说明**：{{risk.message}}
- **建议**：{{risk.suggestion}}

{% endfor %}
{% else %}
暂无风险提示。
{% endif %}

---

*本文档由 ProcureGen AI 自动生成，仅供采购参考，最终版本请人工复核确认。*
