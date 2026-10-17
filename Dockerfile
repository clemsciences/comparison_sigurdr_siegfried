# syntax=docker/dockerfile:1

# Build: docker build -t sigurd .
# Browse the texts: docker run --rm -p 8000:8000 sigurd    then open http://localhost:8000
# Other commands:   docker run --rm sigurd list | show nib-c | export /out (mount a volume on /out)

ARG PYTHON_VERSION=3.13

FROM python:${PYTHON_VERSION}-slim-trixie AS builder
COPY --from=ghcr.io/astral-sh/uv:0.9.21 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never
WORKDIR /app

# Dependencies first, so that they stay cached while the code changes.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev --no-install-project

COPY pyproject.toml uv.lock README.md LICENSE ./
COPY src ./src
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable


FROM python:${PYTHON_VERSION}-slim-trixie

LABEL org.opencontainers.image.title="sigurd" \
      org.opencontainers.image.description="Texts of the Nibelungenlied (Bibliotheca Augustana manuscripts A, B, C, n and ReM M321)" \
      org.opencontainers.image.source="https://github.com/clemsciences/comparison_sigurdr_siegfried" \
      org.opencontainers.image.licenses="MIT AND CC-BY-SA-4.0"

RUN useradd --create-home --uid 1000 sigurd
COPY --from=builder --chown=sigurd:sigurd /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1
USER sigurd
WORKDIR /home/sigurd

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/', timeout=2)"]
ENTRYPOINT ["sigurd"]
CMD ["serve", "--host", "0.0.0.0", "--port", "8000"]
