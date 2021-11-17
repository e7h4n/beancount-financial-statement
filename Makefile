SRC_CORE=beanstatement
SRC_RESOURCES=resources
PYTHON=python3
PYDOC=pydoc3
PIP=pip3


help: ## Print help for each target
	$(info Things3 low-level Python API.)
	$(info =============================)
	$(info )
	$(info Available commands:)
	$(info )
	@grep '^[[:alnum:]_-]*:.* ##' $(MAKEFILE_LIST) \
		| sort | awk 'BEGIN {FS=":.* ## "}; {printf "%-25s %s\n", $$1, $$2};'

test: ## Test the code
	@type coverage >/dev/null 2>&1 || (echo "Run '$(PIP) install coverage' first." >&2 ; exit 1)
	@coverage run --source . -m beanstatement.reporter_test
	@coverage report

doc: ## Document the code
	@$(PYDOC) src

clean: ## Cleanup
	@rm -f $(SRC_CORE)/**/*.pyc
	@rm -rf $(SRC_CORE)/**/__pycache__

auto-style: ## Style the code
	@if type autopep8 >/dev/null 2>&1 ; then autopep8 -i -r $(SRC_CORE) ; \
	 else echo "SKIPPED. Run '$(PIP) install autopep8' first." >&2 ; fi

code-style: ## Test the code style
	@if type pycodestyle >/dev/null 2>&1 ; then pycodestyle --max-line-length=120 $(SRC_CORE) ; \
	 else echo "SKIPPED. Run '$(PIP) install pycodestyle' first." >&2 ; fi

code-count: ## Count the lines of code
	@if type cloc >/dev/null 2>&1 ; then cloc $(SRC_CORE) ; \
	 else echo "SKIPPED. Run 'brew install cloc' first." >&2 ; fi

code-lint: ## Lint the code
	@if type pyflakes >/dev/null 2>&1 ; then pyflakes $(SRC_CORE) ; \
	 else echo "SKIPPED. Run '$(PIP) install pyflakes' first." >&2 ; fi
	@if type pylint >/dev/null 2>&1 ; then pylint $(SRC_CORE) ; \
	 else echo "SKIPPED. Run '$(PIP) install pylint' first." >&2 ; fi
	@if type flake8 >/dev/null 2>&1 ; then flake8 --max-complexity 10 $(SRC_CORE) ; \
	 else echo "SKIPPED. Run '$(PIP) install flake8' first." >&2 ; fi
	@if type pyright >/dev/null 2>&1 ; then pyright $(SRC_CORE) ; \
	 else echo "SKIPPED. Run 'npm install -f pyright' first." >&2 ; fi
	@if type mypy >/dev/null 2>&1 ; then mypy --ignore-missing-imports $(SRC_CORE) ; \
	 else echo "SKIPPED. Run '$(PIP) install mypy' first." >&2 ; fi
