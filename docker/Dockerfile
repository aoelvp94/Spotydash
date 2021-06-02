FROM python:3.8.5

# Setup pipx and poetry
RUN pip install pipx
RUN pipx install poetry
ENV PATH="/root/.local/pipx/venvs/poetry/bin/:$PATH"

COPY pyproject.toml /spotydash/pyproject.toml
COPY poetry.lock /spotydash/poetry.lock
WORKDIR /spotydash
RUN poetry install --no-root
COPY . /spotydash
RUN poetry install --no-interaction
