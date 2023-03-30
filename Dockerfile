FROM python:3.11-slim-buster AS builder

WORKDIR /app

RUN pip install pipenv

COPY Pipfile* ./

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

COPY . .

FROM python:3.11-slim-buster AS image

WORKDIR /app

RUN useradd -m worker && chown -R worker /app
COPY --from=builder --chown=worker /app .
COPY --from=builder --chown=worker /app/.venv /app/.venv

ENV VIRTUAL_ENV=/app/.venv PATH="/app/.venv/bin:$PATH"

USER worker

ENTRYPOINT ["./entrypoint.sh"]