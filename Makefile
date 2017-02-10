PROJECT := pirec

.PHONY: checks test docstyle codestyle lint

checks: test docstyle codestyle lint

test:
	pytest --cov $(PROJECT)

docstyle:
	pydocstyle $(PROJECT)

codestyle:
	pycodestyle $(PROJECT)

lint:
	pylint $(PROJECT)
