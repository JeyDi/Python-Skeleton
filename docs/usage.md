# Usage

## Requirements
In addition to Python 3.8, this project requires
- [Cookiecutter](https://cookiecutter.readthedocs.io/): 
  :::{code-block} console
    $ python3 -m pip install --user cookiecutter
  :::

- [Poetry](https://python-poetry.org/docs/): 
  :::{code-block} console
    $ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
  :::

## Getting started
1. Run the cookiecutter command 
  :::{code-block} console
    $ cookiecutter https://github.com/JeyDi/Python-Skeleton
  :::

2. Select your template:
  :::{code-block} console
    $ cookiecutter https://github.com/JeyDi/Python-Skeleton
    Select project_type:
    1 - Base
    2 - FastAPI
    3 - Package
    4 - Streamlit
    Choose from 1, 2, 3, 4 [1]: 2
  :::
    
  This will prompt the template specific configurations.
  
3. Move to the newly created directory and install the required dependencies
  :::{code-block} console
    $ cd <directory_name>
    $ poetry shell
    $ poetry install
  :::

4. (Optional) Set-up a GIT repository and link it to the remote one:
  :::{code-block} console
    $ git init
    $ git remote add origin <repo_url>
    $ git add .
    $ git commit -m 'Initial commit'
    $ git push -u origin master
  :::

## IDEs
VSCode is supported and configured with settings files.

PyCharm ...

## Templates usage
Specific template documentation can be found in the following sections:
- [Package](Python Package template)
- [FastAPI](FastAPI template)
- [Streamlit](Streamlit template)
- [Base](Base python template)

:::{toctree}
  :hidden:
usage_pkg
usage_streamlit
usage_fastAPI
:::