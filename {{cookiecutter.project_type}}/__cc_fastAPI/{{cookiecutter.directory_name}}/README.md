# FastAPI Template

This repository contains my version of FastAPI template with a simple example and contains everything I have learned so far about.

Please feel free to open issues and pull requests if something is missing or needs to be changed.

## Features implemented
- FastAPI standard logic implementation
- FastAPI api routing
- Pydantic validation
- SQLAlchemy support for postgres with ORM and different types of relations
- vscode features: debugger, devcontainer
- docker compose and docker integration
- test for TDD (db and API)
- auth system with OAuth2
- gitlab issue and bug management
- generic api pattern and classes
- integration with cookiecutter template
- uvicorn ASGI on gunicorn wrapper for more stability
- Alembic database migration
- Pydantic class for the configs
- Celery with Redis for async tasks
- Celery job monitoring with flower
- Grafana and Prometheus integration with Celery and Flower
- RabbitMQ Integration (not tested yet)
- Caching system with Redis async
- Caching system with Memcached async

### Features to be done
- FastAPI Web socket
- Testing with the database (not committing the data changes)
- SQLAlchemy possibility to launch sql scripts and sql queries
- Automatic CI/CD pipelines for github and gitlab
- MKDocs documentation system and integration

### Cache System

The cache system it's created with `redis` and `memcache` libraries.

If you want to test the cache system with redis you have to create the redis container up there is also the possibility to have the web interface to check the informations about the cache.

If you want to use memcache you have to install memcache manually in your system before.


** Redis Caching notes**
- https://rednafi.github.io/digressions/python/database/2020/05/25/python-redis-cache.html
- https://realpython.com/python-redis/
- aioredis official doc (v2) https://aioredis.readthedocs.io/en/v2.0.1/
- aioredis high level api: https://aioredis.readthedocs.io/en/v2.0.1/api/high-level/#aioredis.client.Redis
- redis py default library documentation: https://redis.readthedocs.io/en/latest/
- fastapi_cache library: https://github.com/long2ice/fastapi-cache/blob/master/fastapi_cache/backends/redis.py
- introduction to redis: https://redistogo.com/documentation/introduction_to_redis
- introduction to asyncaio: https://realpython.com/async-io-python/
- examples with asyncaio: https://www.velotio.com/engineering-blog/async-features-in-python#:~:text=An%20async%20function%20uses%20the,Tasks%20as%20a%20Future%20object.

**Memcache notes**
aiomcache example to cache in memory variables.
asyncio (PEP 3156) library to work with memcached.
- official documentation: https://pypi.org/project/aiomcache/
- implementation of functions: https://github.com/aio-libs/aiomcache/blob/master/aiomcache/client.py
- https://realpython.com/python-memcache-efficient-caching/

WARNING: remember to install memcached manually on your system before using it

## Install and configure the project

First of all it's important to install `poetry`.  
If you don't know how to install it please follow this guide

If you want to save the virtualenv inside the project folder please do: 

Then you have to initialize the project with: `poetry install`

If you want to use the environment variable, you have to create a .env variable with this values inside:
```bash
DB_PORT=<your_db_external_port>

APP_DB_NAME=fastcash
APP_DB_USER=root
APP_DB_PASSWORD=<yourpassword>
APP_DB_PORT=<yourport>
APP_DB_HOST="fastcash-db"

APP_ENDPOINT_HOST="localhost"
APP_DOCKER_PORT=<your_docker_app_external_port>
APP_ENDPOINT_PORT=8044
APP_SECRET_KEY=<your_app_secret>
APP_DEBUG_MODE="False"
APP_VERBOSITY="DEBUG"
APP_API_TOKEN=<your_secret_app_api_token>

#optional
POSTGRES_DATA_DIR=<your_machine_data_folder>
POSTGRES_BACKUP_DIR=<your_machine_backup_folder>
```

### Launching the project

If you want to launch the project locally you can use:
1. the terminal launching the scripts inside the folder: `scripts`
2. using docker
3. using vscode debugger (already setupped)


## VSCode settings

To configure and use vscode as main IDE with Python it's important to create two main files: `settings.json` and `launch.json`.

### Setting the Vscode Ide

This settings can be done only the first time because if you log-in with your Github or Microsoft account it's possible to keep all your settings in every machine and vscode you use.

Please remember to **install the required extensions for vscode** before.

First of all it's important to create inside the project a folder called: `.vscode`.

Inside this folder create new file with the name: `launch.json`.
This file it's important because contains all the settings for the vscode python debugger.

The content of the file is this one (paste inside the file).
```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
      {
        "name": "Python: Current File",
        "type": "python",
        "request": "launch",
        "program": "${file}",
        "console": "integratedTerminal",
        "cwd": "${workspaceFolder}",
        "env": {
          "PYTHONPATH": "${cwd}",
          "VERBOSITY": "DEBUG",
          
        }
      },
      {
        "name": "FastAPI",
        "type": "python",
        "request": "launch",
        "module": "uvicorn",
        "args": ["app.main:app", "--reload", "--port", "8044"],
        "env": {
          "PYTHONPATH": "${cwd}",
          "API_ENDPOINT_PORT": "8042",
          "API_ENDPOINT_HOST": "localhost",
          "APP_VERBOSITY": "DEBUG",
        }
      },
    ]
  }

```
With the `Python: Current File` you can launch the debugger on a single python file and with `Flask Backend` you can launch the flask application with the VSCode debugger directly (in Debug mode of course)

