ARG PYTHON_VERSION=3.13
FROM python:${PYTHON_VERSION}-slim as builder

RUN pip install --no-cache-dir uv

RUN --mount=type=bind,source=requirements.txt,target=requirements.txt  \
    uv pip install --system -r requirements.txt

FROM python:${PYTHON_VERSION}-slim as final

WORKDIR /app

ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

COPY --from=builder /usr/local/lib /usr/local/lib

COPY --chown=appuser:appuser . .

USER appuser

CMD ["python", "src/__main__.py"]
