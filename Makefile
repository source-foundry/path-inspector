all: install

black:
	black -l 90 lib/pathins/*.py

clean:
	- rm dist/*.whl dist/*.tar.gz dist/*.zip

dist-build: clean
	python3 setup.py sdist bdist_wheel

dist-push:
	twine upload dist/*.whl dist/*.tar.gz

import-sort:
	isort -l 90 lib/pathins

install:
	pip3 install --ignore-installed -r requirements.txt .

install-dev:
	pip3 install --ignore-installed -r requirements.txt -e ".[dev]"

install-user:
	pip3 install --ignore-installed --user .

test: test-lint test-type-check test-unit

test-coverage:
	coverage run --source pathins -m py.test
	coverage report -m
#	coverage html

test-lint:
	flake8 --ignore=W50 lib/pathins

test-type-check:
	mypy --pretty lib/pathins

test-unit:
	tox

uninstall:
	pip3 uninstall --yes pathins

.PHONY: all black clean dist-build dist-push import-sort install install-dev install-user test test-lint test-type-check test-unit uninstall