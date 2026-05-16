.PHONY: help install lint validate test clean

help:
	@echo "Available targets:"
	@echo "  install    Install development dependencies"
	@echo "  lint       Run YAML linting"
	@echo "  validate   Run blueprint validation"
	@echo "  test       Run all tests (lint + validate)"
	@echo "  clean      Clean up temporary files"

install:
	pip install -r requirements.txt
	pre-commit install

lint:
	yamllint -c .yamllint.yaml blueprints/

validate:
	python .github/scripts/validate_blueprints.py
	python .github/scripts/check_metadata.py

test: lint validate
	@echo "All tests passed!"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
