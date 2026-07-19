from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from mangum import Mangum
from sqlalchemy import text

# 본인의 프로젝트 구조에 맞춘 import 경로
from app.api.endpoints import user as user_api
from app.api.endpoints import onboarding as onboarding_api
from app.api.endpoints import record as record_api
from app.api.endpoints import main_page as main_page_api
from app.api.endpoints import meals as meals_api
from app.api.endpoints import exercise
from app.api.endpoints import expected_effect

# database.py에서 설정한 engine을 가져옵니다.
from app.core.database import engine

app = FastAPI(
    title="CareView API",
    version="v1",
    description="로그인, 회원가입, 일정 관리 등을 위한 API"
)
#"@@"

# CORS 설정
origins = [
    "http://localhost:3000", 
    "http://localhost:8000",
    "http://localhost:5173",
    "https://careview-front.onrender.com",
    "https://careview.kro.kr",
    "https://www.careview.kro.kr",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(user_api.router, tags=["Users"])
app.include_router(onboarding_api.router, tags=["Onboarding"])
app.include_router(record_api.router, tags=["Record"])
app.include_router(main_page_api.router, tags=["Main Page"])
app.include_router(meals_api.router, tags=["meals"])
app.include_router(exercise.router, tags=["Exercise"])
app.include_router(expected_effect.router, tags=["Expected Effect"])

@app.get("/")
def read_root():
    return {"message": "Welcome to CareView API V1"}

# DB 연결 확인 및 헬스 체크
@app.get("/health", tags=["Health Check"])
def health_check():
    try:
        # database.py에서 가져온 engine을 사용하여 실제 DB 연결 테스트
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {
            "status": "ok", 
            "db": "connected", 
            "message": "CareView API is running and DB is connected"
        }
    except Exception as e:
        return {
            "status": "error", 
            "db": "disconnected", 
            "message": f"DB Connection failed: {str(e)}"
        }

# OpenAPI 설정
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer", 
            "bearerFormat": "JWT"
        }
    }
    
    security_requirement = [{"BearerAuth": []}]
    for route in openapi_schema["paths"].values():
        for method in route.values():
            tags = method.get('tags', [])
            if tags and any(tag in ['Users', 'Onboarding', 'Record', 'Main Page', 'meals', 'Exercise', 'Expected Effect'] for tag in tags):
                method["security"] = security_requirement

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Lambda 핸들러
handler = Mangum(app)