FROM python:3.8-slim-buster

# Metadata
LABEL name="Celery Template"
LABEL maintainer="JeyDi"
LABEL version="0.1"

ARG YOUR_ENV="virtualenv"

ENV YOUR_ENV=${YOUR_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.8 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# Install project libraries
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN pip install "poetry==$POETRY_VERSION"

# Project Python definition
WORKDIR /celery

#Copy all the project files
COPY pyproject.toml .
#COPY poetry.lock .
COPY /app ./app
COPY .env .


# Install libraries
# it's important for celery requirements to have a specific version of setuptools
RUN poetry config virtualenvs.create false \
    && poetry run pip install 'setuptools==59.6.0' \
    && poetry install $(test "$YOUR_ENV" = production) --no-dev --no-interaction --no-ansi