FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    chromium

ENV CHROME_BIN=/usr/bin/chromium





COPY ../requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY .. .

CMD ["celery", "-A", "celery_app.celery_app", "worker", "--loglevel=info"]
