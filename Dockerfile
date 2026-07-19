# AWS Lambda Python Runtime
FROM public.ecr.aws/lambda/python:3.12

# 작업 디렉토리
WORKDIR ${LAMBDA_TASK_ROOT}

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 복사
COPY . .

# Lambda Handler 지정
ENV LAMBDA_TASK_ROOT=/var/task
ENTRYPOINT ["/lambda-entrypoint.sh"]
CMD ["app.main.handler"]