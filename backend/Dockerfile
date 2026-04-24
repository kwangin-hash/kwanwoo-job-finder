FROM python:3.11-slim

WORKDIR /app

# 시스템 의존성 (lxml 빌드용)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libxml2-dev libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 소스
COPY . .

# Render 가 PORT 환경변수 주입
EXPOSE 8000

CMD ["python", "run.py"]
