PYTHON ?= $(shell if [ -x .venv/bin/python ]; then echo .venv/bin/python; else echo python3; fi)
MKDOCS ?= $(PYTHON) -m mkdocs
SPHINXBUILD ?= $(PYTHON) -m sphinx
MIKE ?= $(shell if [ -x .venv/bin/mike ]; then echo .venv/bin/mike; else echo mike; fi)
REMOTE ?= origin

.PHONY: all pipeline charts sphinx build serve publish clean

all: build

pipeline:
	$(PYTHON) scripts/run_experiment.py

charts:
	$(PYTHON) scripts/make_charts.py

sphinx:
	$(SPHINXBUILD) -b html -d sphinx/_build/doctrees sphinx sphinx/_build/html

build: pipeline charts sphinx
	$(MKDOCS) build --strict

serve: pipeline charts sphinx
	$(MKDOCS) serve

publish: build
	@test -n "$(VERSION)" || { echo "usage: make publish VERSION=v1.1"; exit 2; }
	$(MIKE) deploy --push -r $(REMOTE) --update-aliases --allow-empty --alias-type copy "$(VERSION)" latest
	$(MIKE) set-default --push -r $(REMOTE) --allow-empty latest

clean:
	rm -rf site .build sphinx/_build
