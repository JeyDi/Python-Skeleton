FROM python:3.8-slim-buster

# Metadata
LABEL name="{{cookiecutter.project}}"
LABEL maintainer="{{cookiecutter.author}}"
LABEL version="0.1"

ARG YOUR_ENV="virtualenv"
ARG POETRY_VERSION="1.1.13"

ENV YOUR_ENV=${YOUR_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=${POETRY_VERSION} \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH" 


# Install libraries
RUN DEBIAN_FRONTEND=noninteractive apt update && apt install -y \
    libpq-dev gcc curl openssh-client git \
    && pip install "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.create false \
    && poetry install $(test "$YOUR_ENV" = production) --no-dev --no-interaction --no-ansi


# Project Python definition
WORKDIR /mkdocs

#Copy all the project files
COPY pyproject.toml .
COPY poetry.lock .
COPY docs ./docs
COPY makefile .
COPY mkdocs.yml .

#Launch the main (if required)
# CMD ["make debug_docker"]
CMD ["make", "launch_docker"]

#keep the container running in background
# ENTRYPOINT ["tail"]
# CMD ["-f","/dev/null"]