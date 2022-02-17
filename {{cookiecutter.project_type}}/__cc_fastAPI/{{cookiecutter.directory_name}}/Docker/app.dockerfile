FROM python:3.8-slim-buster

# Metadata
LABEL name="FastAPI Template"
LABEL maintainer="JeyDi"
LABEL version="0.1"

ARG YOUR_ENV="virtualenv"

ENV YOUR_ENV=${YOUR_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.13 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# Install poetry dependencies
RUN DEBIAN_FRONTEND=noninteractive apt update && apt install -y libpq-dev gcc curl

# Install project libraries
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN pip install "poetry==$POETRY_VERSION"

# Project Python definition
WORKDIR /fastapi

#Copy all the project files
COPY pyproject.toml .
COPY poetry.lock .
COPY /app ./app
COPY .env .
COPY ./scripts/launch.sh .


# Install libraries
RUN poetry config virtualenvs.create false \
    && poetry install $(test "$YOUR_ENV" = production) --no-dev --no-interaction --no-ansi

#Launch the main (if required)
RUN chmod +x launch.sh
CMD ["bash", "launch.sh"]

#keep the container running in background
# ENTRYPOINT ["tail"]
# CMD ["-f","/dev/null"]