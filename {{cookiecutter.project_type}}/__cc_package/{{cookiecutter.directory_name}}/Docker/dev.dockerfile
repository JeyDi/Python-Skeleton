FROM ubuntu:20.04

# Metadata
LABEL name="dev_container"
LABEL maintainer="JeyDi"
LABEL version="0.1"

ARG YOUR_ENV="virtualenv"
ARG POETRY_VERSION="1.1.13"

# Define environment variables
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
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    VENV_PATH="/opt/pysetup/.venv" \
    PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Install Node
#RUN apt-get update && apt-get install -y curl && curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && apt-get install -y nodejs

# Install Git
RUN DEBIAN_FRONTEND=noninteractive apt update \
    && apt upgrade -y \
    && apt install -y git \
    && apt install -y python3.8 python3-pip python-is-python3 \
    && apt install -y libpq-dev gcc curl


# Install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN pip install "poetry==$POETRY_VERSION"

# Copy ssh keys from local machine to dev container
#RUN ssh-add $HOME/.ssh/keyname

##########################
# Project Python definition
WORKDIR /workspace

#Copy all the project files
COPY . .

# Install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
# Install libraries
# RUN poetry config virtualenvs.create false \
#     && poetry install $(test "$YOUR_ENV" = production) --no-dev --no-interaction --no-ansi
RUN poetry install

#Launch the main (if required)