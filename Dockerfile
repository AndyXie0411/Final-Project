FROM python:3.11-slim

WORKDIR /app

# Install minimal system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install all packages at once to avoid conflicts
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    Flask==2.3.0 \
    transformers==4.35.0 \
    accelerate==0.24.0 \
    sentencepiece==0.1.99 \
    protobuf==3.20.0

# Install torch separately with CPU-only version
RUN pip install --no-cache-dir \
    torch==2.0.1+cpu \
    torchvision==0.15.2+cpu \
    torchaudio==2.0.2+cpu \
    --index-url https://download.pytorch.org/whl/cpu

# Copy application
COPY app.py .
COPY templates/ ./templates/

# Expose port 8080
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/api/health || exit 1

# Set environment variables
ENV PORT=8080
ENV HF_MODEL_NAME="microsoft/DialoGPT-small"
ENV HF_HOME="/app/.cache/huggingface"
ENV TRANSFORMERS_CACHE="/app/.cache/huggingface/models"

# Run the application
CMD ["python", "app.py"]