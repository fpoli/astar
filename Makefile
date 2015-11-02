
.PHONY: report
report:
	@$(MAKE) $@ --no-print-directory --directory=report

linter:
	@pep8 src/
