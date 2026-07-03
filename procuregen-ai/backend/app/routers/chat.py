"""AI 采购顾问聊天路由 — SSE 流式对话"""
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.services.llm_adapter import llm_adapter
import json, uuid

router = APIRouter()

SYSTEM_PROMPT = """你是 ProcureGen AI 采购顾问助手。你精通政府采购法、招标投标法、合同法，
能回答关于采购流程、招标文件编写、合同条款、风险评估的专业问题。
回答要求：
1. 简洁专业，分点回答
2. 涉及法规时注明出处
3. 不确定的内容明确说明
4. 每次回答控制在 300 字以内"""


@router.get("/chat-stream")
async def chat_stream(message: str = "", session_id: str = ""):
    """流式 AI 对话"""
    if not message.strip():
        return StreamingResponse(
            iter(["data: " + json.dumps({"error": "empty"}, ensure_ascii=False) + "\n\n"]),
            media_type="text/event-stream"
        )

    history = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": message}]

    def generate():
        full = ""
        for token in llm_adapter.stream_llm(SYSTEM_PROMPT, message):
            full += token
            yield f"data: {json.dumps({'token': token, 'full': full}, ensure_ascii=False)}\n\n"
        yield f"data: {json.dumps({'done': True, 'full': full}, ensure_ascii=False)}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
