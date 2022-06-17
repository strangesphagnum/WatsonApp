FROM python:3.9
WORKDIR /app
ENV POETRY_VERSION=1.0.10

COPY poetry.lock pyproject.toml ./
RUN yes | apt update && yes | apt install git && pip install --no-cache-dir "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi
COPY ./ ./

# TODO: Run from uvicorn
CMD ["bash", "-c", "alembic upgrade head && python3 main.py"]
