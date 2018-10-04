root_dir := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

all: coverage flake

flake:
	flake8 hovercraft tests

coverage:
	coverage run setup.py test
	coverage html
	coverage report

test:
	python setup.py test

