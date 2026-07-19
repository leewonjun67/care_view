import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 1. 엔진 생성을 지연시키기 위해 함수로 분리
def get_engine():
    # Supabase 연결 설정 및 타임아웃(5초) 제한 추가
    return create_engine(
        settings.DATABASE_URL, 
        pool_pre_ping=True,
        pool_recycle=300,
        connect_args={"connect_timeout": 5}
    )

# 2. 세션 생성 함수 (API 엔드포인트에서 호출됨)
def get_db():
    engine = get_engine()
    SessionLocal = sessionmaker(
        autocommit=False, 
        autoflush=False, 
        bind=engine,
        expire_on_commit=False
    )
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3. 모델 정의를 위한 베이스
Base = declarative_base()