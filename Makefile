#
# Makefile for pynote
#
# Combines scripts for common tasks.
#
# Copyright: (c) 2013-2014 Stefan Tatschner <stefan@sevenbyte.org>
# License: MIT, see COPYING for details.
#


PYTHON ?= python

.PHONY: all clean test

all: clean test

clean:
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

test:
	@$(PYTHON) tests.py
