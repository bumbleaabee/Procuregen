"""
LLM Adapter：统一封装 DeepSeek API 调用与 Mock 降级模式。
使用 httpx 直接调用，不依赖 OpenAI SDK，避免版本兼容问题。
"""
import json
import re
import httpx
from app.config import settings


class LLMAdapter:
    def __init__(self):
        self.mode = "mock" if settings.is_mock() else "deepseek"

    def _call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """调用 DeepSeek 大模型，失败时降级到 Mock。"""
        if self.mode == "mock":
            return self._mock_response(user_prompt)

        url = f"{settings.DEEPSEEK_BASE_URL.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json",
        }
        body = {
            "model": settings.DEEPSEEK_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.1,
            "max_tokens": 4096,
        }

        try:
            with httpx.Client(timeout=60) as client:
                resp = client.post(url, headers=headers, json=body)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"].strip()
            else:
                print(f"[LLM] API 返回 {resp.status_code}: {resp.text[:200]}")
                self.mode = "mock"
                return self._mock_response(user_prompt)
        except Exception as e:
            print(f"[LLM] API 调用失败，降级至 Mock 模式: {e}")
            self.mode = "mock"
            return self._mock_response(user_prompt)

    def stream_llm(self, system_prompt: str, user_prompt: str):
        """流式调用 DeepSeek，逐 token yield。Mock 模式模拟逐字输出。"""
        if self.mode == "mock":
            text = self._mock_response(user_prompt)
            for i in range(0, len(text), 3):
                yield text[i:i+3]
            return

        url = f"{settings.DEEPSEEK_BASE_URL.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json",
        }
        body = {
            "model": settings.DEEPSEEK_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.1,
            "max_tokens": 4096,
            "stream": True,
        }
        try:
            with httpx.Client(timeout=90) as client:
                with client.stream("POST", url, headers=headers, json=body) as resp:
                    if resp.status_code != 200:
                        self.mode = "mock"
                        text = self._mock_response(user_prompt)
                        for i in range(0, len(text), 3):
                            yield text[i:i+3]
                        return
                    for line in resp.iter_lines():
                        line = line.strip()
                        if line.startswith("data: "):
                            data = line[6:]
                            if data == "[DONE]":
                                return
                            try:
                                chunk = json.loads(data)
                                delta = chunk["choices"][0].get("delta", {})
                                content = delta.get("content", "")
                                if content:
                                    yield content
                            except (json.JSONDecodeError, KeyError, IndexError):
                                continue
        except Exception as e:
            print(f"[LLM] 流式调用失败: {e}")
            self.mode = "mock"
            text = self._mock_response(user_prompt)
            for i in range(0, len(text), 3):
                yield text[i:i+3]
            print(f"[LLM] API 调用失败，降级至 Mock 模式: {e}")
            self.mode = "mock"
            return self._mock_response(user_prompt)

    def _mock_response(self, user_prompt: str) -> str:
        """Mock 模式返回样例 JSON，保证无 API Key 也能演示。"""
        return json.dumps({
            "project_name": "人工智能实验室服务器采购项目",
            "purchase_type": "货物",
            "procurement_method": "公开招标",
            "budget": 800000,
            "delivery_period": "30天",
            "qualification": [
                "近三年高校信息化项目案例",
                "本地售后服务能力",
                "三年质保承诺"
            ],
            "technical_specs": [
                "4台GPU服务器",
                "每台不少于2张48GB显存GPU",
                "配套深度学习开发环境"
            ],
            "evaluation_factors": ["价格", "技术", "商务", "售后服务"],
            "payment_terms": None,
            "acceptance_criteria": None,
            "warranty_period": "3年",
            "missing_fields": ["付款方式", "验收标准"],
            "confidence": 0.86
        }, ensure_ascii=False)

    # ── 核心调用方法 ──

    def parse_requirement(self, input_text: str) -> dict:
        """解析采购需求为结构化 JSON。"""
        system_prompt = """你是采购文件生成助手。请从用户输入的采购需求中抽取结构化字段。
要求：
1. 只输出 JSON，不要输出解释性文字。
2. 字段缺失时填写 null，并在 missing_fields 中列出。
3. 不要编造用户没有提供的金额、日期、品牌或资质。
4. qualification、technical_specs、evaluation_factors 使用数组。
输出 JSON 字段：
project_name, purchase_type, procurement_method, budget, delivery_period,
qualification, technical_specs, evaluation_factors, payment_terms,
acceptance_criteria, warranty_period, missing_fields, confidence."""
        user_prompt = f"用户需求：{input_text}"
        response_text = self._call_llm(system_prompt, user_prompt)
        return self._extract_json(response_text)

    def recommend_clauses(self, parsed_spec: dict, candidate_clauses: list[dict]) -> list[dict]:
        """根据结构化参数推荐条款。"""
        system_prompt = """你是采购合同条款推荐助手。请根据结构化采购参数，从候选条款中选择适用条款。
要求：
1. 输出 JSON 数组。
2. 每个条款包含 clause_id、title、reason、risk_level。
3. 只能选择候选条款中的内容，不要生成不存在的条款编号。
4. 如果参数不足，请说明需要用户补充的信息。"""
        user_prompt = f"结构化采购参数：{json.dumps(parsed_spec, ensure_ascii=False)}\n候选条款：{json.dumps(candidate_clauses, ensure_ascii=False)}"
        response_text = self._call_llm(system_prompt, user_prompt)
        return self._extract_json(response_text)

    def explain_risks(self, parsed_spec: dict, triggered_rules: list[dict]) -> dict:
        """根据命中规则生成风险解释报告。"""
        system_prompt = """你是采购文件合规预审助手。请根据规则命中的风险项，生成简洁、可解释的风险报告。
要求：
1. 不提供法律意见结论，只提供风险提示和修改建议。
2. 每条风险包含 level、type、reason、suggestion。
3. 建议必须具体、可执行。
4. 语气保持中性、专业。"""
        user_prompt = f"结构化采购参数：{json.dumps(parsed_spec, ensure_ascii=False)}\n命中的规则：{json.dumps(triggered_rules, ensure_ascii=False)}"

        # Mock 模式直接返回规则引擎结果
        if self.mode == "mock":
            risks = []
            overall_map = {"high": 3, "medium": 2, "low": 1}
            max_sev = 0
            for rule in triggered_rules:
                sev_val = overall_map.get(rule.get("severity", "low"), 1)
                if sev_val > max_sev:
                    max_sev = sev_val
                risks.append({
                    "level": rule["severity"],
                    "type": rule["rule_type"],
                    "message": rule.get("message_template", "").format(**parsed_spec) if parsed_spec else rule.get("message_template", ""),
                    "suggestion": rule.get("suggestion", "")
                })
            reverse_map = {3: "high", 2: "medium", 1: "low"}
            return {
                "overall_level": reverse_map.get(max_sev, "low"),
                "risks": risks
            }

        response_text = self._call_llm(system_prompt, user_prompt)
        result = self._extract_json(response_text)
        if isinstance(result, list):
            return {"overall_level": "medium", "risks": result}
        return result if isinstance(result, dict) else {"overall_level": "low", "risks": []}

    def _extract_json(self, text: str):
        """从模型输出中提取 JSON（处理 markdown 代码块包裹）。"""
        if not text:
            return {} if not text.startswith("[") else []
        # 尝试去除 markdown 代码块
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        if match:
            text = match.group(1).strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # 尝试提取第一个 { } 或 [ ] 块
            for pattern in [r"\{[\s\S]*\}", r"\[[\s\S]*\]"]:
                match = re.search(pattern, text)
                if match:
                    try:
                        return json.loads(match.group())
                    except json.JSONDecodeError:
                        continue
            return {}


# 全局单例
llm_adapter = LLMAdapter()
