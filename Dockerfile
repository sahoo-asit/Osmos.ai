# Lead Manager QA Automation - Docker Image
# Supports: Local runs, CI/CD, Jenkins, Remote execution

FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    procps \
    curl \
    unzip \
    openjdk-17-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (for Playwright)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Allure
RUN wget -qO- https://github.com/allure-framework/allure2/releases/download/2.25.0/allure-2.25.0.tgz | tar -xz -C /opt/ \
    && ln -s /opt/allure-2.25.0/bin/allure /usr/local/bin/allure

# Set working directory
WORKDIR /app

# Copy requirements first (for layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN python -m playwright install chromium
RUN python -m playwright install-deps chromium

# Copy test framework
COPY . .

# Create reports directory
RUN mkdir -p reports

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_BROWSERS_PATH=/root/.cache/ms-playwright
ENV ALLURE_PORT=5050

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${ALLURE_PORT} || exit 1

# Default command: run smoke tests and serve Allure
CMD ["./run.sh", "--smoke", "--report"]
