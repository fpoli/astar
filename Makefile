CURR_DIR := $(shell pwd)
BOT_KEY := $(shell cat bot.key)

.PHONY: default report start linter test docs clean

default: start

report:
	@echo "(*) Generate report..."
	@$(MAKE) $@ --no-print-directory --directory=report

start:
	@echo "(*) Start bot..."
	@PYTHONPATH="$${PYTHONPATH}:$(CURR_DIR)/src/" \
		./src/main.py $(BOT_KEY)

linter:
	@echo "(*) Run linter..."
	@pep8 --ignore="E221" src/ test/

test:
	@echo "(*) Run tests..."
	@PYTHONPATH="$${PYTHONPATH}:$(CURR_DIR)/src/:$(CURR_DIR)/test/" \
		python3 -m "nose" --nocapture -w test/

test:
	@echo "(*) Run tests..."
	@PYTHONPATH="$${PYTHONPATH}:$(CURR_DIR)/src/:$(CURR_DIR)/test/" \
		python3 -m "nose" --nocapture -w test/

docs: clean
	@echo "(*) Generate documentation..."
	@cd src/ && sphinx-apidoc --module-first --force --separate --output-dir=../docs/source/api/ .
	@$(MAKE) html --no-print-directory --directory=docs

clean:
	@echo "(*) Clean project..."
	@rm -rf docs/source/api/*
	@$(MAKE) $@ --no-print-directory --directory=docs
	@find . -name '*.pyc' -delete
	@find . -name '__pycache__' -delete
