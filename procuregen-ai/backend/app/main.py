"""
FastAPI 应用入口：ProcureGen AI 采购文件智能生成系统。
"""
import os
import sys
import logging

# 确保项目根目录在 sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.database import init_db
from app.data.seed import seed_all
from app.routers import parse, risk, templates, generate

# 日志配置
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("procuregen")

app = FastAPI(
    title="ProcureGen AI",
    description="采购文件智能生成系统 — 需求语义理解 + 动态模板组装 + 合规风险预审 + Word 导出",
    version="2.0.0"
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"未处理异常: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"success": False, "data": None, "message": f"服务器内部错误: {str(exc)}"}
    )


# 注册路由
app.include_router(parse.router, prefix="/api", tags=["需求解析"])
app.include_router(risk.router, prefix="/api", tags=["风险预审"])
app.include_router(templates.router, prefix="/api", tags=["模板与条款"])
app.include_router(generate.router, prefix="/api", tags=["文档生成"])


@app.on_event("startup")
def startup_event():
    """应用启动：初始化数据库与种子数据。"""
    logger.info(f"LLM 模式: {settings.LLM_MODE} | Mock: {settings.is_mock()}")
    init_db()
    seed_all()
    logger.info("系统启动完成 — http://localhost:8000/docs")


@app.get("/")
def root():
    return {
        "service": "ProcureGen AI",
        "version": "2.0.0",
        "docs": "/docs",
        "llm": settings.summary()
    }


@app.get("/api/test-llm")
def test_llm():
    """测试 DeepSeek API 连通性（绕过 SDK，直接 HTTP 请求）。"""
    import httpx

    result = {
        "env_llm_mode": settings.LLM_MODE,
        "env_api_key_set": bool(settings.DEEPSEEK_API_KEY),
        "env_api_key_prefix": (settings.DEEPSEEK_API_KEY[:12] + "...") if settings.DEEPSEEK_API_KEY else "未设置",
        "env_base_url": settings.DEEPSEEK_BASE_URL,
        "env_model": settings.DEEPSEEK_MODEL,
    }

    if settings.is_mock():
        return {"success": False, "message": "配置为 Mock 模式（LLM_MODE=mock 或未设置 API Key）", "detail": result}

    # 直接 HTTP 测试
    url = f"{settings.DEEPSEEK_BASE_URL.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": settings.DEEPSEEK_MODEL,
        "messages": [{"role": "user", "content": "请回复：OK"}],
        "max_tokens": 10,
    }
    result["request_url"] = url

    try:
        with httpx.Client(timeout=10) as client:
            resp = client.post(url, headers=headers, json=body)
        result["http_status"] = resp.status_code

        if resp.status_code == 200:
            data = resp.json()
            return {
                "success": True,
                "message": "DeepSeek API 连接成功！",
                "response": data["choices"][0]["message"]["content"],
                "model_used": data.get("model", ""),
            }
        else:
            return {
                "success": False,
                "message": f"HTTP {resp.status_code}",
                "detail": {**result, "response_body": resp.text[:500]}
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"连接失败: {type(e).__name__}: {str(e)}",
            "detail": result
        }
