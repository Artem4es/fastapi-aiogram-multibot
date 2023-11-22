FROM diliplakshya/python3.10.12-alpine3.18-poetry
WORKDIR /alfbot/
COPY pyproject.toml poetry.lock /alfbot/
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "/alfbot"

RUN apk update && apk add poetry && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /alfbot/
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

