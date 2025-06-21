FROM python:3.11-buster AS python_base

WORKDIR /app
ENV \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PATH="/app/.venv/bin:${PATH}"

FROM python_base AS poetry_base

ARG POETRY_VERSION=1.7.1
RUN pip install "poetry==$POETRY_VERSION" && \
    poetry config virtualenvs.in-project true

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main

FROM python_base

COPY --from=poetry_base /app /app/
COPY ./server /app/server
COPY ./exec /app/exec
COPY ./exec/start /app/exec/start
COPY ./server/alembic.ini /app/alembic.ini

ARG VERSION
ARG MODE

ENV VERSION=${VERSION}
ENV MODE=${MODE}

HEALTHCHECK CMD [ "bash", "/app/exec/healthcheck.sh" ]
CMD [ "bash", "/app/exec/start.sh" ]
