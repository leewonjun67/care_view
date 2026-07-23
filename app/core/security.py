# app/core/security.py

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from app.core.config import settings


# 신규 비밀번호는 Argon2로 저장
# 기존 sha256_crypt 해시도 로그인 검증 가능
pwd_context = CryptContext(
    schemes=["argon2", "sha256_crypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """
    사용자 비밀번호를 안전한 해시값으로 변환합니다.
    신규 비밀번호는 Argon2 방식으로 저장됩니다.
    """
    if not password:
        raise ValueError("비밀번호는 비어 있을 수 없습니다.")

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    입력받은 일반 비밀번호와 DB에 저장된 해시값을 비교합니다.
    """
    if not plain_password or not hashed_password:
        return False

    try:
        return pwd_context.verify(
            plain_password,
            hashed_password,
        )
    except (ValueError, TypeError, UnknownHashError):
        return False


def password_needs_rehash(hashed_password: str) -> bool:
    """
    기존 sha256_crypt 비밀번호처럼 오래된 해시 방식인지 확인합니다.

    True라면 로그인 성공 후 비밀번호를 다시 해시해
    Argon2 방식으로 DB를 갱신할 수 있습니다.
    """
    if not hashed_password:
        return False

    try:
        return pwd_context.needs_update(hashed_password)
    except (ValueError, TypeError, UnknownHashError):
        return False


def create_access_token(
    subject: str | Any,
    expires_delta: timedelta | None = None,
) -> str:
    """
    사용자 식별자를 subject로 받아 JWT 액세스 토큰을 생성합니다.
    """
    if subject is None:
        raise ValueError("JWT subject 값이 필요합니다.")

    token_expiration = (
        expires_delta
        if expires_delta is not None
        else timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
    )

    expire = datetime.now(timezone.utc) + token_expiration

    payload = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_token(token: str) -> dict[str, Any] | None:
    """
    JWT 토큰의 서명과 만료 시간을 검증하고 payload를 반환합니다.

    유효하지 않거나 만료된 토큰이면 None을 반환합니다.
    """
    if not token:
        return None

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        subject = payload.get("sub")

        if not subject:
            return None

        return payload

    except JWTError:
        return None