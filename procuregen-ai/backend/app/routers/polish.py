"""AI 文档润色 + 续写路由"""
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.services.llm_adapter import llm_adapter
import json

router = APIRouter()

POLISH_PROMPTS = {
    "polish": "你是采购文档润色专家。请将以下文本润色为更专业、更规范的采购文件语言，保持原意不变，只输出润色后文本：\n\n",
    "expand": "你是采购文档撰写专家。请将以下简要描述扩展为详细、专业的采购文件段落，补充必要的细节和规范表述，只输出扩展后文本：\n\n",
    "shorten": "你是采购文档精简专家。请将以下文本精简为简洁版本，保留核心信息，去除冗余表述，只输出精简后文本：\n\n",
    "formal": "你是政府采购文档专家。请将以下文本改写为正式的政府采购文件语调，使用规范术语，只输出改写后文本：\n\n",
    "autocomplete": "你是采购文档续写专家。请根据用户已写的内容，专业地续写后续段落，保持风格一致。只输出续写内容，不要重复已有内容：\n\n",
}


class PolishRequest(BaseModel):
    text: str
    action: str = "polish"  # polish / expand / shorten / formal / autocomplete


@router.post("/polish")
def polish_text(req: PolishRequest):
    """非流式润色"""
    prompt = POLISH_PROMPTS.get(req.action, POLISH_PROMPTS["polish"])
    try:
        result = llm_adapter._call_llm(prompt + req.text, req.text)
        return {"success": True, "data": {"result": result}, "message": "ok"}
    except Exception as e:
        return {"success": False, "data": None, "message": str(e)}


@router.get("/polish-stream")
async def polish_stream(text: str = "", action: str = "polish"):
    """流式润色"""
    if not text.strip():
        return StreamingResponse(iter(["data: {}\n\n"]), media_type="text/event-stream")

    prompt = POLISH_PROMPTS.get(action, POLISH_PROMPTS["polish"])

    def generate():
        full = ""
        for token in llm_adapter.stream_llm(prompt + text, text):
            full += token
            yield f"data: {json.dumps({'token': token, 'full': full}, ensure_ascii=False)}\n\n"
        yield f"data: {json.dumps({'done': True, 'full': full}, ensure_ascii=False)}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
