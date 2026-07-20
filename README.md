# CareView

Cloud-native healthcare management platform built with React, FastAPI, AWS Lambda, and Supabase.

## Overview

CareView is a full-stack healthcare management system that provides secure patient management, medical record management, AI-powered healthcare assistance, and cloud-native deployment on AWS.

The frontend is built with React and Vite, while the backend is powered by FastAPI running on AWS Lambda using container images. The application uses Supabase PostgreSQL as its database and GitHub Actions for automated CI/CD.

---

## Tech Stack

### Frontend
- React
- Vite
- JavaScript
- CSS

### Backend
- FastAPI
- SQLAlchemy
- Alembic
- Python

### Database
- Supabase (PostgreSQL)

### AWS
- AWS Lambda (Container Image)
- Amazon ECR
- Amazon S3
- Amazon CloudFront
- IAM

### DevOps
- Docker
- GitHub Actions (CI/CD)

---

## Main Features

- User authentication
- Patient management
- Medical record management
- Dashboard
- AI healthcare chatbot
- Cloud-native deployment
- Automated CI/CD pipeline

---

## System Flow

```
User
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

### Backend

```
GitHub
   │
GitHub Actions
   │
Docker Build
   │
Amazon ECR
   │
AWS Lambda
```

### Frontend

```
GitHub
   │
GitHub Actions
   │
Vite Build
   │
Amazon S3
   │
CloudFront
```

---

## AWS Services

| Service | Purpose |
|----------|---------|
| Lambda | Backend API |
| ECR | Docker image repository |
| S3 | Frontend hosting |
| CloudFront | CDN |
| IAM | Access management |

---

## Local Run

### Backend

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd FrontEnd-main
npm install
npm run dev
```

---

## Live Demo

```
https://YOUR-CLOUDFRONT-DOMAIN
```

---

## Repository

```
https://github.com/leewonjun67/care_view
```
