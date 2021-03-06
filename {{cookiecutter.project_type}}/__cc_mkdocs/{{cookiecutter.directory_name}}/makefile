.PHONY: project_black
black:
	black app test setup.py --check

.PHONY: project_flake
flake:
	flake8 app test setup.py

.PHONY: project_interrogate
interrogate:
	interrogate -vv --ignore-nested-functions --ignore-semiprivate --ignore-private --ignore-magic --ignore-module --ignore-init-method --fail-under 100 tests
	interrogate -vv --ignore-nested-functions --ignore-semiprivate --ignore-private --ignore-magic --ignore-module --ignore-init-method --fail-under 100 clumper

.PHONY: project_test
test:
	pytest

.PHONY: check
check: black flake test interrogate

.PHONY: poetry_install
install-dev:
	poetry config virtualenvs.in-project true
	poetry install
	poetry show -v

.PHONY: install_pipeline
install-pipeline:
	pip install --upgrade pip
	pip install poetry==1.1.13
	poetry config virtualenvs.in-project false
	poetry install --no-root --no-dev --no-interaction --no-ansi
	poetry show -v

.PHONY: project_clean
clean:
	rm -rf **/.ipynb_checkpoints **/.pytest_cache **/__pycache__ **/**/__pycache__ ./notabooks/ipynb_checkpoints .pytest_cache ./dist ./volumes

.PHONY: project_restore
restore:
	rm -rf **/.ipynb_checkpoints **/.pytest_cache **/__pycache__ **/**/__pycache__ ./notabooks/ipynb_checkpoints .pytest_cache ./dist .venv poetry.lock

.PHONY: poetry_build
package_build:
	poetry build

.PHONY: publish_pypi
pypi:
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*

.PHONY: docs_launch
docs_launch:
	mkdocs serve

.PHONY: docs_build
docs_build:
	mkdocs build

.PHONY: docs_launch_docker
docs_launch_docker:
	mkdocs build
	mkdocs serve --dev-addr=0.0.0.0:8000

.PHONY: docs_debug_docker
docs_launch_debug_docker:
	mkdocs build
	mkdocs serve -v --dev-addr=0.0.0.0:8000

.PHONY: docs_deploy-github
docks_deploy: 
	mkdocs build
	mkdocs gh-deploy --force

.PHONY: docs_public
docs_public:
	mkdocs build -c -v --site-dir public