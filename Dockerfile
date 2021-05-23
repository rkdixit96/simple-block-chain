FROM python:3.9.0

RUN pip install poetry
COPY pyproject.toml /
RUN poetry config virtualenvs.create false && poetry install

ENV PYTHONPATH "${PYTHONPATH}:/motucoin"