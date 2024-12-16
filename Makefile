PHONY: install run virtualenv ipython clean test pflake8 fmt lint


install:
	@echo "Installing for dev environment"
	@.venv/bin/python -m pip install -e '.[test,dev]'


virtualenv:
	@echo "Creating virtual environment"
	@python -m venv .venv
	@echo "Virtual environment created"


run:
	@echo "Running app..."
	@python manage.py runserver


test:
	@echo "Running tests..."
	@python manage.py test payments
	@echo "Tests complete!!"


ipython:
	@.venv/bin/ipython


lint:
	@echo "Running pflake8 for linting"
	@.venv/bin/pflake8 core payments --config=pyproject.toml
	@echo "Linting complete"

fmt:
	@echo "Running isort and black for formatting"
	@.venv/bin/isort --profile=black --skip .venv -m 3 core payments
	@.venv/bin/black --exclude .venv core payments


clean:            ## Clean unused files.
	@echo "Cleaning project"
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build
