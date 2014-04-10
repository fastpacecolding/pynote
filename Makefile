PYTHON ?= python
PROJECT = pynote
COPYRIGHT = "Stefan Tatschner"
EMAIL = "stefan@sevenbyte.org"
LOCALE = de
VERSION = 0.2.2

.PHONY: release test pybabel-extract pybabel-init pybabel-update pybabel-compile

docs:
	$(MAKE) --directory=doc html
	$(MAKE) --directory=doc man

release: docs pybabel-compile
	$(PYTHON) setup.py sdist

test:
	@$(PYTHON) tests.py

extract-messages:
	@pybabel extract pynote --project=$(PROJECT) --copyright=$(COPYRIGHT) \
	  --version=$(VERSION) --msgid-bugs-address=$(EMAIL)  \
	  --output=messages.pot

init-locale:
	@pybabel init --domain=pynote --locale=$(LOCALE) --input-file=locale/messages.pot \
	  --output-dir=locale

update-locale:
	@pybabel update --domain=pynote --locale=$(LOCALE) --input-file=locale/messages.pot \
	  --output-dir=locale

compile-locales:
	@pybabel compile --directory=locale --domain=$(PROJECT)
