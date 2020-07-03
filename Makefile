python ?= /usr/bin/env python3

dependencies := counterpar/*.py


#@ List helpful targets
help:
	@ scripts/make-help.awk $(MAKEFILE_LIST)


#@ Generate developer documentation
docs: docs/counterpar/*

docs/counterpar/*: $(dependencies)
	$(python) -m pdoc --html -f -o docs counterpar

#@ Start a live server for developer documentation
docs.live:
	$(python) -m pdoc --http : counterpar


#@ Run required tests/lints
test: test.pylint test.mypy test.pytest

#@ Run required pylint tests
test.pylint:
	$(python) -m pylint counterpar
	$(python) -m pylint tests

#@ Run required mypy tests
test.mypy:
	$(python) -m mypy -m counterpar

#@ Run required pytest tests
test.pytest:
	$(python) -m pytest $(pytest) tests

#@ Run pytest and generate coverage report
test.cov:
	$(python) -m pytest --cov=counterpar --cov-branch --cov-report=html tests


#@ Build distribution archives
build:
	$(python) setup.py sdist bdist_wheel


#@ Clean everything
clean: clean.build clean.docs clean.cov clean.caches

#@ Clean build/egg/dist artifacts
clean.build:
	rm build counterpar.egg-info dist -rf

#@ Clean documentation
clean.docs:
	rm docs -rf

#@ Clean coverage
clean.cov:
	rm .coverage htmlcov -rf

#@ Clean caches
clean.caches:
	rm .mypy_cache .pytest_cache -rf */__pycache__
