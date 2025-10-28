FROM python:3.11-slim

WORKDIR /app

ENV PYTHONIOENCODING=UTF-8 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    pkg-config \
    cargo \
    rustc \
    fontconfig \
    fonts-noto-cjk \
    fonts-noto-color-emoji \
    fonts-nanum \
    && fc-cache -f -v \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir --prefer-binary -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 포트 노출
EXPOSE 8000

# 서버 실행 - 타임아웃 증가 및 워커 설정
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-keep-alive", "75", "--limit-max-requests", "1000", "--reload"]
