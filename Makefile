.ONESHELL:
SHELL := /bin/bash
SRC = $(wildcard ./*.ipynb)

all: metaflow_magicdir docs

metaflow_magicdir: $(SRC)
	nbdev_build_lib
	touch metaflow_magicdir

sync:
	nbdev_update_lib

docs_serve: docs
	cd docs && bundle exec jekyll serve

docs: $(SRC)
	nbdev_build_docs
	touch docs

test:
	nbdev_test_nbs

release: pypi
	nbdev_bump_version

conda_release:
	fastrelease_conda_package

pypi: dist
	twine upload --repository pypi dist/*

dist: clean
	nbdev_bump_version
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist