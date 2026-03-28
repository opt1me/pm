FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:0.4.15 /uv /bin/uv

# Copy the project into the image.
ADD . /app

# Sync the project into a new environment
WORKDIR /app/backend
RUN uv venv /app/.venv && uv pip compile pyproject.toml -o requirements.txt
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"
RUN uv pip install -r requirements.txt

# Expose the API port.
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')" || exit 1

# Run the backend using the environment's uvicorn.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
