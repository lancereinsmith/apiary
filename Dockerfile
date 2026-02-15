# Python version should stay in sync with pyproject.toml requires-python (>=3.12)
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

# Enable bytecode compilation for faster startup
ENV UV_COMPILE_BYTECODE=1
# Prevent uv from creating a cache directory
ENV UV_NO_CACHE=1

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Install dependencies (no dev groups in production)
RUN uv sync --frozen --no-dev

# Copy application code
COPY . /app

EXPOSE 8000

# Use uv run to execute the application
CMD ["uv", "run", "--no-dev", "uvicorn", "app:api", "--host", "0.0.0.0", "--port", "8000"]