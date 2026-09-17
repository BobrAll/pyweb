PYTHON ?= $(shell if [ -x .venv/bin/python ]; then echo .venv/bin/python; else echo python3; fi)
MKDOCS ?= $(PYTHON) -m mkdocs
SPHINXBUILD ?= $(PYTHON) -m sphinx

.PHONY: all pipeline charts build serve clean

all: build

pipeline:
	$(PYTHON) scripts/run_experiment.py

charts:
	$(PYTHON) scripts/make_charts.py

build: pipeline charts
	$(MKDOCS) build --strict
	$(SPHINXBUILD) -b html sphinx sphinx/_build/html
	rm -rf site/sphinx
	cp -r sphinx/_build/html site/sphinx

serve: pipeline charts
	$(MKDOCS) serve

clean:
	rm -rf site .build sphinx/_build
