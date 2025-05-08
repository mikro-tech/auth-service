from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from core import settings
from routers import api_router

app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)

# CORS setup
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/", include_in_schema=False)
async def root():
    return JSONResponse({"message": f"{settings.PROJECT_NAME} is running"})


# Include API routes
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# Uvicorn entry point (if run via python main.py)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )