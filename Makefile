CURR_DIR := $(shell pwd)
BOT_KEY := $(shell cat bot.key)

.PHONY: report linter docs clean

report:
	@$(MAKE) $@ --no-print-directory --directory=report

start:
	@PYTHONPATH="$(CURR_DIR)/src/:$${PYTHONPATH}" \
		./src/main.py $(BOT_KEY)

linter:
	@pep8 --ignore="E221" src/

docs:
	@rm -rf docs/source/api/*
	@cd src/ && sphinx-apidoc --module-first --force --separate --output-dir=../docs/source/api/ .
	@$(MAKE) html --no-print-directory --directory=docs

clean:
	@$(MAKE) $@ --no-print-directory --directory=docs
	@find . -name '*.pyc' -delete
	@find . -name '__pycache__' -delete
