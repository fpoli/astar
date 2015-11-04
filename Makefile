
.PHONY: report linter docs clean

report:
	@$(MAKE) $@ --no-print-directory --directory=report

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
