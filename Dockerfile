# Use uv base image with Python 3.14
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

# Set working directory
WORKDIR /app

# Copy project files for dependency installation
COPY pyproject.toml ./

# Install dependencies using native uv commands
# Use --no-dev to skip development dependencies if any
RUN uv sync --frozen --no-dev

# Copy application code
COPY fetch_rss.py ./

# Set the entrypoint to use uv run
ENTRYPOINT ["uv", "run", "python", "fetch_rss.py"]

# Default arguments (can be overridden)
CMD ["--help"]
