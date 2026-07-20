from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from mangum import Mangum
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.database import get_db

def create_app():
    # FastAPI 인스턴스 생성
    app = FastAPI(
        title="CareView API",
        version="v1",
        description="로그인, 회원가입, 일정 관리 등을 위한 API"
    )

    # CORS 설정 (S3 정적 웹 사이트 호스팅 주소 추가 완료)
    origins = [
        "http://localhost:3000", 
        "http://localhost:8000",
        "http://localhost:5173",
        "https://careview-front.onrender.com",
        "https://careview.kro.kr",
        "https://www.careview.kro.kr",
        "http://careview-front-bucket.s3-website.ap-northeast-2.amazonaws.com",  # S3 호스팅 주소 추가
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # [지연 로딩 적용] 함수 내부에서 라우터 모듈을 import하여 초기 로딩 부하를 줄임
    from app.api.endpoints import (
        user, onboarding, record, main_page, meals, exercise, expected_effect
    )

    # 라우터 등록
    app.include_router(user.router, tags=["Users"])
    app.include_router(onboarding.router, tags=["Onboarding"])
    app.include_router(record.router, tags=["Record"])
    app.include_router(main_page.router, tags=["Main Page"])
    app.include_router(meals.router, tags=["meals"])
    app.include_router(exercise.router, tags=["Exercise"])
    app.include_router(expected_effect.router, tags=["Expected Effect"])

    @app.get("/")
    def read_root():
        return {"message": "Welcome to CareView API V1"}

    @app.get("/health", tags=["Health Check"])
    def health_check(db: Session = Depends(get_db)):
        try:
            db.execute(text("SELECT 1"))
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
    return app

# 앱 인스턴스 생성 및 Mangum 핸들러 등록
app = create_app()
handler = Mangum(app)