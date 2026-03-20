FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Set working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy project files
COPY pyproject.toml uv.lock ./

# Install dependencies separately to cache layers
RUN uv sync --frozen --no-install-project --no-dev

# Copy application code
COPY . .

# Install the project itself (if needed)
RUN uv sync --frozen --no-dev

# Set environment variables (defaults)
ENV PYTHONUNBUFFERED=1

# Launch the bot
CMD ["uv", "run", "bot.py"]
