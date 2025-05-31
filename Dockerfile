# Multi-stage Dockerfile for MathSpeak
FROM python:3.9-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy the application
COPY . .

# Production stage
FROM python:3.9-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    espeak-ng \
    libespeak-ng1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -s /bin/bash mathspeak

# Copy from builder
COPY --from=builder /root/.local /home/mathspeak/.local
COPY --from=builder /app /app

# Set working directory
WORKDIR /app

# Change ownership
RUN chown -R mathspeak:mathspeak /app

# Switch to non-root user
USER mathspeak

# Add local bin to PATH
ENV PATH=/home/mathspeak/.local/bin:$PATH

# Create cache directory
RUN mkdir -p /home/mathspeak/.mathspeak/cache

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Default command
CMD ["python", "mathspeak_server.py", "--host", "0.0.0.0", "--port", "8000"]