FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git curl build-essential libgomp1 libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install torch from CPU wheels
RUN pip install --no-cache-dir torch==2.1.0 --index-url https://download.pytorch.org/whl/cpu

# Install other Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY app.py .
COPY templates/ ./templates/

# Expose port
EXPOSE 8080

# Set environment variables
ENV PORT=8080
ENV HF_MODEL_NAME="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
ENV HF_HOME="/app/.cache/huggingface"
ENV TRANSFORMERS_CACHE="/app/.cache/huggingface/models"

# Run the app
CMD ["python", "app.py"]
