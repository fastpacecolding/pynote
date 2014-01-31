#
# Makefile for pynote
#
# Combines scripts for common tasks.
#
# Copyright: (c) 2013-2014 Stefan Tatschner <stefan@sevenbyte.org>
# License: MIT, see COPYING for details.
#


PYTHON ?= python

.PHONY: all clean test man pybabel-extract pybabel-init-de pybabel-compile-de \
		pybabel-update-de

clean:
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

test:
	@$(PYTHON) tests.py

man:
	a2x --doctype manpage --format manpage man/noterc.txt

pybabel-extract:
	pybabel extract pynote --project=pynote --copyright="Stefan Tatschner" \
	  --version=0.2 --msgid-bugs-address="stefan@sevenbyte.org"  \
	  --output=messages.pot

pybabel-init-de:
	pybabel init --domain=pynote --locale=de --input-file=messages.pot \
	  --output-dir=locale

pybabel-update-de:
	pybabel update --domain=pynote --locale=de --input-file=messages.pot \
	  --output-dir=locale

pybabel-compile-de:
	pybabel compile --directory=locale --locale=de --domain=pynote
