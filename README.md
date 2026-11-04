# CareView

React, FastAPI, AWS Lambda, Supabase를 활용한 클라우드 네이티브 건강관리 플랫폼입니다.

## 프로젝트 개요

CareView는 안전한 사용자 관리, 의료 기록 관리, AI 기반 건강관리 지원 기능을 제공하며 AWS 클라우드 네이티브 환경에 배포된 풀스택 건강관리 시스템입니다.

프론트엔드는 React와 Vite로 구축했으며, 백엔드는 컨테이너 이미지를 사용하는 AWS Lambda 환경에서 FastAPI로 실행됩니다. 데이터베이스는 Supabase PostgreSQL을 사용하고, GitHub Actions를 통해 CI/CD를 자동화했습니다.

---

## 기술 스택

### 프론트엔드
- React
- Vite
- JavaScript
- CSS

### 백엔드
- FastAPI
- SQLAlchemy
- Alembic
- Python

### 데이터베이스
- Supabase (PostgreSQL)

### AWS
- AWS Lambda (컨테이너 이미지)
- Amazon ECR
- Amazon S3
- Amazon CloudFront
- IAM

### DevOps
- Docker
- GitHub Actions (CI/CD)

---

## 주요 기능

- 사용자 인증
- 환자 관리
- 의료 기록 관리
- 대시보드
- AI 건강관리 챗봇
- 클라우드 네이티브 배포
- CI/CD 파이프라인 자동화

---

## 시스템 아키텍처

<img width="526" height="280" alt="image" src="https://github.com/user-attachments/assets/111cb55a-6f3b-4586-9450-6cedd23d5f71" />


---

## 시스템 흐름

```text
사용자
   │
   ▼
CloudFront
   │
   ▼
Amazon S3 (React + Vite)
   │
   ▼
FastAPI (AWS Lambda)
   │
   ▼
Supabase PostgreSQL
```

---

## CI/CD

### 백엔드

```text
GitHub
   │
GitHub Actions
   │
Docker 빌드
   │
Amazon ECR
   │
AWS Lambda
```

### 프론트엔드

```text
GitHub
   │
GitHub Actions
   │
Vite 빌드
   │
Amazon S3
   │
CloudFront
```

---

## AWS 서비스

| 서비스 | 역할 |
|---|---|
| Lambda | 백엔드 API |
| ECR | Docker 이미지 저장소 |
| S3 | 프론트엔드 호스팅 |
| CloudFront | CDN |
| IAM | 접근 권한 관리 |

---

## 로컬 실행

### 백엔드

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 프론트엔드

```bash
cd FrontEnd-main
npm install
npm run dev
```

---

## 저장소

https://github.com/leewonjun67/care_view
