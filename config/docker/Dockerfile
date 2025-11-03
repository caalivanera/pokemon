# Multi-stage Dockerfile for Pokemon Dashboard
# Production-ready with security best practices

# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

# Create non-root user for security
RUN useradd -m -u 1000 pokemonuser && \
    mkdir -p /app && \
    chown -R pokemonuser:pokemonuser /app

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder --chown=pokemonuser:pokemonuser \
    /root/.local /home/pokemonuser/.local

# Copy application code
COPY --chown=pokemonuser:pokemonuser . .

# Set environment variables
ENV PATH=/home/pokemonuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Switch to non-root user
USER pokemonuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8501/_stcore/health')"

# Expose Streamlit port
EXPOSE 8501

# Run database initialization and start app
CMD ["sh", "-c", "python src/database/data_loader.py && streamlit run src/core/app.py"]
