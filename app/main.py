from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from mangum import Mangum
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db


def create_app() -> FastAPI:
    # FastAPI 인스턴스 생성
    app = FastAPI(
        title="CareView API",
        version="v1",
        description="로그인, 회원가입, 일정 관리 등을 위한 API",
    )

    # 프런트엔드에서 백엔드 API 호출을 허용할 출처
    origins = [
        # 로컬 개발 환경
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:5173",

        # 기존 배포 주소
        "https://careview-front.onrender.com",
        "https://careview.kro.kr",
        "https://www.careview.kro.kr",

        # 기존 S3 정적 웹사이트 주소
        "http://careview-front-bucket.s3-website.ap-northeast-2.amazonaws.com",

        # 현재 CloudFront 프런트엔드 주소
        "https://d18nlrjzbq5l8h.cloudfront.net",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 지연 로딩: 앱 생성 시점에 라우터 모듈 불러오기
    from app.api.endpoints import (
        user,
        onboarding,
        record,
        main_page,
        meals,
        exercise,
        expected_effect,
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
                "message": "CareView API is running and DB is connected",
            }

        except Exception as e:
            return {
                "status": "error",
                "db": "disconnected",
                "message": f"DB Connection failed: {str(e)}",
            }

    # Swagger/OpenAPI JWT 인증 설정
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )

        # components가 존재하지 않는 경우를 대비
        openapi_schema.setdefault("components", {})

        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }

        security_requirement = [{"BearerAuth": []}]

        protected_tags = {
            "Users",
            "Onboarding",
            "Record",
            "Main Page",
            "meals",
            "Exercise",
            "Expected Effect",
        }

        for path_item in openapi_schema.get("paths", {}).values():
            for method in path_item.values():
                # OpenAPI 경로 내부에 parameters 같은 비-HTTP 항목이 생길 경우 대비
                if not isinstance(method, dict):
                    continue

                tags = method.get("tags", [])

                if any(tag in protected_tags for tag in tags):
                    method["security"] = security_requirement

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

    return app


# FastAPI 앱 인스턴스
app = create_app()

# AWS Lambda 핸들러
handler = Mangum(app)