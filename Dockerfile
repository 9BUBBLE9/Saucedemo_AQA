FROM python:3.10-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget gnupg ca-certificates \
    libnss3 libnspr4 libasound2 \
    libx11-6 libx11-xcb1 libxcomposite1 libxdamage1 libxfixes3 \
    libxrandr2 libxkbcommon0 libgtk-3-0 libgbm1 libglib2.0-0 \
    libpango-1.0-0 libpangocairo-1.0-0 libcairo2 libatspi2.0-0 \
    libdrm2 libdbus-1-3 libxext6 libxcb1 libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


RUN python -m playwright install --with-deps chromium

COPY . .

CMD ["pytest"]
