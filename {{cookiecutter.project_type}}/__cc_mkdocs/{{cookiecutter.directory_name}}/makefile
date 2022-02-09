NAME := provalo
VENV := $(shell echo $${VIRTUAL_ENV-.venv})
PY3 := $(shell command -v python3 2> /dev/null)
PYTHON := $(VENV)/bin/python
INSTALL_STAMP := $(VENV)/.install.stamp


$(PYTHON):
	@if [ -z $(PY3) ]; then echo "Python 3 could not be found."; exit 2; fi
	$(PY3) -m venv $(VENV)

install: $(INSTALL_STAMP)
$(INSTALL_STAMP): $(PYTHON) requirements.txt constraints.txt
	$(PIP_INSTALL) -Ur requirements.txt -c constraints.txt
	touch $(INSTALL_STAMP)

.PHONY: clean
clean:
	find . -type d -name "__pycache__" | xargs rm -rf {};
	rm -rf $(VENV) $(INSTALL_STAMP) .coverage .mypy_cache

.PHONY: lint
lint: $(INSTALL_STAMP)
	$(VENV)/bin/isort --profile=black --lines-after-imports=2 --check-only ./tests/ $(NAME) --virtual-env=$(VENV)
	$(VENV)/bin/black --check ./tests/ $(NAME) --diff
	$(VENV)/bin/flake8 --ignore=W503,E501 ./tests/ $(NAME)
	$(VENV)/bin/mypy ./tests/ $(NAME) --ignore-missing-imports
	$(VENV)/bin/bandit -r $(NAME) -s B608

.PHONY: format
format: $(INSTALL_STAMP)
	$(VENV)/bin/isort --profile=black --lines-after-imports=2 ./tests/ $(NAME) --virtual-env=$(VENV)
	$(VENV)/bin/black ./tests/ $(NAME)

.PHONY: test
test: $(INSTALL_STAMP)
	$(PYTHON) -m pytest ./tests/ --cov-report term-missing --cov-fail-under 100 --cov $(NAME)

.PHONY: launch
launch:
	mkdocs serve

.PHONY: build
build:
	mkdocs build

.PHONY: launch_docker
launch_docker:
	mkdocs build
	mkdocs serve --dev-addr=0.0.0.0:8000

.PHONY: debug_docker
launch_docker:
	mkdocs build
	mkdocs serve -v --dev-addr=0.0.0.0:8000

.PHONY: deploy-github
deploy: 
	mkdocs build
	mkdocs gh-deploy --force

.PHONY: public
public:
	mkdocs build
	mkdocs build --site-dir public

.PHONY: template
template:
	npm start
	mkdocs serve --watch-theme

.PHONY: template_build
template_build:
	npm run build