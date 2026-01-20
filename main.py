import limiter
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routers.users import router as users_router
import logging
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

app = FastAPI(
    title="Cloud Community API",
    version="1.0.0"
)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
logging.basicConfig(level=logging.INFO)
app.include_router(users_router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    error = exc.errors()[0]  # 첫 번째 에러만 사용
    field = error["loc"][-1]

    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "error": {
                "code": "VALIDATION_ERROR",
                "message": f"{field}은(는) 올바른 형식이 아닙니다.",
                "details": {
                    "field": field
                }
            }
        }
    )

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "status": "error",
            "error": {
                "code": "RATE_LIMIT_EXCEEDED",
                "message": "요청이 너무 많습니다. 잠시 후 다시 시도해주세요."
            }
        }
    )