Be carefull to set the correct `API_ENDPOINT_PORT` inside the vscode fastapi debug configuration.

Then you have to create another file inside the `.vscode` folder in your project, this file is called: `settings.json`.
The file contains all the **python settings and information for the project and the ide**.

After you have created the file and installed the project with poetry launch: `poetry show -v`, then copy the first path of your virtualenv.

Now paste this settings inside the new `settings.json` file.
```json
{
    "python.pythonPath": "<path of your local virtualenv>/bin/python",
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": false,
    "python.linting.enabled": true
}

```
Substitute `<path of your local virtualenv>` with the path copied from `poetry show -v` command.

After this reload vscode and every time you open a new windows vscode automatically activate the venv created with poetry for you.

### Usefull dev extensions

If you want some informations about dev extension for this repository for VSCode look inside `.vscode/extensions.json` file.

### Other informations about vscode or python configurations

If you want to have other informations please check our website (English and Italian only): https://pythonbiellagroup.it

## Launch and debug (development mode)

Instructions to launch and debug the project locally with vscode.

1. Clone the project
2. Install vscode + poetry (if you don't know to install poetry check this guide)
3. Set vscode (and vscode related files for debugging and venv) with the instructions in this readme file
4. Install the dependencies of the project with poetry by doing: `poetry install`
5. If you want to activate the venv created with poetry in your terminal do: `poetry shell`
6. After all the configurations restart vscode, then vscode will update your default IDE virtual env by default (if all the configurations are correct)
7. You can use the vscode debugger to launch the application or to launch a single python script file


The environment variabile called DEBUG_MODE should be False if you want to test the app via gunicorn.
If the environment variable is True you should use the Debug function of VS Code.

If you experience some changes to the pyproject.toml file, you can update your local version of the libraries and environment by running the command: `poetry update`

If you want you can use also the shell script: `launch-debug.sh` to test the project in debug mode with Flask and without gunicorn

## Documentation

If you want to see the official documentation of the project you can check it here:
   - http://localhost:8042/docs
   - http://localhost:8042/redoc

The OpenAPI documentation is created automatically by FastAPI.

Please consider that the port and the host can be changed based on your personal project configuration.

## Launch in production mode

First of all check if you have all the tools installed correctly on your machine.

If you want to launch the code (flask backend) in production mode with `gunicorn` you can use the `launch.sh` script located inside the main folder.

Remember to set the permissions of the script: `sudo chmod +x launch.sh`
Launch with: `./scripts/launch.sh`

If you get the error: `gunicorn: not found` you need to activate the poetry env by doing: `poetry shell`

You can also launch the single docker compose if you want to test the code inside the docker container by doing `docker-compose up --build -d`



## Considerations and know issues

To use the system with psycopg2 for the postgres database connection it's important to install in your system (linux-based) the requirements: `sudo apt-get install libpq-dev`

To launch the project from terminal if you are on the project root you have to do: `PYTHONPATH="./" python ./test/<name of the script>.py`

Be carefull not to install virtualenv via `apt` on linux, but use virtualenv by `pip`.

### Useful commands
If you want to restore docker on your machine:
```bash
docker system prune --all
```

Open the port on your machine if you are developing remotely (in a VPS for example and in a Linux OS based):
```bash
# if you want to launch the mapping in detach mode
ssh -f -N pbg
```

Launch a single docker image based on the docker compose:
```bash
docker-compose up --build -d fastapi-db
```

With this command you have to set your <pbg> ssh config profile with the ports in the `~/.ssh/config` file.  
For example:
```bash
# put this inside the config file
LocalForward 8042 127.0.0.1:8042
LocalForward 8000 127.0.0.1:8000
```


### Use Alembic to do migrations
Alembic can help you to launch migrations and propagate changes to the data class models to the database.
This process can help you to not destroy and recreate the database every time you want to update the database schema.

Remember also that if you want to use alembic in the project you need to have an `alembic` folder with inside the `env.py` script and the `versions` folder empty (if you want to start from zero, instead inside the versions folder you can have some history of migrations of the project)

Create a migration script (inside the folder: alembic)
```bash
alembic revision -m "first migration"
```

Run the first migration
```bash
alembic upgrade head
```

Then every time you want to do a migration (a database change process), you can simply repeat those 2 steps.

If you want to view the current version of the database:
```bash
alembic current
```

If you want to see the history of the database and migrations;
```bash
alembic history --verbose
```

You can also downgrade to a specific point or to the beginning of the database (very dangerous).
Remember that after a downgrade you can also come back to the head
```bash
#downgrade to the beginning of the database
alembic downgrade base

# upgrade again to the head
alembic upgrade head
```